import argparse
import subprocess
from string import Template

# Parse command line arguments
parser = argparse.ArgumentParser(description='Script to apply or delete Kubernetes resources')
parser.add_argument('action', choices=['apply', 'delete'], help='Action to perform: "apply" or "delete"')

# Supported Kubernetes kinds
# Each kind should have a corresponding YAML template file
kinds = ['daemonset', 'node', 'service']

# Add arguments for each kind
for kind in kinds:
    parser.add_argument(f'--{kind}', type=int, default=0, help=f'Number of {kind}s to create/delete')

args = parser.parse_args()

# Open templates and run kubectl with the generated YAMLs for each kind
for kind in kinds:
    with open(f'{kind}.yaml') as f:
        template = Template(f.read())
    for i in range(1, getattr(args, kind) + 1):
        subprocess.run(['kubectl', args.action, '-f', '-'], input=template.substitute(id=i).encode())
