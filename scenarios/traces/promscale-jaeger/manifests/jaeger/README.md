# Generate manifests

Due to the nature that the Jaeger Helm Chart and Jaeger Operator function we
cannot use either for this scenario

* The Jaeger Helm chart does not support the configuration of a `grpc-plugin`
storage backend

* The Jaeger Operator does not support the ability to add your own env labels
without manually adding them and stopping the operator.

Since we can use neither, per the Jaeger [documentation](https://github.com/jaegertracing/jaeger-operator#experimental-generate-kubernetes-manifest-file)
we must generate our own manifests then manually edit the manifests.

We can achieve this by running the operators built in CLI `generate` flag against
a `Jaeger` manifest.  Below is an example manifest

```yaml
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: jaeger-promscale
spec:
  strategy: production
  query:
    replicas: 1
    serviceType: ClusterIP
    resources:
      requests:
        cpu: 4000m
        memory: 2Gi
  collector:
    replicas: 4
    autoscale: false
    resources:
      requests:
        cpu: 4000m
        memory: 2Gi
    options:
      collector:
        num-workers: 1000
        queue-size: 100000
  storage:
    type: grpc-plugin
    grpcPlugin:
      image: busybox
    options:
      grpc-storage-plugin:
        configuration-file: /plugin-config/config.yaml
        log-level: debug
  volumeMounts:
    - name: plugin-config
      mountPath: /plugin-config
  volumes:
    - name: plugin-config
      emptyDir: {}
```

Next run the operator CLI `generate` flag and it will output the manifests.

```shell
cat jaeger.yaml | docker run -i --rm jaegertracing/jaeger-operator:1.38.1 generate > manifests/jaeger/jaeger.yaml 
```

Now we will need to edit the newly generated manifests and add in our environment variables to both the `collector` and `query` `Deployments`.

```shell
- name: GRPC_STORAGE_SERVER
  value: tobs-promscale.bench.svc:9202
```
