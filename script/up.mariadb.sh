source _base.up.sh

export MARIADB_IMAGE="${DOCKERS_DIR}/mariadb.compose.yml"

docker-compose -f "$MARIADB_IMAGE" up -d --force-recreate --build

# mariadb server and adminer are run now
# you can go to adminer with http://localhost:8080
