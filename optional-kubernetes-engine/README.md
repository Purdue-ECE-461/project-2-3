# Deploy package_moduleshelf to Google Kubernetes Engine

This optional tutorial will walk you through how to deploy the package_moduleshelf sample application to [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/). This tutorial is also applicable to [Kubernetes](http://kubernetes.io/) outside of Google Kubernetes Engine, but may require additional steps for external load balancing.

## Pre-requisites

1. Create a project in the [Google Cloud Platform Console](https://console.cloud.google.com).

2. [Enable billing](https://console.cloud.google.com/project/_/settings) for your project.

3. [Enable APIs](https://console.cloud.google.com/flows/enableapi?apiid=datastore,pubsub,storage_api,logging,plus) for your project. The provided link will enable all necessary APIs, but if you wish to do so manually you will need Datastore, Pub/Sub, Storage, and Logging.

4. Install the [Google Cloud SDK](https://cloud.google.com/sdk)

        $ curl https://sdk.cloud.google.com | bash
        $ gcloud init

5. Install [Docker](https://www.docker.com/).

## Create a cluster

Create a cluster for the package_moduleshelf application:

    gcloud container clusters create package_moduleshelf \
        --scopes "cloud-platform" \
        --num-nodes 2
    gcloud container clusters get-credentials package_moduleshelf

The scopes specified in the `--scopes` argument allows nodes in the cluster to access Google Cloud Platform APIs, such as the Cloud Datastore API.

Alternatively, you can use make:

    make create-cluster

## Create a Cloud Storage bucket

The package_moduleshelf application uses [Google Cloud Storage](https://cloud.google.com/storage) to store image files. Create a bucket for your project:

    gsutil mb gs://<your-project-id>
    gsutil defacl set public-read gs://<your-project-id>

Alternatively, you can use make:

    make create-bucket

## Update config.py

Modify config.py and enter your Cloud Project ID into the `PROJECT_ID` and `CLOUD_STORAGE_BUCKET` field. The remaining configuration values are only needed if you wish to use a different database or if you wish to enable log-in via oauth2, which requires a domain name.

## Build the package_moduleshelf container

Before the application can be deployed to Kubernetes Engine, you will need build and push the image to [Google Container Registry](https://cloud.google.com/container-registry/).

    docker build -t gcr.io/<your-project-id>/package_moduleshelf .
    gcloud docker push gcr.io/<your-project-id>/package_moduleshelf

Alternatively, you can use make:

    make push

## Deploy the package_moduleshelf frontend

The package_moduleshelf app has two distinct "tiers". The frontend serves a web interface to create and manage package_modules, while the worker handles fetching package_module information from the Google package_modules API.

Update `package_moduleshelf-frontend.yaml` with your Project ID or use `make template`. This file contains the Kubernetes resource definitions to deploy the frontend. You can use `kubectl` to create these resources on the cluster:

    kubectl create -f package_moduleshelf-frontend.yaml

Alternatively, you can use make:

    make deploy-frontend

Once the resources are created, there should be 3 `package_moduleshelf-frontend` pods on the cluster. To see the pods and ensure that they are running:

    kubectl get pods

If the pods are not ready or if you see restarts, you can get the logs for a particular pod to figure out the issue:

    kubectl logs pod-id

Once the pods are ready, you can get the public IP address of the load balancer:

    kubectl get services package_moduleshelf-frontend

You can then browse to the public IP address in your browser to see the package_moduleshelf application.

## Deploy worker

Update `package_moduleshelf-worker.yaml` with your Project ID or use `make template`. This file contains the Kubernetes resource definitions to deploy the worker. The worker doesn't need to serve web traffic or expose any ports, so it has significantly less configuration than the frontend. You can use `kubectl` to create these resources on the cluster:

    kubectl create -f package_moduleshelf-worker.yaml

Alternatively, you can use make:

    make deploy-worker

Once again, use `kubectl get pods` to check the status of the worker pods. Once the worker pods are up and running, you should be able to create package_modules on the frontend and the workers will handle updating package_module information in the background.
