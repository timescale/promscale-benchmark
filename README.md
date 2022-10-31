# Promscale-Benchmark

This repository will contain resources that will be used to benchmark
[Promscale](https://github.com/timescale/promscale) using [Avalanche](https://github.com/prometheus-community/avalanche).
For now this will focus on utilizing [tobs](https://github.com/timescale/tobs)
Helm chart to install to a K8s cluster. At this moment we are only using this
to test ingestion of Prometheus data into Promscale using the `remote-write`
endpoint in Promscale.

- [Promscale-Benchmark](#promscale-benchmark)
  - [Prerequisites](#prerequisites)
  - [Stack Setup](#stack-setup)
    - [Cluster provisioning](#cluster-provisioning)
      - [Local](#local)
      - [Amazon EKS](#amazon-eks)
    - [Stack installation](#stack-installation)
    - [Updating](#updating)
  - [Benchmark scenarios](#benchmark-scenarios)
    - [Available scenarios](#available-scenarios)
    - [Run a scenario](#run-a-scenario)
    - [Configure scenario](#configure-scenario)
  - [Grafana](#grafana)

## Prerequisites

To run this benchmark you will need to have at least the following tools installed.

* [docker](https://www.docker.com/) - For local testing only
* [kind](https://kind.sigs.k8s.io/) - For local testing only
* [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
* [helm](https://helm.sh)
* [make](https://www.gnu.org/software/make/)

## Stack Setup

In this repo we have a local Helm chart that can be used to install and manage
both tobs and Avalanche configurations into a Kubernetes Cluster.

The helm chart can be used on any Kubernetes cluster.

### Cluster provisioning

#### Local

Start a local kind cluster and install [cert-manager](https://cert-manager.io/)

```shell
make start-kind
```

Verify that you have access to the local cluster

```shell
kubectl get nodes
```

#### Amazon EKS

Go to [docs/eks.md](docs/eks.md) for instructions on how to provision and manage an EKS cluster.

### Stack installation

We are using Helm to install the latest tobs stack with `values.yaml` pre-configured for
the benchmark environment.

The default installation will install tobs in `bench` namespace and can be executed with:

```shell
make stack
```

To check if the stack was installed correctly you can run:

```shell
kubectl get po -n bench

NAME                                                         READY   STATUS      RESTARTS        AGE
opentelemetry-operator-controller-manager-7b69d9856f-8nhcm   2/2     Running     0               3m40s
prometheus-tobs-kube-prometheus-stack-prometheus-0           2/2     Running     0               3m26s
tobs-connection-secret-9m45w                                 0/1     Completed   0               3m40s
tobs-grafana-6c545d5fc8-7hr9k                                3/3     Running     0               3m40s
tobs-kube-prometheus-stack-operator-75985bb949-x2bxv         1/1     Running     0               3m40s
tobs-kube-state-metrics-5cfc875576-9pp5b                     1/1     Running     0               3m40s
tobs-opentelemetry-collector-6869598c59-tbncl                1/1     Running     0               107s
tobs-prometheus-node-exporter-hc6s6                          1/1     Running     0               3m40s
tobs-promscale-57855f5c46-zn562                              1/1     Running     4 (2m54s ago)   3m40s
tobs-timescaledb-0                                           2/2     Running     0               3m40s
```

### Updating

If you want to modify the default stack installation (ex. to change promscale image version) you
can edit the `stack/values.yaml` file and run:

```
make stack
```

## Benchmark scenarios

### Available scenarios

To check the available scenarios explore the `scenarios` directory.

### Run a scenario

To quickly execute a benchmark scenario you can run:

```shell
make scenarios/<TYPE>/<NAME>
```

Where `<TYPE>` is the type of scenario you want to run and `<NAME>` is the name of the scenario.

For example:
```
make scenarios/metrics/ingest-direct
```

This will run the load-generator from the `ingest-direct` scenario in the `metrics` type.

_Note: Keep in mind that by default all scenarios are deployed in separate namespaces._

Alternatively you can go to the scenario directory and run `make` command.

### Configure scenario

To configure a scenario follow its instructions in the dedicated `README.md` file. You can find
the file in scenario directory.

## Grafana

You can easily log into Grafana and view Dashboards with a simple command:

```shell
make grafana
```

Once ran you can log into Grafana locally with [http://localhost:8080](https://localhost:8080).

_Note: By default grafana is configured with anonymous access which doesn't require a password._
