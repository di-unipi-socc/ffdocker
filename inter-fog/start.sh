


# run the server socket
docker build -t diunipisocc/sserver -f Dockerfile-sserver .
docker run --name sserver --network=fognode --rm  -p 8888:8888 diunipisocc/sserver


# run the client socket
docker build -t diunipisocc/sclient -f Dockerfile-sclient .
docker run --name sclient  --network=fognode  diunipisocc/sclient
