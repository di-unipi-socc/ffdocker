

docker build -t diunipisocc/fnc -f Dockerfile-fnc .
docker run --rm --name fnc -v /tmp/:/tmp/ -v /var/run/docker.sock:/var/run/docker.sock diunipisocc/fnc



docker build -t diunipisocc/app -f Dockerfile-app .
CID=$(docker run --rm --name app -v /tmp/ffsocket.sock:/tmp/ffsocket.sock diunipisocc/app)
echo "App images started"
