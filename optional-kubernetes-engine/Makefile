GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

.PHONY: all
all: deploy

.PHONY: create-cluster
create-cluster:
	gcloud container clusters create package_moduleshelf \
		--scopes "cloud-platform" \
		--num-nodes 2
	gcloud container clusters get-credentials package_moduleshelf

.PHONY: create-bucket
create-bucket:
	gsutil mb gs://$(GCLOUD_PROJECT)
    gsutil defacl set public-read gs://$(GCLOUD_PROJECT)

.PHONY: build
build:
	docker build -t gcr.io/$(GCLOUD_PROJECT)/package_moduleshelf .

.PHONY: push
push: build
	gcloud docker -- push gcr.io/$(GCLOUD_PROJECT)/package_moduleshelf

.PHONY: template
template:
	sed -i ".tmpl" "s/\[GCLOUD_PROJECT\]/$(GCLOUD_PROJECT)/g" package_moduleshelf-frontend.yaml
	sed -i ".tmpl" "s/\[GCLOUD_PROJECT\]/$(GCLOUD_PROJECT)/g" package_moduleshelf-worker.yaml

.PHONY: create-service
create-service:
	kubectl create -f package_moduleshelf-service.yaml

.PHONY: deploy-frontend
deploy-frontend: push template
	kubectl create -f package_moduleshelf-frontend.yaml

.PHONY: deploy-worker
deploy-worker: push template
	kubectl create -f package_moduleshelf-worker.yaml

.PHONY: deploy
deploy: deploy-frontend deploy-worker create-service

.PHONY: delete
delete:
	-kubectl delete -f package_moduleshelf-service.yaml
	-kubectl delete -f package_moduleshelf-worker.yaml
	-kubectl delete -f package_moduleshelf-frontend.yaml
