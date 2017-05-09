
## Live migration with Socket (INET)

Run the server side:

`docker run --name sserver --network=fognode --rm -v $(pwd):/code -p 8888:8888 diunipisocc/sserver `

The client has an internal state that send to the server:
`docker run --name sclient  --network=fognode -v $(pwd):/code  diunipisocc/sclient`


Checkpoint of the client
`docker checkpoint create sclient ckclient`

Restart the client
`docker start --checkpoint ckclient sclient`
