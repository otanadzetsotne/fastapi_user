# shellcheck disable=SC2155
export SCRIPTS_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export BASE_DIR="${SCRIPTS_DIR}/.."
export DOCKERS_DIR="${BASE_DIR}/docker"
export VOLUMES_DIR="${BASE_DIR}/volume"

mkdir -p "${VOLUMES_DIR}"
