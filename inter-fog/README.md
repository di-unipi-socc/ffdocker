
## Live migration with (INET) Socket
IN order to run the `checkpoint` command the `experimental` docker daemon shoul be enabled.

Create a network
`docker network create fognode`

Run the server side:

`docker run --name sserver --network=fognode --rm -v $(pwd):/code -p 8888:8888 diunipisocc/sserver`

The client has an internal state that send to the server:
`docker run --name sclient  --network=fognode -v $(pwd):/code  diunipisocc/sclient`


Create a Checkpoint of the client
`docker checkpoint create sclient ckclient`

Restore the client from the checkpoint
`docker start --checkpoint ckclient sclient`
