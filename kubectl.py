import subprocess
from string import Template
# open templates from files
with open('daemonset.yaml') as f:
    daemonset = Template(f.read())
with open('node.yaml') as f:
    node = Template(f.read())
# run kubectl with the generated yamls
for i in range(1, 11):
    subprocess.run(['kubectl', 'apply', '-f', '-'], input=daemonset.substitute(id=i).encode())
for i in range(1, 110):
    subprocess.run(['kubectl', 'apply', '-f', '-'], input=node.substitute(id=i).encode())
