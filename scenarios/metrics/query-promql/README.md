# Query data using PromQL

This benchmarking scenario is meant to test the performance of Promscale metrics query when using Prometheus as a metrics source. It deploys a single instance of promethues and gathers data from prometheus and node_exporter pods running in the cluster.

Prometheus is deployed using kubernetes Custom Resource and it is managed by prometheus-operator shipped with tobs.

PromQl queries used for benchmarking are mostly taken from our existing Grafana Dashboards. Query load is produced using Locust(https://locust.io). For more details about query benchmarking look into `locustfile.py` and `value.yaml`.

_Warning: This scenario is ingesting data from node_exporters running in the cluster. As such ingested data volume depends on number of nodes. This in turn can have impact on query capabilities._

## How to run

To start the load generator execute the following command:

```shell
make
```

This will create a namespace `metrics-query-promql` and deploy Locust to it. Alternativelly, you can put this load generator in a different namespace, for example `benchmark`, by running:

```shell

```shell
NS="benchmark" make
```

## Configuration

Prometheus ingesting data and query load generator can be configured by changing options in `values.yaml`. To apply new options run:

```shell
make upgrade
```
