
## An Architecture to Support Autonomic Data Stream Processing Applications in the Fog

The high-level architecture for supporting autonomic data
stream parallel applications in the fog is shown below composed by the following components:
 - **Fog Nodes (FNs)**: are devices (e.g., smartphones, laptops, routers) where the containerized Stream parallel Application are executed,
 - **Fog Node Controllers (FNCs)**: (containerized) component used for  scaling up/down the resources (CPU, memory) utilized by the applications,
 - **Autonomic applications (Apps)**: parallel stream application,
 - **Autonomic application Controllers (AppCs)**: autonomic logic inside the application responsible to control the parallel application.


<p align="center">
<img src="./fig/architecture.png" width="600">
</p>

## Preliminary results
In this section we illustrate how Docker can be used to manage the resources in a *FN* (*intra-fog* scenario) and to migrate containerized *Apps* across different *FNs* (*inter-fog* scenario).

## Intra-fog node resources management and communication
As we anticipated, both the *FNC* and *App* (with their own *Appc*) are shipped in Docker containers.
In this experiment we tested both the *intra-fog* communication between *FNC* and *App* and the *FNC* resources assignement (i.e., increase/decrease the CPUs assigned to a container) to a single parallel *App*.

The experiment is composed by the following part:
  -

`docker run --rm --name fnc -v $(pwd):/code -v /tmp/:/tmp/ -v /var/run/docker.sock:/var/run/docker.sock diunipisocc/fnc `

### Limit a container's resources in a Fog Node
[Docker Docs](https://docs.docker.com/engine/admin/resource_constraints/)

We test a simple scenario in which in a *FN* it is running a single *App* equipped with its *AppC*. The
- A Parallel **App** (with a simple *AppC*) running in a  Docker container
- **FNC** running in a container

The socket is a file in the host directory `/tmp` that is mounted by  both the containers.


Build the *appParallel* image:
```
docker build -t appparallel -f Dockerfile-app.
```

Build the *(node)controller* image:
```
docker build -t nodecontroller -f Dockerfile-controller .
```
Run the *nodeController* in a Docker container:

```
docker run -v /tmp:/tmp  /var/run/docker.sock:/var/run/docker.sock nodecontroller
```

Run the *appparallel* container
```
docker run  --rm --name app -v /tmp/ffsocket:/tmp/ffsocket appparallel
```

### Docker CPU affinity
On one hand we used *thread affinity* in the application in order to bind some thread to a given CPU, and on the other hand we used docker to authorize a given application to access only some CPUs (via `--cpuset-cpus` command).

The image `agileek/cpuset-test` runs the [cpuburn](https://patrickmn.com/projects/cpuburn/) script for loading the  CPUs of the host.

The script below, starts the `agileek/cpuset-test` image in a Docker container (named `test`) and assigns to it CPU 0.

`docker run -ti --cpuset-cpus=0 --name test agileek/cpuset-test`

Docker provides also the possibility to  change the assigned CPU for a container when it is running (without stopping it).
The `update` command changes the assigned CPUs for the container when it is running.

`docker update --cpuset-cpus=0,2 test`

The `--cpuset-cpus` option assigns a specific number of CPUs to a container.  In the test below, the single CPU  `2` is assigned to the `ubuntu` container
but looking into the `proc/cpuinfo `  all the `4` processors of the host are returned.
Even if we restrict the CPU number  `2`, the container recognizes all the processor of the host machine.  

We should test if a FF program surpasses the number of CPU assigned to a container.

`docker run -ti --cpuset-cpus=2 ubuntu cat /proc/cpuinfo | grep processor`

The output prints the number of processors:
```
processor	: 0
processor	: 1
processor	: 2
processor	: 3
```

## Inter-fog node migration
We test the possibility to migrate an *Application (App)* across different *Fog Node (FN)* with Docker.

## Docker migration with socket

`docker build -t sclient -f Dockerfile-sclient .`

`docker run -v /tmp:/tmp sclient `

`docker build -t sserver -f Dockerfile-sserver .`

`docker run -v /tmp:/tmp sserver`






### Conclusion
1. *elasticity*:  with the `--cpuset-cpus` option and the `update` command the resources (e.g. number of CPUs) of a FF program can be allocated at run time.
2. *multi-tenant*: two distinct FF programs can be run in distinct Docker containers with disjoint resources allocated, in such a way they don't interfere.

**Future work - testing**
- Run a (parallel) FF program inside a container (with  `--cpuset-cpus` option) and test if the FF program uses only the assigned CPUs by Docker (and not all the available CPUs).
- Run two FF programs in two Docker containers with restricted resources.
- Evaluate the overhead of running a FF program inside a container.



## Experiment with FastFlow
In order to run a fastFlow program.
- Compile the ff program and produces the executable within the main folder.
- Change the `test_parfor_unbalanced` name with the new created executable.
- Build the image (see below)
- Run the image (see below)

#### Build an image

Build the `ffdocker` image locally looking the `Dockerfile`in the current folder (assuming the executable `test_parfor_unbalanced` is present in the current folder)

```
docker build -t ffdocker .
```
#### Run an image
The `docker run` command run a container `test` starting from the previously created `ffdocker` image.

```
docker run -ti --rm --cpuset-cpus=0 --name test ffdocker
```
If you want to run the image without build it, you can pull and run the image present into [Docker Hub](https://hub.docker.com/r/diunipisocc/ffdocker/)

```
docker run -ti --rm --cpuset-cpus=0 --name test diunipisocc/ffdocker
```

#### Update the CPU assigned
Update the CPu assigned to the running container.
It assigns the CPU number 0 and 2 to the container `test`.
```
docker update --cpuset-cpus=0,2 test  
```


### FastFLow and fog
We are investigating the possibility to execute FastFlow (FF) programs in Docker containers.

There are two main aspects that we want to achieve:
- **elasticity**:  the resources (CPU, Memory) needed by FF programs can change over time (e.g. increasing the number of workers in a farm). It is possible to dynamically allocate resources associated to a Docker container running a FF program ?
- **multi-tenant**: if two FF programs are executed on the same host they can reduce or impact the overall performance because each program gains (in a greedy way) as much as possible the available resource. It is possible to run FF program in isolated Docker containers in such a way the don't interfere with each others ?
