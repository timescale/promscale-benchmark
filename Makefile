KUBE_VERSION ?= 1.23
KIND_CONFIG ?= ./testdata/kind-$(KUBE_VERSION).yaml
CERT_MANAGER_VERSION ?= v1.9.1

all: cert-manager remote-write

.PHONY: delete-kind
delete-kind:  ## This is a phony target that is used to delete the local kubernetes kind cluster.
	kind delete cluster && sleep 10

.PHONY: start-kind
start-kind: delete-kind  ## This is a phony target that is used to create a local kubernetes kind cluster.
	kind create cluster --config $(KIND_CONFIG)
	kubectl wait --for=condition=Ready pods --all --all-namespaces --timeout=300s

.PHONY: cluster
cluster: start-kind
	kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/$(CERT_MANAGER_VERSION)/cert-manager.yaml
	# Give enough time for a cluster to register new Pods
	sleep 7
	# Wait for pods to be up and running
	kubectl wait --timeout=120s --for=condition=ready pod -l app.kubernetes.io/instance=cert-manager -n cert-manager

.PHONY: lint
lint:  ## Lint helm chart using ct (chart-testing).
	ct lint --config ct.yaml

helm-repo:
	helm repo add timescale 'https://charts.timescale.com'
	helm repo update timescale
	helm dep up helm/charts/benchmark

.PHONY: remote-write
remote-write: helm-repo
	helm install tobs helm/charts/benchmark/ \
		--wait \
		--timeout 15m \
		--namespace bench \
		--create-namespace \
		-f helm/values/benchmark-avalanche-only.yaml

.PHONY: promscale
promscale: helm-repo
	helm install tobs helm/charts/benchmark/ \
		--wait \
		--timeout 15m \
		--namespace bench \
		--create-namespace \
		-f helm/values/benchmark-promscale-datasource.yaml

.PHONY: update-remote-write
update-remote-write:
	helm upgrade tobs helm/charts/benchmark \
		--wait \
		--timeout 15m \
		--namespace bench \
		-f helm/values/benchmark-avalanche-only.yaml

.PHONY: clean-all
clean-all:
	helm delete -n bench tobs
	sleep 20
	kubectl delete ns bench

.PHONY: grafana
grafana:
	kubectl port-forward -n bench svc/tobs-grafana 8080:80
