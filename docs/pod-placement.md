# Pod placement

Document describes used methods to place pods on specific nodes.

## Quick start

To quickly place pods on specific nodes you can use the following command:

```shell
# Place database on a separate, dedicated node
DB_NODE=<NODE_NAME>
kubectl taint nodes "${DB_NODE}" database=true:NoSchedule
kubectl label node "${DB_NODE}" topology.timescale.com/zone=database

# Place promscale-connector on a separate, dedicated node
CONNECTOR_NODE=<NODE_NAME>
kubectl taint nodes "${CONNECTOR_NODE}" connector=true:NoSchedule
kubectl label node "${CONNECTOR_NODE}" topology.timescale.com/zone=connector
```

This will taint nodes and apply labels to them. Tolerations, anti-affinity, and node affinity settings are already applied to the stack.

## Pod anti-affinity

Stack is by defualt configured to use anti-affinity to repel pods from other pods when choosing node to place them on. Configuration is done in `stack/values.yaml` file and it is supposed to repulse prometheus, promcale-connector, and databse pods from being placed on the same node. This is done to avoid the situation when all pods are placed on the same node and the node is overloaded. This is only a soft constraint and it is possible that all pods are placed on the same node.

We are using the following configuration, example for promscale-connector:

```yaml
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: app.kubernetes.io/component
              operator: In
              values:
              - timescaledb
          topologyKey: "kubernetes.io/hostname"
```

## Node affinity

Stack is by defualt configured to use node affinity to attract pods to specific nodes. Configuration is done in `stack/values.yaml` file and it is supposed to attract pods to specific node, primarily tainted ones. This is only a soft constraint and it is possible that all pods are placed on the same node.

We are using the following configuration, example for promscale-connector:

```yaml
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
          - key: topology.timescale.com/zone
            operator: In
            values:
            - connector
```

### Label nodes

To use node affinity, nodes need to have proper labels on them. This can be done by using `kubectl label` command. Example:

```shell
NODE=<NODE_NAME>

kubectl label node "${NODE}" topology.timescale.com/zone=connector
```

Ideally this is done in conjunction with tainting node as described in [taints](#taints) section.

## Taints and Tolerations

To make sure that nodes "accept" only specific pods we are using taints and tolerations. Taints are set on nodes and tolerations are set on pods. Default tolerations are set in `stack/values.yaml` file.

### Taints

Taints need to be applied manually on nodes. To apply taints on nodes run the following command:

```shell
NODE=<NODE_NAME>

# Taint node for database
kubectl taint nodes "${NODE}" database=true:NoSchedule
```

### Tolerations

By default database and connector pods are configured to tolerate specific taints.

Connector pods by default tolerate `connector=true:NoSchedule` taint. This is done to make sure that connector pods are placed on nodes dedicated to them.

Database pods by default tolerate `database=true:NoSchedule` taint. This is done to make sure that database pods are placed on nodes dedicated to them.
