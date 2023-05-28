# kwok-bench

This repository aims to help developers set up a large-scale, simulated Kubernetes cluster, to test and benchmark your applications, with ease using [KWOK](https://kwok.sigs.k8s.io/).

## Usage

### Prerequisites

- Python 3.6 or higher.
- Docker installed and running on your machine.

---

1. **Install KWOK**

     KWOK can be installed on Linux/MacOS systems via the Homebrew package manager:

    ```sh
    brew install kwok
    ```

    For other systems or installation methods, please refer to the [official KWOK documentation](https://kwok.sigs.k8s.io/docs/user/install/).

2. **Create a KWOK Cluster**

    Create a new cluster named "demo" with the following command:

    ```sh
    kwokctl create cluster --name demo
    ```

    Confirm that the cluster has been created successfully by running:

    ```sh
    kwokctl get clusters
    ```

3. **Generate Resources**

    Use the `generate.py` script to create fake resources in the new cluster. You can specify the number of resources per supported kind as arguments to the script:

    ```sh
    python generate.py apply --node 1 --daemonset 2
    ```

   > This command will create 1 node and 2 daemonsets in the "demo" cluster.

   Removing resources can be achieved by running the script with the `delete` argument:

   ```sh
   python generate.py delete --node 3
   ```

   > This command will delete 3 nodes

4. **Deleting the Cluster**

   After you have finished using the cluster, it is recommended to delete it to free up resources. You can easily do this with the following command:

   ```sh
   kwokctl delete cluster --name demo
   ```

## Troubleshooting

If you encounter any issues or errors while using, please open an issue in this repository.

## License

This project is licensed under the Apache-2.0 License.
