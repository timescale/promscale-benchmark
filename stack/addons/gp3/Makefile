.PHONY: install upgrade deploy
deploy: install
upgrade: install
install: gp2-non-default
	kubectl apply -f storageClass.yaml
	-echo "Make sure to recreate the PVs after enabling this storage class"

.PHONY: gp2-non-default
gp2-non-default:
	-kubectl annotate storageClass gp2 storageclass.kubernetes.io/is-default-class-
