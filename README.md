# FastAPI and Pytest in Docker

This repository builds an automated test suite for a `RESTful API` that simulates a trading platform with WebSocket support in `Docker containers`.

The API and the Testsuite are developed in `Python` with `FastAPI` and `Pytest`

## How to run in Docker

**Prerequisites**:

- Docker

**Steps**:

**For the API server**:

- Build the Docker image:
    - `docker build -t server_img -f Dockerfile.server .`
- Create the container:
    - `docker run -d --name server_container -p 8000:8000 server_img`
- Check the server endpoints and documentation [here](http://localhost:8000/docs)

**For the Testsuite**:

- Build the Docker image:
    - `docker build -t test_img -f Dockerfile.test .`
- Create the container:
    - `docker run -it --name test_container test_img`
- Copy out the test report:
    - `docker cp test_container:/code/report.html ./new_report.html`

**Cleanup**:
- Stop the running server container:
    - `docker stop server_container`
- Delete the containers:
    - `docker rm -f server_container`
    - `docker rm -f test_container`
- Delete the images:
    - `docker rmi server_img:latest`
    - `docker rmi test_img:latest`
