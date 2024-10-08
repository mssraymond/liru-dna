"""
GitHub class to work with GitHub's REST API. Personal Access Token required.
"""

import sys
from typing import Any, Dict, List
import requests
import yaml
from src.logger import Logger

sys.path.append("..")


class GitHubException(Exception):
    """GitHub REST API Exceptions"""


class GitHub:
    def __init__(self) -> None:
        with open("secrets.yml", mode="r", encoding="utf-8") as stream:
            secrets = yaml.safe_load(stream=stream)
            token = secrets["github_personal_access_token"]
        self.entities = {
            "company",
            "ships",
            "landpads",
            "launches",
            "starlink",
        }  # Add more entity endpoints by including entity names in this set.
        self.url = "https://api.github.com/repos/{owner}/{repo}/contents"
        self.owner = "r-spacex"
        self.repo = "SpaceX-API"
        self.full_url = self.url.format(owner=self.owner, repo=self.repo)
        self.headers = {"Authorization": f"Bearer {token}"}
        self.timeout: int = 120
        self.logger = Logger()
        self.sha = "?ref=5c2cae2ba1d9e423bc75ab609e730d87edca5c21"  # Hardcoded sha to ensure reference doc remains unchanged

    def traverse(self) -> List[str]:
        self.logger.info(
            f"Parsing SpaceX's GitHub documentation at `{self.full_url}`..."
        )
        paths: List[str] = []
        try:
            resp = requests.get(
                url=self.full_url + "/docs" + self.sha,
                headers=self.headers,
                timeout=self.timeout,
            )
        except Exception as e:
            self.logger.exception(e)
            raise GitHubException(e) from e

        def traverse_recur(pages: Any, paths: List[str]) -> None:
            if isinstance(pages, List):
                for page in pages:
                    traverse_recur(
                        pages=requests.get(
                            url=self.full_url + page["path"] + self.sha,
                            headers=self.headers,
                            timeout=self.timeout,
                        ).json(),
                        paths=paths,
                    )
            elif isinstance(pages, Dict):
                paths.append(pages["html_url"])

        for item in resp.json():
            if item["name"] in self.entities:
                try:
                    traverse_recur(
                        pages=requests.get(
                            url=self.full_url + item["path"] + self.sha,
                            headers=self.headers,
                            timeout=self.timeout,
                        ).json(),
                        paths=paths,
                    )
                except Exception as e:
                    self.logger.exception(e)
                    raise GitHubException(e) from e
        self.logger.info("Documentation successfully parsed.")
        return paths
