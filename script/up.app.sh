source _base.sh

# shellcheck disable=SC2155
export CUR_DATE="$(date +%d_%m_%Y__%k_%M_%S)"
export IMAGE="${DOCKERS_DIR}/app.dockerfile"
export IMAGE_NAME="imsim.io.app"

docker build -t "${IMAGE_NAME}:latest" -f "${IMAGE}" "${BASE_DIR}"
docker run -d -p 80:80 -v "${APP_DIR}":/app --name "${IMAGE_NAME}_${CUR_DATE}" "${IMAGE_NAME}"
