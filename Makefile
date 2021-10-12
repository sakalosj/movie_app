VENV=venv
PYTHON=$(VENV)/bin/python3
PIP=$(VENV)/bin/pip3
SUDO=$$(which sudo)
.DEFAULT_GOAL=help
BUILD_REQUIREMENTS=./requirements_dev.txt

.PHONY: help test install db_start db_stop db_clean

$(VENV):
	$(SUDO) apt update && $(SUDO) apt install -y python3 python3-pip python3-venv
	python3 -m venv $(VENV)
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

$(PIP) $(PYTHON): $(VENV)

#help: @ List available tasks on this project
help:
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| sort | tr -d '#'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

#install: @ Install current project with all dependencies
install: $(PIP)
	 $(PIP) install -e .

#db_start: @ Starts app db with default port 4432 inside docker
db_start:
	docker run --name movie_db --rm -v ~/tmp/db_data/movie_app_db:/var/lib/postgresql/data -e POSTGRES_USER=user1 \
-e POSTGRES_PASSWORD=passwd -e POSTGRES_DB=movie_db -p 4432:5432 -v ${PWD}/data/init.sql:/docker-entrypoint-initdb.d/init.sql -d postgres

#db_stop: @ Stops app db
db_stop:
	docker stop movie_db

#db_clean: @ Removes app db
db_clean:
	$(SUDO) rm -rf ~/tmp/db_data/movie_app_db

#test_db_start: @ Starts test db with default port 4442 inside docker
test_db_start:
	docker run --name test_movie_db --rm -v ~/tmp/db_data/test_movie_app_db:/var/lib/postgresql/data \
-e POSTGRES_USER=user1 -e POSTGRES_PASSWORD=passwd -e POSTGRES_DB=movie_db \
-v ${PWD}/data/init.sql:/docker-entrypoint-initdb.d/init.sql  -p 4442:5432 -d postgres

#test_db_stop: @ Stops test db
test_db_stop:
	docker stop test_movie_db

#test_db_clean: @ Removes test db
test_db_clean:
	$(SUDO) rm -rf ~/tmp/db_data/test/movie_app_db

#web_start: @ Starts app using gunicorn
web_start:  $(VENV)
	gunicorn -w 4 -b 0.0.0.0:4000 movie_app.app:app --daemon

#unit_test: @ Executes unit tests
unit_tests:
	MOVIE_CFG=./tests/data/test_movie_app.yaml pytest --cov=src tests/unit/

#integration_test: @ Executes integration tests
integration_tests:
	MOVIE_CFG=./tests/data/test_movie_app.yaml pytest --cov=src tests/integration/
