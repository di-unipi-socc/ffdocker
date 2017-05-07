
# run the server socket
docker build -t diunipisocc/sserver -f Dockerfile-sserver .
docker run --rm --name sserver -v /tmp/:/tmp/ diunipisocc/sserver

# run the client socket
docker build -t diunipisocc/sclient -f Dockerfile-sclient .
docker run --rm --name sclient -v /tmp/:/tmp/  diunipisocc/sclient
