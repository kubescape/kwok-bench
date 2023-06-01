import argparse
import subprocess
import os
from string import Template

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
    "clusterrole",
    "clusterrolebinding",
    "configmap",
    "controllerrevision",
    "daemonset",
    "deployment",
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

args = parser.parse_args()

# Open templates and run kubectl with the generated YAMLs for each kind
for kind in kinds:
    filepath = os.path.join('resources', f"{kind}.yaml") 
    with open(filepath) as f:
        template = Template(f.read())
    amount_of_resources = (
        getattr(args, "all") if getattr(args, "all") > 0 else getattr(args, kind)
    )
    for i in range(1, amount_of_resources + 1):
        subprocess.run(
            ["kubectl", args.action, "-f", "-"],
            input=template.substitute(id=i).encode(),
        )
