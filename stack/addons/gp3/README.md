# gp3 addon

This addon enables gp3 storage class for EKS clusters.

## Prerequisites

- EKS cluster with version 1.23 or higher
- aws-ebs-csi-driver enabled in the cluster

_Note: How to start an EKS cluster with the required version and addons can be found in [docs/eks.md](docs/eks.md)._

## Install

```shell
make install
```

_Note: Remove existing PVs after installing new storage class it. We recommend installing this addon BEFORE starting the tobs stack_
