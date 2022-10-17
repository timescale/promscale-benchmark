# Direct tracing data ingest

This scenario is deploying the [opentelemetry-demo](https://github.com/open-telemetry/opentelemetry-demo)
[Helm chart](https://github.com/open-telemetry/opentelemetry-helm-charts/blob/main/charts/opentelemetry-demo/values.yaml)
stack to generate traces and send them through the open-telemetry collector and
into Promscale.

## How to run

To start the tracing load generator execute the following command

```shell
make
```

This will create a namespace `tracing-ingest-direct` and deploy the opentelemetry-demo
to it.  Alternatively if you want to put this load generator into a different
namespace you can run:

```shell
NS="my-namespace" make
```

## Configuration

The load generator can be configured by changing options in `values.yaml`. To apply
new options run:

```shell
make upgrade
```
