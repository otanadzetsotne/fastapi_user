# shellcheck disable=SC2155
export SCRIPTS_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export BASE_DIR="${SCRIPTS_DIR}/.."
export APP_DIR="${BASE_DIR}/app"
export DOCKERS_DIR="${BASE_DIR}/docker"
export VOLUMES_DIR="${BASE_DIR}/volume"
export CONFIG_DIR="${BASE_DIR}/cfg"

mkdir -p "${VOLUMES_DIR}"
