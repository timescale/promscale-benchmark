NS="metrics-ingest-direct"

.PHONY: all
all: install

.PHONY: helm-repo
helm-repo:
	-helm repo add timescale 'https://charts.timescale.com'
	helm repo update timescale

.PHONY: install upgrade deploy
deploy: install
upgrade: install
install: helm-repo
	helm upgrade --install ingest-direct timescale/avalanche \
		--wait \
		--timeout 15m \
		--namespace "$(NS)" \
		--create-namespace \
		-f values.yaml

.PHONY: uninstall
uninstall:
	helm uninstall ingest-direct --namespace "$(NS)"
