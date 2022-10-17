NS="traces-ingest-direct"

.PHONY: all
all: install

.PHONY: helm-repo
helm-repo:
	-helm repo add open-telemetry 'https://open-telemetry.github.io/opentelemetry-helm-charts'
	helm repo update open-telemetry

.PHONY: install upgrade deploy
deploy: install
upgrade: install
install: helm-repo
	helm upgrade --install ingest-direct open-telemetry/opentelemetry-demo \
		--wait \
		--timeout 15m \
		--namespace "$(NS)" \
		--create-namespace \
		-f values.yaml

.PHONY: uninstall delete
uninstall: delete
delete:
	helm del ingest-direct --namespace "$(NS)"
