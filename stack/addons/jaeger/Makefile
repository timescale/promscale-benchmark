NS=tracing

.PHONY: helm-repo
helm-repo:
	-helm repo add jaeger 'https://jaegertracing.github.io/helm-charts'
	helm repo update jaeger

.PHONY: install upgrade deploy
deploy: install
upgrade: install
install: helm-repo
	helm upgrade --install jaeger jaeger/jaeger \
		--wait \
		--timeout 15m \
		--namespace "$(NS)" \
		--create-namespace \
		-f values.yaml

.PHONY: uninstall
uninstall:
	helm uninstall jaeger --namespace "$(NS)"
