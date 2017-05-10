
docker login

# create app image containinr of a paralle app with inside a app controller
docker build -t diunipisocc/sclient -f Dockerfile-sclient .
docker push diunipisocc/sclient

# create the foge node controller
docker build -t diunipisocc/sserver -f Dockerfile-sserver .
docker push diunipisocc/sserver
