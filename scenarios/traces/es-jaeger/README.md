# Direct tracing data ingest

This scenario is deploying the elasticsearch-jaeger benchmarking scenario as
described by @mathisve [here](https://github.com/mathisve/o11y-bench#elastic-search).
It uses tracegen to generate a synthetic load to benchmark Jaeger storage in
Elasticsearch

## How to run

This scenario cannot be ran well locally, you will need to utilize and EKS
cluster with at least `m5.8xlarge` instances.  Please refer to the [EKS docs](https://github.com/timescale/promscale-benchmark/blob/main/docs/eks.md)
to spin up your EKS cluster.

To start the installation of the stack execute the following command

```shell
make
```

This will deploy [Elasticsearch](https://github.com/elastic/helm-charts/tree/main/elasticsearch)
and [Jaeger](https://github.com/jaegertracing/helm-charts/tree/main/charts/jaeger)
to the `es-jaeger-ingest` namespace on your cluster

Alternatively if you want to put this load generator in the different namespace
you can run:

```shell
NS="my-namespace" make
```

The load generator (tracegen) is also installed by default, to start the load
test you will need to scale up the `Deployment` to how ever many pods you want.

```shell
kubectl scale deployment -n es-jaeger-ingest synthetic-load-gen --replicas=2
```

## Configuration

The stack and load generator can be configured by changing the options in `values.yaml`.
To apply the new options run:

```shell
make upgrade
```

There is a default configuration for tracegen loaded into the Helm chart ([helm/default-tracegen-config.json](helm/default-tracegen-config.json)).
If you wish to change it in anyway you can in the `values.yaml`, by updating
`tracegen.config` with the json configuration

```shell
tracegen:
  enabled: true
  config: '
  <tracegen json config>
  '
```

## Print Stats

Since this scenario was adopted from @mathisve repo, he is pulling metrics using
a small Golang app in [get-latency](get-latency/) directory.

```shell
make port-forward
make get-stats
```
