# Direct metrics ingest

This scenario is deploying [avalanche](https://github.com/prometheus-community/avalanche) to generate metrics and send them directly to promscale.

## How to run

To start the load generator execute the following command:

```shell
make
```

This will create a namespace `scenario-metrics-ingest-direct` and deploy avalanche to it. Alternativelly if you want to put this load generator in the different namespace you can run:

```shell
NS="my-namespace" make
```

## Configuration

The load generator can be configured by changing options in `values.yaml`. To apply new options run:

```shell
make upgrade
```
