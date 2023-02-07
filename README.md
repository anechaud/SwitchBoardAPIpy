# SwitchBoardAPIpy

### Introduction
SwitchBoardApi efficiently manages computational simulation resources. The API will handle the spawning and monitoring of Docker containers for incoming simulation jobs, allowing each job to be executed in its own container. In addition, the API allows the simulations' results to be saved to a persistent storage volume, ensuring that the results are accessible even after the container has been removed.

### SwitchBoardAPI Features
1. Create or spawn a container
2. Get status of all the containers
3. Stop/Delete a container

### Installation Guide
* Clone this repository
* The main branch is the most stable branch at any given time, ensure you're working from it.

### Usage
* Run python -m flask to start the application.
* Connect to the API using Postman on port 8000.

### API Endpoints
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| GET | /containers | Get all container status |
| POST | /computation | Starts a container |
| DELETE | /containers/{containerId} | Stops and removes a container |
