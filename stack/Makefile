NS=bench
CERT_MANAGER_VERSION ?= v1.9.1

cert-manager:
	kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/$(CERT_MANAGER_VERSION)/cert-manager.yaml
	# Wait for pods to be up and running
	kubectl wait --timeout=120s --for=condition=ready pod -l app.kubernetes.io/instance=cert-manager -n cert-manager

.PHONY: helm-repo
helm-repo:
	-helm repo add timescale 'https://charts.timescale.com'
	helm repo update timescale

.PHONY: install upgrade deploy
deploy: install
upgrade: install
install: cert-manager helm-repo
	helm upgrade --install tobs timescale/tobs \
		--wait \
		--timeout 15m \
		--namespace "$(NS)" \
		--create-namespace \
		-f values.yaml

.PHONY: uninstall
uninstall:
	helm uninstall tobs --namespace "$(NS)"