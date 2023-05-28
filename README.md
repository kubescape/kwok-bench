# kwok-bench

This repository provides scripts and configuration files that can help developers set up a fake Kubernetes cluster in scale easily using [KWOK](https://kwok.sigs.k8s.io/).

## Usage

### Prerequisites

- Python 3.6+
- Docker

### Getting Started

1. Install KWOK

    On Linux/MacOS systems you can install kwok/kwokctl via brew:

    ```sh
    brew install kwok
    ```

    For additional installation methods [read here](https://kwok.sigs.k8s.io/docs/user/install/).

2. Create cluster

    ```sh
    kwokctl create cluster --name demo
    ```

    Confirm cluster created by running:

    ```sh
    kwokctl get clusters
    ```

3. Generate resources:

    Run `generate.py` to create fake resources in the new cluster.

    ```sh
    python generate.py apply --node 1 --daemonset 2
    ```

## Troubleshooting

If you encounter any issues or errors while using this toolkit, please refer to the KWOK troubleshooting guide or open an issue in this repository.

## License

This project is licensed under the Apache-2.0 License.
