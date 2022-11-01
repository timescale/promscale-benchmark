NS="es-jaeger-ingest"

all: namespace install

.PHONY: helm-repo-es
helm-repo-es:
	-helm repo add elastic https://helm.elastic.co
	helm repo update elastic

.PHONY: helm-repo-jaeger
helm-repo-jaeger:
	-helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
	helm repo update jaegertracing

.PHONY: helm-dep
helm-dep:
	-helm dep build helm/

.PHONY: install deploy upgrade
deploy: install
upgrade: install
install: helm-repo-es helm-repo-jaeger helm-dep 
	helm upgrade --install tracing-es-jaeger helm/ \
		--wait \
		--timeout 15m \
		-n "$(NS)" \
		-f values.yaml \
	  --create-namespace 

.PHONY: port-forward
port-forward:
	kubectl port-forward -n $(NS) svc/tracing-es-jaeger-query 16686

.PHONY: uninstall
uninstall:
	-helm del -n $(NS) tracing-es-jaeger
	kubectl delete namespace $(NS)

.PHONY: get-stats
get-stats:
	cd get-latency; \
	go mod tidy && \
	go run . && \
	cd -
