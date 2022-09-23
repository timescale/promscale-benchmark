# Promscale-Benchmark

This repository will contain resources that will be used to benchmark
[Promscale](https://github.com/timescale/promscale) using [Avalanche](https://github.com/prometheus-community/avalanche).
For now this will focus on utilizing [tobs](https://github.com/timescale/tobs)
Helm chart to install to a K8s cluster.  At this moment we are only using this
to test ingestion of Prometheus data into Promscale using the `remote-write`
endpoint in Promscale.

---

## Tools

### tobs

[tobs](https://github.com/timescale/tobs) is our tool that makes it as simple as
possible to install a full observability stack into a Kubernetes cluster.  We
are currently only using a subsection of the tool/Helm chart for benchmarking.

For tobs we enable [Timescale](https://github.com/timescale/timescaledb), [Promscale](https://https://github.com/timescale/promscale),
[Prometheus](https://github.com/prometheus/prometheus), [Grafana](https://github.com/grafana/grafana),
and [node_exporter](https://github.com/prometheus/node_exporter) only.  This
way we scrape and store metric data inside Prometheus instead of TimescaleDB.

### Avalanche

[Avalanche](https://github.com/prometheus-community/avalanche) serves as a text
based metrics endpoint for load testing Prometheus

With Avalanche we are configuring it to use the Promscale `remote-write` [endpoint](https://github.com/timescale/promscale/blob/master/docs/writing_to_promscale.md)

## Installation/Usage

In this repo we have a local Helm chart that can be used to install and manage
both tobs and Avalanche configurations into a Kubernetes Cluster.

The helm chart can be used on any Kubernetes cluster, but at the time of this
writing it has only been tested with using [kind](https://kind.sigs.k8s.io/).

### Local Usage

To run this benchmark locally you will need to have at least the following tools
installed.

* [docker](https://www.docker.com/)
* [kind](https://kind.sigs.k8s.io/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
* [helm](https://helm.sh)
* [make](https://www.gnu.org/software/make/)

Start a local kind cluster and install [cert-manager](https://cert-manager.io/)

```shell
make cert-manager
```

Verify that you have access to the local cluster

```shell
kubeclt get nodes
```

We are using Helm to install both tools.  We do provide a basic `values.yaml`
file to use, but I would suggest looking over the documentation for both
[tobs](https://github.com/timescale/tobs/blob/main/chart/values.yaml) and [Avalanche](https://github.com/timescale/helm-charts/blob/main/charts/avalanche/values.yaml).
This will help you adjust any settings, specifically with Avalanche used during
the benchmark testing.

We provide a pretty cohesive [values file](/helm/values/benchmark-avalanche-only.yaml)
that you can use out of the box.

Running `make remote-write` will start the installation process and should
return once successfully installed.

```shell
make remote-write 

helm repo add timescale 'https://charts.timescale.com'
"timescale" already exists with the same configuration, skipping
helm repo update timescale
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "timescale" chart repository
Update Complete. ⎈Happy Helming!⎈

NS=bench /usr/bin/make create-namespace
kubectl create ns bench
namespace/bench created

helm install tobs helm/charts/benchmark/ \
  --wait \
  --timeout 15m \
  --namespace bench \
  -f helm/values/benchmark-avalanche-only.yaml
```

```shell
kubectl get po -n bench

NAME                                                   READY   STATUS      RESTARTS      AGE
prometheus-tobs-kube-prometheus-stack-prometheus-0     2/2     Running     0             68s
tobs-avalanche-54d4b5b8df-s4nj9                        1/1     Running     0             72s
tobs-connection-secret-7zxns                           0/1     Completed   0             72s
tobs-grafana-74dd454d46-npqzg                          3/3     Running     0             72s
tobs-kube-prometheus-stack-operator-755b69fbbb-zkj6t   1/1     Running     0             72s
tobs-kube-state-metrics-6c79f8fbdb-9s6hv               1/1     Running     0             72s
tobs-prometheus-node-exporter-k7hws                    1/1     Running     0             72s
tobs-promscale-7798d778f4-bhl4k                        1/1     Running     3 (56s ago)   72s
tobs-timescaledb-0                                     2/2     Running     0             72s
```

### Avalanche Configuration

We are setting the following Avalanche flags by default.  Please read over the
[documentation](https://github.com/timescale/helm-charts/blob/c669a2b9c4312f978c958d31f94c867edb690c8c/charts/avalanche/values.yaml#L14)
and adjust your tests accordingly.

```shell
    - --metric-count=100
    - --label-count=10
    - --series-count=10
    - --const-label=cluster=avalanche
    - --const-label=replica=0
    - --value-interval=60
    - --series-interval=315360000
    - --metric-interval=315360000
    - --remote-batch-size=2500
    - --remote-requests-count=1000000
    - --remote-write-interval=30s
```

### Updating

If you made changes to the default values and wish to apply an update to
avalanche you just need to run Helm again to apply it.

```shell
helm update tobs helm/charts/benchmark --wait --timeout 15m -n bench -f helm/values/benchmark-avalanche-only.yaml
```
