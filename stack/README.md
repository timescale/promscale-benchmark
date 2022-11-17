# Main application stack

This is the main application stack based on tobs. It pre-configured for usage in a benchmark environment.

For information on how to configure the stack, see the [tobs documentation](https://github.com/timescale/tobs/tree/main/chart#tobs-helm-charts).

## Applying custom configuration

To allow customization of the stack and allow easy `git rebase` flow it is recommended
to use `values-overrides.yaml` file. This file is ignored by git and can be used to override any configuration option in the stack while allowing to keep the original configuration in the `values.yaml` file. It also allows easy sharing of the configuration between different users.

Configuration options from `values-overrides.yaml` are merged with the default configuration from `values.yaml` file and the resulting configuration is used to deploy the stack.
