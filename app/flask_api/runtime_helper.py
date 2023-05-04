from flask_api.database import get_db_connection


def getBasicYaml(userID, projectID, nodeID):
    data = {'apiVersion': 'v1', 'kind': 'Pod',
            'metadata': {'name': nodeID, 'namespace': projectID, 'labels': {'app': 'nfs-test'}},
            'spec': {'restartPolicy': 'Never', 'nodeName': 'gedgeworker1', 'containers': [
                {'name': 'ubuntu', 'image': 'yolov5:v0.0.230503', 'imagePullPolicy': 'IfNotPresent',
                 'command': ['/bin/bash', '-c'], 'args': [
                    'source /root/path.sh; PATH=/opt/conda/envs/pt1.12.1_py38/bin:/root/volume/cuda/cuda-11.3/bin:$PATH; env; cd /root/yolov5; python train.py --data ~/volume/dataset/coco128/coco128.yaml --device 0 --weights ./weights/yolov5s-v7.0.pt --epochs 1 --batch 1'],
                 'env': [{'name': 'LD_LIBRARY_PATH',
                          'value': '/root/volume/cuda/cuda-11.3/lib64:/root/volume/cudnn/cuda-cudnn-8.3/lib64:/root/volume/tensorrt/TensorRT-8.4.3.1-cuda-11/lib'}],
                 'resources': {'limits': {'cpu': '4', 'memory': '8G', 'nvidia.com/gpu': '1'}}, 'volumeMounts': [
                    {'mountPath': '/root/volume/cuda/cuda-11.3', 'name': 'nfs-volume-total',
                     'subPath': 'cuda/cuda-11.3',
                     'readOnly': True}, {'mountPath': '/root/volume/cudnn/cuda-cudnn-8.3', 'name': 'nfs-volume-total',
                                         'subPath': 'cudnn/cuda-cudnn-8.3', 'readOnly': True},
                    {'mountPath': '/opt/conda/envs/pt1.12.1_py38', 'name': 'nfs-volume-total',
                     'subPath': 'envs/pt1.12.1_py38',
                     'readOnly': True},
                    {'mountPath': '/root/volume/tensorrt/TensorRT-8.4.3.1-cuda-11/', 'name': 'nfs-volume-total',
                     'subPath': 'tensorrt/TensorRT-8.4.3.1-cuda-11', 'readOnly': True},
                    {'mountPath': '/root/volume/dataset/coco128', 'name': 'nfs-volume-total',
                     'subPath': 'dataset/coco128',
                     'readOnly': True}]}],
                     'volumes': [
                         {'name': 'nfs-volume-total', 'persistentVolumeClaim': {'claimName': getBasicPVCName(userID, projectID)}}]}}
    return data


def getBasicPVName(userID, projectID):
    return "softonet" + "." + "pv." + userID + "." + projectID


def getBasicPVCName(userID, projectID):
    return "softonet" + "." + "pvc." + userID + "." + projectID


def getBasicPVYaml(userID, projectID):
    data = {
        "apiVersion": "v1",
        "kind": "PersistentVolume",
        "metadata": {
            "name": getBasicPVName(userID, projectID),
            "labels": {
                "app": "nfs-test"
            }
        },
        "spec": {
            "capacity": {
                "storage": "10Gi"
            },
            "volumeMode": "Filesystem",
            "accessModes": [
                "ReadOnlyMany"
            ],
            "persistentVolumeReclaimPolicy": "Delete",
            "storageClassName": "",
            "nfs": {
                "path": "/shared/nfs/",
                "server": "101.79.4.15"
            }
        }
    }
    return data


def getBasicPVCYaml(userID, projectID):
    data = {
        "apiVersion": "v1",
        "kind": "PersistentVolumeClaim",
        "metadata": {
            "name": getBasicPVCName(userID, projectID),
            "namespace": projectID
        },
        "spec": {
            "accessModes": [
                "ReadOnlyMany"
            ],
            "volumeMode": "Filesystem",
            "storageClassName": "",
            "resources": {
                "requests": {
                    "storage": "10Gi"
                }
            },
            "volumeName": getBasicPVName(userID, projectID),
            "selector": {
                "matchLabels": {
                    "app": "nfs-test"
                }
            }
        }
    }

    return data


def makeYamlTrainRuntime(userID, projectID, node_id, runtime, model, tensorRT, cuda):
    data = getBasicYaml(userID, projectID, node_id)

    return data

def makeYamlValidateRuntime(userID, projectID, node_id, runtime, model, tensorRT, cuda):
    data = {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': node_id}, 'spec': {'restartPolicy': 'Never',
                                                                                       'containers': [
                                                                                           {'name': node_id,
                                                                                            'image': 'aiflow/test1:v1.0.1.230329', }]}}
    return data
def makeYamlOptimizationRuntime(userID, projectID, node_id, runtime, model, tensorRT, cuda):
    data = {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': node_id}, 'spec': {'restartPolicy': 'Never',
                                                                                       'containers': [
                                                                                           {'name': node_id,
                                                                                            'image': 'aiflow/test1:v1.0.1.230329', }]}}
    return data

def makeYamlOptValidateRuntime(userID, projectID, node_id, runtime, model, tensorRT, cuda):
    data = {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': node_id}, 'spec': {'restartPolicy': 'Never',
                                                                                       'containers': [
                                                                                           {'name': node_id,
                                                                                            'image': 'aiflow/test1:v1.0.1.230329', }]}}
    return data


def getProjectYaml(userID, projectID):
    yaml = {'PV': {}, 'PVC': {}}
    yaml['PV'] = getBasicPVYaml(userID, projectID)
    yaml['PVC'] = getBasicPVCYaml(userID, projectID)

    return yaml
