# Running

- local: `python <path_to>/main.py`
- docker-compose: `PUBLISH_PORT=<port number> DATA_LOC=<path to db folder> docker compose up`

DB folder must exist, DB file will be created if not exists.

# Environment variables

- DB_FILE=*location of db file*
- MOISTURE_URL=*address of moisture service*
- CHART_FILE=*location of generated chart*
- DATA_LOC=*path to DB folder, mapped for volume on docker host*
- PUBLISH_PORT=*host port the container port is mapped to*
