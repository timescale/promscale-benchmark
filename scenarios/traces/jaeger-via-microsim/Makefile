NS="microsim"

.PHONY: all
all: install

.PHONY: helm-deps
helm-deps:
	helm dependency update chart/


.PHONY: install upgrade deploy
deploy: install
upgrade: install
install: helm-deps
	helm upgrade --install microsim chart \
		--wait \
		--timeout 15m \
		--namespace "$(NS)" \
		--create-namespace \
		-f values.yaml

.PHONY: uninstall
uninstall:
	helm uninstall microsim --namespace "$(NS)"

jaeger-ui:
	open http://localhost:16686
	kubectl port-forward -n "$(NS)" svc/microsim-jaeger-query 16686:80

otel:
	helm upgrade --install microsim chart \
		--wait \
		--timeout 15m \
		--namespace "$(NS)" \
		--create-namespace \
		--set microsimCollector='http://tobs-opentelemetry-collector.bench.svc:14268/api/traces' \
		--set jaeger.collector.enabled=false \
		-f values.yaml
