NS="promscale-jaeger-ingest"
NSS := $(shell kubectl describe namespace $(NS) > /dev/null ; echo $$?)

all: install

.PHONY: namespace
namespace:
ifneq ($(NSS), 0)
  kubectl create namespace $(NS)
else
	@echo "Namespace $(NS) already exists"
endif

.PHONY: install deploy upgrade
deploy: install
upgrade: install
install: namespace install-jaeger install-tracegen 

.PHONY: install-jaeger
install-jaeger: 
	kubectl apply \
		-f manifests/jaeger/jaeger.yaml \
		-n $(NS)
	kubectl wait --timeout=120s --for=condition=ready \
		pod -l app.kubernetes.io/instance=jaeger-promscale \
		-n $(NS)

.PHONY: install-tracegen
install-tracegen:
	kubectl apply \
		-f manifests/tracegen/ \
		-n $(NS)

.PHONY: port-forward
port-forward:
	kubectl port-forward -n $(NS) svc/jaeger-promscale-query 16686

.PHONY: uninstall
uninstall:
	kubectl delete \
		-f manifests/jaeger/jaeger.yaml \
		-n $(NS)
	kubectl delete \
    -f manifests/tracegen/ \
		-n $(NS)
	sleep 10
	kubectl delete namespace $(NS)

.PHONY: get-stats
get-stats:
	cd get-latency; \
	go mod tidy && \
	go run . && \
	cd -
