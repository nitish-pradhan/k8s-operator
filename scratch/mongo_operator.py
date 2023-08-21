import kopf
import os
from kubernetes import config

def initialize_kube():
    DEV = os.getenv('DEV')
    if DEV:
        print ("Loading from local kube config")
        home = os.path.expanduser("~")
        kube_config_path = os.getenv("KUBE_CONFIG", home+"/.kube/config")
        config.load_kube_config(config_file=kube_config_path)
    else:
        print ("Loading In-cluster config")
        config.load_incluster_config()

@kopf.on.create('mongodbs')
def create_fn(spec, **kwargs):
    print(f"And here we are! Creating: {spec}")
    return {'message': 'hello world'}  # will be the new status


initialize_kube()