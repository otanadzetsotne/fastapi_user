source _base.up.sh

# shellcheck disable=SC2155
export CUR_DATE="$(date +%d_%m_%Y__%H_%M_%S)"
export IMAGE="${DOCKERS_DIR}/app.dockerfile"
export IMAGE_NAME="imsim.io.app"

docker build --build-arg ENV_FILE="$ENV_FILE" -t "${IMAGE_NAME}:latest" -f "${IMAGE}" "${BASE_DIR}"
docker run -d -p 80:80 -v "${APP_DIR}":/app --network imsim.io --name "${IMAGE_NAME}_${CUR_DATE}" "${IMAGE_NAME}"
