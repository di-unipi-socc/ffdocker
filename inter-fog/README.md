
## Intra-node experiment - Live migration
IN order to run the `checkpoint` command the `experimental` featured of the docker daemon should be enabled.

Create a network
`docker network create fognode`

## Development mode
The images do not contain the source code of the component.

`docker build -t diunipisocc/filtering -f Dockerfile-filtering-dev .`

`docker build -t diunipisocc/selection -f Dockerfile-selection-dev .`

`docker build -t diunipisocc/fnc -f Dockerfile-fnc-dev .`

Run the *`fnc`*:
`docker run --name fnc  --rm  \
        -v $(pwd):/code  \
        -v /usr/bin/docker:/usr/bin/docker \
        -v /var/run/docker.sock:/var/run/docker.sock \
        --network=fognode  \
        diunipisocc/fnc`


Run the *`selection`*:
`docker run --name selection \
        --network=fognode \
        -v $(pwd):/code  \
        diunipisocc/selection`

Run the *`filtering`*:
`docker run --name filtering    \
        -v $(pwd):/code        \
        --network=fognode        \
        diunipisocc/filtering`



## Docker swarm, services and live migration
Only swarm services can connect to overlay networks, not standalone containers. For more information about swarms, see Docker swarm mode overlay network security model and Attach services to an overlay network.


`docker build -t diunipisocc/sserver -f Dockerfile-sserver .`

`docker build -t diunipisocc/sclient -f Dockerfile-sclient .`


 // docker run --name sserver --network=fognode --rm  -p 8888:8888 diunipisocc/sserver

`docker service create --name sserver  \
                        --network interfog-network  \
                        --constraint  node.role==manager \
                        --publish 8888:8888  \
                        diunipisocc/sserver
                        `


`docker service create --name sclient  \
        --network interfog-network  \
        --constraint  node.role==manager \
        diunipisocc/sclient
`

`docker service create --name sclient  \
        --network interfog-network  \
        --constraint  node.role==worker \
        diunipisocc/sclient
`
