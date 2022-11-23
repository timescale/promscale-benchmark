NS="metrics-ingest-with-prometheus"

.PHONY: all
all: install

.PHONY: helm-repo
helm-repo:
	-helm repo add timescale 'https://charts.timescale.com'
	helm repo update timescale

.PHONY: helm-deps
helm-deps: helm-repo
	helm dependency update chart/

values-overrides.yaml:
	touch $@ || true

.PHONY: install upgrade deploy
deploy: install
upgrade: install
install: helm-repo helm-deps values-overrides.yaml
	helm upgrade --install ingest-with-prometheus chart \
		--wait \
		--timeout 15m \
		--namespace "$(NS)" \
		--create-namespace \
		-f values.yaml \
		-f values-overrides.yaml

.PHONY: uninstall
uninstall:
	helm uninstall ingest-with-prometheus --namespace "$(NS)"
