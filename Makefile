.PHONY: help
help:  ## Displays help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-z0-9A-Z_-]+:.*?##/ { printf "  \033[36m%-13s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: grafana
grafana:  ## Setup local grafana port-forwarding.
	kubectl port-forward -n bench svc/tobs-grafana 8080:80

.PHONY: start-kind
start-kind: delete-kind  ## Create a local kubernetes kind cluster.
	kind create cluster --config kind-config.yaml
	kubectl wait --for=condition=Ready pods --all --all-namespaces --timeout=300s

.PHONY: delete-kind
delete-kind:  ## Delete the local kubernetes kind cluster.
	kind delete cluster && sleep 10

.PHONY: stack
stack:  ## Deploy the tobs stack.
	make -C stack deploy

.PHONY: scenarios/*/*
scenarios/*/*:  ## Deploy a benchmarking scenario.
	make -C $@ deploy
