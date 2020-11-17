# !/bin/bash

if [ -x "$(command -v docker)" ]; then
	echo "Docker installed"
else
	echo "Installing docker..."
	apt-get update
	
	# install docker
	apt install docker.io
	systemctl start docker
	systemctl enable docker

	# install docker-compose
	apt install docker-compose
fi


