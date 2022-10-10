# Amazon EKS Cluster provisioning and maintenance

The guide is based on official [AWS EKS documentation](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html) and assumes usage of `eksctl` tool. For other methods of provisioning EKS cluster, please refer to the official documentation.

- [Amazon EKS Cluster provisioning and maintenance](#amazon-eks-cluster-provisioning-and-maintenance)
  - [Prerequisites](#prerequisites)
  - [Cluster provisioning](#cluster-provisioning)
    - [AIO (All-in-one) privisioning](#aio-all-in-one-privisioning)
  - [Adding/Changing nodes](#addingchanging-nodes)
  - [Cluster deletion](#cluster-deletion)

## Prerequisites

This guide assumes you have the following tools installed:
- [awscli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [eksctl](https://github.com/weaveworks/eksctl) - [alternative installation instruction available here](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)
- [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)

## Cluster provisioning

1. Make sure you have your credentials set up in `~/.aws/credentials` file. You can use `aws configure` to set them up.
2. Define the cluster name and region in the environment variables:
    ```shell
    export NAME="promscale-${USER}-$(date +%s)"
    export REGION=us-east-1
    ```
3. Start a cluster with `eksctl`:
    ```shell
    eksctl create cluster --name "$NAME" --region "$REGION" --without-nodegroup
    ```
4. Wait until cluster is up and running. This can be checked with `eksctl`:
    ```shell
    eksctl get cluster --name "$NAME" --region "$REGION"
    ```
5. Verify cluster access with `kubectl`:
    ```shell
    kubectl cluster-info
    ```
6. Create a nodegroup:
    ```shell
    eksctl create nodegroup --cluster "$NAME" --region "$REGION" --node-type m5.xlarge --nodes 3 --nodes-min 1 --nodes-max 3 --managed
    ```

_Note: You can obtain current list of node types with `aws ec2 describe-instance-types --region "$REGION" | jq '.InstanceTypes[].InstanceType'` or [here](https://aws.amazon.com/ec2/instance-types/)._

### AIO (All-in-one) privisioning

```shell
export NAME="promscale-${USER}-$(date +%s)"
export REGION=us-east-1
eksctl create cluster --name "$NAME" --region "$REGION" --without-nodegroup
eksctl get cluster --name "$NAME" --region "$REGION"
kubectl cluster-info
eksctl create nodegroup --cluster "$NAME" --region "$REGION" --node-type m5.xlarge --nodes 3 --nodes-min 1 --nodes-max 3 --managed
```

## Adding/Changing nodes

By default we are deploying EKS cluster using a quite small setup of 3 nodes of type `m5.xlarge`. If you want to change the number of nodes or their type, you can do so by running the following:

1. Get the nodegroup name:
    ```shell
    eksctl get nodegroup --cluster "$NAME" --region "$REGION"
    ```
2. Change the nodegroup:
    ```shell
    eksctl scale nodegroup --cluster "$NAME" --region "$REGION" --node-type m5.xlarge --nodes 5 --nodes-min 1 --nodes-max 5 --name <nodegroup-name>
    ```
3. Wait until the nodes are up and running:
    ```shell
    kubectl get nodes
    ```

## Cluster deletion

Cluster deletion will remove all associated resources. To do this execute the following command:

```shell
eksctl delete cluster --name "$NAME" --region "$REGION"
```
