"""
SpaceX class to work with SpaceX REST API.
"""

import json
from typing import Any, Dict, List, Tuple, Union
from datetime import datetime
import inspect
import requests
from src.github import GitHub
from src.logger import Logger


class SpaceXException(Exception):
    """SpaceX REST API Exception"""


class SpaceX:
    def __init__(self) -> None:
        self.logger = Logger()
        self.url: str = "https://api.spacexdata.com/"
        self.version: str = (
            "v4"  # Hardcoded to mitigate possible breaking changes in newer versions
        )
        self.github = GitHub()
        self.docs = self.github.traverse()
        self.api: Dict[str, Dict[str, str]] = {}
        self._compile_api_endpoints(logger=self.logger)
        self.timeout: int = 120

    def _compile_api_endpoints(self, logger: Logger) -> None:
        logger.info(
            f"Compiling SpaceX's REST API endpoints at `{self.url + self.version}`..."
        )
        for doc in self.docs:
            if doc.endswith("schema.md") or self.version not in doc:
                continue
            path = doc.split("/docs/")[1]
            key = path.split("/")[0]
            endpoint = path.split("/")[-1].replace(".md", "")
            path = self.url + path.replace(
                f"{key}/{self.version}", f"{self.version}/{key}"
            ).replace("all.md", "").replace("one.md", "{id}").replace(".md", "").rstrip(
                "/"
            )
            if key in self.api:
                self.api[key][endpoint] = path
            else:
                self.api[key] = {endpoint: path}
        logger.info(
            f"Endpoints successfully compiled:\n{json.dumps(self.api, indent=2)}"
        )

    def _get(self, url: str) -> Dict[str, Any]:
        try:
            resp = requests.get(
                url=url,
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                return resp.json()
            self.logger.error(resp.text)
            raise SpaceXException(resp.text)
        except Exception as e:
            self.logger.exception(e)
            raise SpaceXException(e) from e

    def _post(self, url: str, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            result = []
            while True:
                resp = requests.post(
                    url=url,
                    json=payload,
                    timeout=self.timeout,
                )
                if resp.status_code == 200:
                    resp = resp.json()
                else:
                    raise SpaceXException(resp.text)
                result += resp["docs"]
                payload["options"]["page"] += 1
                if resp["hasNextPage"] is False:
                    break
            return result
        except Exception as e:
            self.logger.exception(e)
            raise SpaceXException(e) from e

    def invoke(
        self,
        entity: str,
        identifier: str = None,
        paginate: bool = False,
        dates: Tuple[str] = None,
    ) -> Union[None, Any]:
        """
        Sample Args:
            ```

            entity: ["company", "ships", "landpads", ...]
            identifier: "5eb87d46ffd86e000604b389"
            paginate: [True|False]
            dates: (<START_DATE>, <END_DATE>) ex. ("2020-01-01", "2020-01-31")

            ```
        """

        def either_identifier_or_paginate(local_vars: Dict[str, Any]) -> bool:
            """
            Ensure only one of `identifier`, `paginate`, OR `dates` is supplied.
            """
            supplied = 0
            for key in [
                key
                for key in inspect.signature(self.invoke).parameters.keys()
                if key != "entity"
            ]:
                if key in local_vars and local_vars[key]:
                    supplied += 1
            if supplied > 1:
                return False
            return True

        if not either_identifier_or_paginate(local_vars=locals()):
            self.logger.warning(
                "Please supply EITHER `identifier`, `paginate`, OR `dates`."
            )
            return None
        if entity not in self.github.entities:
            return {
                "status": "error",
                "message": f"Entity must be one of {self.github.entities}",
            }
        if identifier:
            return self._get(url=self.api[entity]["one"].format(id=identifier))
        if paginate:
            return self._post(
                url=self.api[entity]["query"],
                payload={"options": {"page": 1, "limit": 10}},
            )
        if dates:
            start_date, end_date = dates
            start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            return self._post(
                url=self.api[entity]["query"],
                payload={
                    "options": {"page": 1, "limit": 10},
                    "query": {
                        "date_utc": {
                            "$gte": start_date,
                            "$lte": end_date,
                        }
                    },
                },
            )
        return self._get(url=self.api[entity]["all"])
