#!/bin/bash

export $(cat .env.dev | xargs)

# -- parse arguments
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -p|--prod)
    export $(cat .env.prod | xargs)
    shift 
    shift 
    ;;
    -d|--dev)
    export $(cat .env.dev | xargs)
    shift 
    shift 
    ;;
    -h|--help)
    echo "OPTIONS:"
    printf "\t%s\t%s\n"  \
    "-p/--prod" "trun with production config" \
    "-d/--dev" "run with production config"  
    exit 0
    shift 
    shift
    ;;
    --default)
    DEFAULT=YES
    export $(cat .env.dev | xargs)
    shift
    ;;
    *) 
    export $(cat .env.dev | xargs)

    shift
    ;;
esac
done

git submodule add git@gitlab.com:abduakhatov/core.git modules/core

# -- install docker and run compose
sudo ./scripts/install-docker.sh
sudo -E docker-compose -f docker-compose.app.yml stop

# -- Build image
sudo docker image prune app
sudo docker image build -f Dockerfile -t "app" .

# -- Starting compose
echo "\e[31m[START]\e[0m Docker Compose";
sudo -E docker-compose -f docker-compose.app.yml up --build -d

# todo :test each stage
# todo :write ci/cd gitlab file
# todo : run docker file