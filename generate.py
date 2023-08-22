import argparse
import subprocess
import os
from string import Template


def get_current_cluster():
    result = subprocess.run(["kubectl", "config", "current-context"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("Failed to get current Kubernetes context.")
    return result.stdout.strip()


def is_namespaced_resource(kind: str) -> bool:
    return kind.lower() not in ["clusterrole", "clusterrolebinding", "namespace", "node", "persistentvolume", "storageclass"]

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Script to apply or delete Kubernetes resources"
)
parser.add_argument(
    "action", choices=["apply", "delete"], help='Action to perform: "apply" or "delete"'
)

# Supported Kubernetes kinds
# Each kind should have a corresponding YAML template file
kinds = [
    "daemonset",
    "deployment",
    "clusterrole",
    "clusterrolebinding",
    "configmap",
    "controllerrevision",
    "endpoints",
    "endpointslice",
    "event",
    "horizontalpodautoscaler",
    "ingress",
    "job",
    "lease",
    "limitrange",
    "networkpolicy",
    "node",
    "persistentvolumeclaim",
    "pod",
    "poddisruptionbudget",
    "podtemplate",
    "replicaset",
    "replicationcontroller",
    "resourcequota",
    "role",
    "rolebinding",
    "secret",
    "service",
    "serviceaccount",
    "statefulset"
]


# Add arguments for each kind
for kind in kinds:
    parser.add_argument(
        f"--{kind}", type=int, default=0, help=f"Number of {kind}s to create/delete"
    )

parser.add_argument(
    f"--all",
    type=int,
    default=0,
    help=f"Number of resources to create/delete for all kinds",
)

parser.add_argument(
    f"--namespaces",
    type=int,
    default=0,
    help=f"Number of namespaces to generate - resources will be create in each of these namespaces",
)

namespaces = [""]
args = parser.parse_args()

if getattr(args, "namespaces") > 0:
    namespaces = [f"namespace-{i}" for i in range(1, getattr(args, "namespaces") + 1)]


# current_cluster = get_current_cluster()
# if "kwok" not in current_cluster:
#     print(f"error: script is not running on 'kwok' cluster. Current cluster is '{current_cluster}'.")
#     exit(-1)

# create the namespaces
if namespaces[0] != "" and args.action == "apply":
    for ns in namespaces:
        subprocess.run(["kubectl", "create", "namespace", ns])

# Open templates and run kubectl with the generated YAMLs for each kind
for kind in kinds:
    filepath = os.path.join('resources', f"{kind}.yaml") 
    with open(filepath) as f:
        template = Template(f.read())
    amount_of_resources = (
        getattr(args, "all") if getattr(args, "all") > 0 and  getattr(args, kind) == 0 else getattr(args, kind)
    )

    current_kind_namespaces = namespaces if is_namespaced_resource(kind) else [""]
    for i in range(1, amount_of_resources + 1):
        # TODO use the namespaces array
        for ns in current_kind_namespaces:
            cmd_args = ["kubectl", args.action] 
            if ns != "":
                cmd_args.extend(["-n", ns])
            cmd_args.extend(["-f", "-"])
            subprocess.run(
                cmd_args,
                input=template.substitute(id=i).encode(),
            )

# finally delete the namespaces
if namespaces[0] != "" and args.action == "delete":
    for ns in namespaces:
        subprocess.run(["kubectl", "delete", "namespace", ns])
