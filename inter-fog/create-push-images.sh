
docker login

# create app image containinr of a paralle app with inside a app controller
docker build -t diunipisocc/filtering -f Dockerfile-filtering .
docker push diunipisocc/filtering

# create the foge node controller
docker build -t diunipisocc/selection -f Dockerfile-selection .
docker push diunipisocc/selection

# create the foge node controller
docker build -t diunipisocc/fnc:checkpoint -f Dockerfile-fnc .
docker push diunipisocc/fnc:checkpoint 
