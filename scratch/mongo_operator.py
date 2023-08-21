import kopf
import os
from kubernetes import config
from typing import Any, Dict, List, Optional, Tuple, cast
import asyncio
from kubernetes_asyncio.client import (
    AppsV1Api,
    CoreV1Api,
    CustomObjectsApi,
    V1Namespace,
    V1PersistentVolumeClaimList,
    V1PodList,
    V1Service,
    V1ServiceList,
    V1StatefulSet,
    V1StatefulSetList,
)
from kubernetes_asyncio.client.api_client import ApiClient

def initialize_kube():
    print("Loading from local kube config")
    home = os.path.expanduser("~")
    kube_config_path = os.getenv("KUBE_CONFIG", home + "/.kube/config")
    config.load_kube_config(config_file=kube_config_path)

@kopf.on.create('mongodbs')
def create_fn(spec, **kwargs):
    print(f"And here we are! Creating: {spec}")
    return {'message': 'hello world'}  # will be the new status


async def get_pvcs_in_namespace(
    core: CoreV1Api, namespace: str, name: str) -> List[Dict[str, str]]:
    labels = {
        LABEL_NAME: name
    }
    label_selector = ",".join(f"{k}={v}" for k, v in labels.items())

    all_pvcs: V1PersistentVolumeClaimList = (
        await core.list_namespaced_persistent_volume_claim(
            namespace=namespace, label_selector=label_selector
        )
    )
    result = [{"uid": p.metadata.uid, "name": p.metadata.name} for p in all_pvcs.items]
    print(result)
    return [{"uid": p.metadata.uid, "name": p.metadata.name} for p in all_pvcs.items]

initialize_kube()
get_pvcs_in_namespace()