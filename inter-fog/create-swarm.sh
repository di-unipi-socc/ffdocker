# create worker in the virtual box machine
docker-machine create -d virtualbox worker

# init swarm on local machine
docker swarm init --advertise-addr 192.168.99.1

#Join the worker to the swarm
docker-machine ssh worker \
  	"docker swarm join \
  	--token SWMTKN-1-0mdvyebwmnmfkp2gfgccgf6frgyqb7xhr68f28zxqgqnhm36qt-f0srutiwpsjk7jvedzxfve147  \
  	--advertise-addr   	192.168.99.1 \
  	192.168.99.1:2377"

# create multi-host networking
docker network create \
    --driver overlay \
    --subnet 10.0.9.0/24 \
    interfog-network
