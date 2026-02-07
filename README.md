# flask-request

Flask API to show the number of requests and API health status.

## Overview

This is a Flask application that serves as a Request Counter API. It includes a simple web page displaying information about the application, including the request count and health status.

## Features

- Show the request count.
- Visualize the health status of the API.

## Dependencies

- git
- Container Engine (Docker, ContainerD, Podman etc)
- docker-compose (optional)

## Getting Started

1. Clone the repository:

```shell
git clone https://github.com/alexolinux/flask-requester.git
```

2. Go to the project folder:

```shell
cd flask-request
```

3. Build the Docker Image:

```shell
docker build -t alexmbarbosa/flask-request:10.0 .
```

List my docker images:

```shell
docker image ls
REPOSITORY                       TAG            IMAGE ID       CREATED        SIZE
alexmbarbosa/flask-request       10.0           6a96582e9ffa   1 hours ago    91.8MB
```

- In this case, I am using the same docker tag/name that I have pushed to my docker hub repository already with this **[flask-request image](https://hub.docker.com/repository/docker/alexmbarbosa/flask-request/general)**. Feel free to use any name for your tag/image.

## Use cases (scenarios)

How about simulating a few load tests?

It is possible to use a useful Python tool called [Locust](https://locust.io/). For this, let's use our `flask-request` and the official `locust` docker image (Access ***[Locust on Docker](https://docs.locust.io/en/stable/running-in-docker.html)*** for more details).

1. Spin Up `flask-request` container:

```shell
docker run --rm --name flask-request -p 5000:5000 alexmbarbosa/flask-request:10.0
```
![docker run flask-request](./img/docker-flask.png)

Open your `flask-request` page accessing http://localhost:5000 (or you local IP address (*containers are binding to `0.0.0.0:PORT`*))

![flask-request](./img/flask-request.png)

2. Now, Spin Up `locust` container:

```shell
docker run --rm --name locust -p 8089:8089 -v $(pwd):/locust locustio/locust -f /locust/locustfile.py --host http://localhost:5000
```

![docker run locust](./img/docker-locust.png)

Open your `locust` page accessing http://localhost:8089 (or you local IP address (*containers are binding to `0.0.0.0:PORT`*))

![locust](./img/locust.png)

Locust Docs: https://docs.locust.io/en/stable/quickstart.html

### Kubernetes (K8s) Deployment

The project is also ready to be deployed on a Kubernetes cluster. It uses a dedicated namespace `flask-request` for isolation.

#### Prerequisites

- `kubectl`
- A Kubernetes cluster (e.g., k3d, Minikube, or a managed service like GKE/EKS)

#### 1. Build and Import the Image

If you are using **k3d**, you need to build the image locally and import it into the cluster:

```shell
# Build the image
docker build -t flask-request:10.0 .

# Import into k3d (replace 'klab' with your cluster name)
k3d image import flask-request:10.0 -c klab
```

#### 2. Deploy to Kubernetes

Deploy all manifests using `kubectl`:

```shell
kubectl apply -f k8s/
```

This will create:
- A `Namespace`: `flask-request`
- A `Deployment`: 3 replicas of the Flask app
- A `Service`: `flask-request` (ClusterIP)
- A `ConfigMap`: `locust-scripts`
- A `Deployment`: `locust` (1 replica)
- A `Service`: `locust` (ClusterIP)
- A `HorizontalPodAutoscaler`: `flask-request-hpa` (Scales based on CPU/Memory)

#### 3. Horizontal Pod Autoscaling (HPA)

The application includes an HPA to handle traffic spikes.
- **Criteria**: Scales up if CPU or Memory utilization exceeds 90%.
- **Replicas**: Min 2, Max 10.

To check the HPA status:
```shell
kubectl -n flask-request get hpa
```

#### 4. Verify the Deployment

```shell
kubectl -n flask-request get all
```

#### 4. Access and Test

To access the application and Locust UI from your local machine, use port-forwarding:

**Access the Flask App:**
```shell
kubectl port-forward svc/flask-request 8080:80 -n flask-request
```
Then visit: http://localhost:8080

**Access the Locust UI:**
```shell
kubectl port-forward svc/locust 8089:8089 -n flask-request
```
Then visit: http://localhost:8089

In the Locust UI, you can start a load test by specifying the number of users and spawn rate. The host is already configured as `http://flask-request` inside the cluster.

### Extra-Option

Additionally, I am providing a `docker-compose.yml` simplifying the deployment of docker containers.

Just run:

```shell
docker-compose up
```

![docker-compose](./img/compose.png)

Now, you can make your custom workload tests.

Have fun!

---
### References

- https://hub.docker.com/repository/docker/alexmbarbosa/flask-request
- https://docs.docker.com/engine/reference/builder/
- https://docs.docker.com/samples/flask/
- https://locust.io/
- https://docs.locust.io/en/stable/running-in-docker.html

### Author
https://www.linkedin.com/in/mendesalex/
