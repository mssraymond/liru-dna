<!-- markdownlint-disable MD026 -->
# Welcome to Liru-DNA!

## What is this?

Fun little side-thing that let's me play around with the UNOFFICIAL [SpaceX REST API](https://github.com/r-spacex/SpaceX-API/blob/master/docs/README.md).

## How do I get started?

- First, ensure you have Docker installed.
- Create a GitHub account (if you don't have one already) and generate a Personal Access Token.
- Clone this repository, then save your token as `github_personal_access_token: <YOUR_TOKEN>` in a `secrets.yml` file at the root.
- Build the image via `docker build -t liru-dna .`.
- Run the test script with `docker run --rm -it --name spacex liru-dna:latest`.
- If you see "All tests passed :)", then you're set!

## Cool! How about something more end-to-end?

- Assuming you've got the prerequisites setup, just run `docker-compose up`.
- Wait for `pg_ingest.py` to ingest sample data into a local PostgreSQL database.
- After it's done, connect to the DB using your query/data visualizer of choice. Mine's pgAdmin!
- I've defaulted the DB password to "postgres". Very secure, I know 😅

## What are some business questions we can answer with this?

### How about some basic company info?

![Company Info](images/company_info.png)

### What are the lightest and heaviest spaceships?

![Lightest and Heaviest Ships](images/lightest_heaviest_ships.png)

### Where are the landing pads located?

![Landing Pad Locations](images/landpad_locations.png)

### __Obviously, we'd want to do some proper data modeling before running any serious analysis. But hopefully you get the picture!__
