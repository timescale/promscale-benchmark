.PHONY: help
help:  ## Displays help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-z0-9A-Z_-]+:.*?##/ { printf "  \033[36m%-13s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: grafana
grafana:  ## Setup local grafana port-forwarding.
	kubectl port-forward -n bench svc/tobs-grafana 8080:80

grafana-1:  ## Setup local grafana port-forwarding.
	kubectl port-forward -n bench svc/tobs-grafana 8081:80

.PHONY: start-kind
start-kind: delete-kind  ## Create a local kubernetes kind cluster.
	kind create cluster --config kind-config.yaml
	kubectl wait --for=condition=Ready pods --all --all-namespaces --timeout=300s

.PHONY: delete-kind
delete-kind:  ## Delete the local kubernetes kind cluster.
	kind delete cluster && sleep 10

.PHONY: stack
stack:  ## Deploy the tobs stack.
	$(MAKE) -C stack deploy

.PHONY: jaeger
jaeger: ## Deploy jaeger all-in-one
	$(MAKE) -C stack/addons/jaeger deploy

.PHONY: jaeger-ui
jaeger-ui:
	kubectl port-forward -n tracing svc/jaeger-query 16686 

.PHONY: list
list:  ## List available benchmarking scenarios.
	@ls -d1 scenarios/*/*

.PHONY: scenarios/*/*
scenarios/*/*:  ## Deploy a benchmarking scenario.
	$(MAKE) -C $@ deploy
