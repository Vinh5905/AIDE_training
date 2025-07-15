include env

build:
	docker-compose build

up:
	docker-compose --env-file env up -d

down:
	docker-compose --env-file env down

restart:
	make down && make up

to_psql:
	docker exec -ti de_psql psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

import_schemas_psql:
	@echo "Copying SCHEMA into container..."
	docker cp ./psql_code/psql_schemas.sql de_psql:/tmp/
	docker exec -i de_psql psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB} -f /tmp/psql_schemas.sql
	@echo "Import schema finished."

import_csv_pqsl:
	@echo "Copying CSV into container..."
	docker cp data/ de_psql:/tmp/
	docker cp ./psql_code/psql_load_csv.sql de_psql:/tmp/
	docker exec -i de_psql psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB} -f /tmp/psql_load_csv.sql
	@echo "Import csv finished."

create_db_mysql:
	docker exec -i de_mysql mysql -u"root" -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};"

to_mysql: create_db_mysql
	docker exec -it de_mysql mysql --local-infile=1 -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" ${MYSQL_DATABASE}

to_mysql_root: create_db_mysql
	docker exec -it de_mysql mysql -u"root" -p"${MYSQL_ROOT_PASSWORD}" ${MYSQL_DATABASE}

import_schemas_mysql: create_db_mysql
	@echo "Copying SCHEMA into container..."
	docker cp mysql_code/mysql_schemas.sql de_mysql:/tmp/
	docker exec -i de_mysql mysql -u"root" -p"${MYSQL_ROOT_PASSWORD}" ${MYSQL_DATABASE} -e 'source /tmp/mysql_schemas.sql'
	@echo "Import schema finished."

import_csv_mysql: create_db_mysql
	@echo "Copying CSV into container..."
	docker cp data/ de_mysql:/tmp/
	docker cp mysql_code/mysql_load_csv.sql de_mysql:/tmp/
	docker exec -i de_mysql mysql -u"root" -p"${MYSQL_ROOT_PASSWORD}" -e "SET GLOBAL local_infile=1;"                                           # local_infile here for server
	docker exec -i de_mysql mysql --local-infile=1 -u"root" -p"${MYSQL_ROOT_PASSWORD}" ${MYSQL_DATABASE} -e 'source /tmp/mysql_load_csv.sql'    # local_infile here for client
	@echo "Import csv finished."

