source _base.up.sh

export IMAGE="${DOCKERS_DIR}/smtp.dockerfile"
export IMAGE_NAME="imsim.io.smtp"

docker build -t $IMAGE_NAME -f $IMAGE .
docker run -d -p $SMTP__PORT:1025 -p 1080:1080 --network imsim.io --name $IMAGE_NAME $IMAGE_NAME
