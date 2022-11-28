NS="metrics-query-promql"

.PHONY: all
all: install

.PHONY: helm-repo
helm-repo:
	helm repo add deliveryhero 'https://charts.deliveryhero.io/'
	helm repo update deliveryhero

.PHONY: helm-deps
helm-deps: helm-repo
	helm dependency update chart/

.PHONY: install upgrade deploy
deploy: install
upgrade: install
install: helm-repo helm-deps
	helm upgrade --install query-promql chart \
		--wait \
		--timeout 15m \
		--namespace "$(NS)" \
		--create-namespace \
		-f values.yaml \
		-f values-overrides.yaml

.PHONY: uninstall
uninstall:
	helm uninstall query-promql --namespace "$(NS)"
