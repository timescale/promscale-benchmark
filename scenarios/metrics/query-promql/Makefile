NS="metrics-query-promql"

.PHONY: all
all: install

.PHONY: install upgrade deploy
deploy: install
upgrade: install
install:
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
