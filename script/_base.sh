source _dirs.sh

if [[ $1 ]]
  then
    export ENV_FILE=$1
  else
    export ENV_FILE='.env'
fi

export ENV_PATH="$CONFIG_DIR/$ENV_FILE"
echo "INFO: Environment variables file: $ENV_PATH"
# shellcheck disable=SC1090
source "$ENV_PATH"
