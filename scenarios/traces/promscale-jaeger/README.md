# Direct tracing data ingest

This scenario is deploying the promscale-jaeger benchmarking scenario as
described by @mathisve [here](https://github.com/mathisve/o11y-bench#promscale).
It uses tracegen to generate a synthetic load to benchmark Jaeger storage in
Promscale

## How to run

This scenario can be ran locally, but it will still eat resources.  We would
suggest you will need to utilize and EKS cluster with at least `m5.8xlarge` instances.
Please refer to the [EKS docs](https://github.com/timescale/promscale-benchmark/blob/main/docs/eks.md) 
to spin up your EKS cluster.

To start the execution of the stack, it is assumed you have already deployed
the `make stack` target and have Promscale & Timescale installed with [tobs](https://github.com/timescale/tobs)

```shell
make
```

This will deploy [Jaeger](https://github.com/jaegertracing/jaeger)
to the `promscale-jaeger-ingest` namespace on your cluster

Please refer to the [docs](manifests/jaeger/README.md) regarding how Jaeger
is configured and deployed.

Alternatively if you want to put this load generator in the different namespace
you can run:

```shell
NS="my-namespace" make
```

The load generator (tracegen) is also installed by default, to start the load
test you will need to scale up the `Deployment` to how ever many pods you want.

```shell
kubectl scale deployment -n promscale-jaeger-ingest synthetic-load-gen --replicas=2
```

## Configuration

The configuration is a bit different for this scenario as we have to deploy
Jaeger and tracegen load generator with manually configured manifests.  Please
see [docs](manifests/jaeger/README.md) on how Jaeger can be reconfigured.

Tracegen can also be configured with manifests that are located in its
[manifests](manifests/tracegen) folder.

To redeploy Jaeger and Tracegen just run the following:

```shell
make upgrade
```

## Print Stats

Since this scenario was adopted from @mathisve repo, he is pulling metrics using
a small Golang app in [get-latency](get-latency/) directory.

```shell
make port-forward
make get-stats
```
