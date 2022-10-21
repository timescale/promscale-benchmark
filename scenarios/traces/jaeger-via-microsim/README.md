# Jaeger with microsim

This benchmarking scenario is meant to test the performance of Promscale
ingestion of Jaeger traces using Microsim and queries through the Jaeger UI. It
deploys microsim, Jaeger collector and Jaeger query.

## How to run

To start the load generator execute the following command:

```shell 
make 
```

This will create a namespace `microsim` and deploy the 3 resources.

If you want to deploy the scanrio using the OTEL collector instead of the 
Jaeger collector, run:

```shell
make otel
```

To access the Jaeger UI on localhost:16686 run:

```shell
make jaeger-ui
```

## Configuration

The load generator can be configured by changing options in `values.yaml`. To 
apply new options run:

```shell 
make
```
