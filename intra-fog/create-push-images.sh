
docker login

# create app image containinr of a paralle app with inside a app controller
docker build -t diunipisocc/app -f Dockerfile-app .
docker push diunipisocc/app

# create the foge node controller
docker build -t diunipisocc/fnc -f Dockerfile-fnc .
docker push diunipisocc/fnc
