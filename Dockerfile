FROM ubuntu

# create the folder code inside the docker image
RUN mkdir /code

# set the working directory inside the image
WORKDIR /code

# copy the fastflow executable inside the image
COPY test_parfor_unbalanced /code/

# when the container starts it runs the executable in the entrypoint
ENTRYPOINT ["/code/test_parfor_unbalanced"]
