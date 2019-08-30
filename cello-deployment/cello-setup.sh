#!/bin/bash

#a script to install required modules for cello / fabric
#this script is tested on Ubuntu 14.04 and Debian 9

DOCKER_GPG_KEY=https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg
DOCKER_LINUX=https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")
DOCKER_COMPOSE=https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m`
NODE_JS=https://deb.nodesource.com/setup_9.x
CELLO_GIT=http://gerrit.hyperledger.org/r/cello

install_req(){
echo "Installing some packages: nano, git, make ..."
sudo apt-get update
sudo apt-get install make git -y
sudo apt-get  install gettext-base -y
sudo apt-get install nfs-common -y

sudo apt-get install nano

echo "***** Done *****"
}

install_docker(){
sudo apt-get update
sudo apt-get -y install \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     software-properties-common -y

#add gpg key
curl -fsSL $DOCKER_GPG_KEY | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] $DOCKER_LINUX \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get -y install docker-ce

echo "Testing docker ?????"
#check docker
sudo docker run hello-world
echo "***** Done *****"
}

install_docker_compose(){

echo "installing docker compose ..."
sudo curl -L $DOCKER_COMPOSE -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

#check composer
echo "checking composer version"
docker-compose --version 

}

install_nodejs(){
#install NodeJS and npm
sudo apt-get update
sudo apt-get install nodejs -y
sudo apt-get install npm -y
echo "***** Done *****"
}

install_nosejs_pac(){

sudo apt-get update
curl -sL $NODE_JS | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install -y build-essential
echo "***** Done *****"

}

clone_cello(){

git clone $CELLO_GIT && cd cello
echo "***** Done *****"

}

#main


if [ $# -eq 0 ]; then
    echo "Your command line contains $# arguments. use -m to setup master or -w to setup worker"
    exit
fi

TARGET=$1
MASTER=false
WORKER=false
if [[ "$TARGET" == "-m" ]]; then

 MASTER=true

elif [[ "$TARGET" == "-w" ]]; then

 WORKER=true

else
 
 echo $TARGET
 echo "The arg is not either -w or -m. Please use -m for master node and -w for worker node"
 exit

fi

echo "Installing req..."
install_req
echo "Installig Docker"
install_docker

echo "Installing Docker Compose"
install_docker_compose


echo "Install NodeJS"
install_nosejs_pac

echo "Clone cello git"
clone_cello
sleep 10
 

if [[ "$MASTER" == "true" ]]; then

 cd cello && make setup-master
 make build-user-dashboard-js
 make start

else 
 cd cello && make setup-worker

fi

echo "installation is done ...."
echo "config the worker Dockerd to leasten on port 2375 
for ubuntu add the this line to /etc/default/docker:

DOCKER_OPTS=\"\$DOCKER_OPTS -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --api-cors-header='*' --default-ulimit=nofile=8192:16384 --default-ulimit=nproc=8192:16384\"

and restart docker daemon: sudo service docker restart

for debian: first stop docker, sudo systemctl stop docker.service the run the following

sudo dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --api-cors-header='*' --default-ulimit=nofile=8192:16384 --default-ulimit=nproc=8192:16384 -D &
"
