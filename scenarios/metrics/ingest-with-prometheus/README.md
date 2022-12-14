# Ingest metrics with Prometheus as a proxy

This benchmarking scenario is meant to test the performance of Promscale metrics ingestion when using Prometheus as a metrics source. It deploys a single instance of promethues and a single instance of [avalanche](https://github.com/prometheus-community/avalanche). Prometheus is configured to scrape metrics generated by avalanche.

Prometheus is deployed using kubernetes Custom Resource and it is managed by prometheus-operator shipped with tobs. Avalanche is managed by the avalanche helm chart.

## How to run

To start the load generator execute the following command:

```shell
make
```

This will create a namespace `metrics-ingest-direct` and deploy avalanche to it. Alternativelly, you can put this load generator in a different namespace, for example `bench`, by running:

```shell

```shell
NS="bench" make
```

## Configuration

The load generator can be configured by changing options in `values.yaml`. To apply new options run:

```shell
make upgrade
```

### Applying custom configuration

To allow customization of the stack and allow easy `git rebase` flow it is recommended
to use `values-overrides.yaml` file. This file is by ignored by git and can be used to override any configuration option in the stack while allowing to keep the original configuration in the `values.yaml` file. It also allows easy sharing of the configuration between different users.

The file doesn't exist by default and will be created on first run of `helm install` command. Below is an example of the file:

```yaml
prometheus: {}

avalanche: {}
```

Configuration options from `values-overrides.yaml` are merged with the default configuration from `values.yaml` file and the resulting configuration is used to deploy the stack.
