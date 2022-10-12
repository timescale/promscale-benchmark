# Benchmarking scenarios

This directory contains various benchmarking scenarios that can be used to test Promscale. Each scenario is a self-contained directory that contains a README.md file with instructions on how to run the scenario. The README.md file also contains a description of the scenario and any configuration options that can be used to tweak the scenario.

The scenarios are meant to be run on a Kubernetes cluster. The cluster can be local or remote. To simplify cleanup, each scenario is deployed in a separate namespace. The namespace can be changed by setting the `NS` environment variable.
