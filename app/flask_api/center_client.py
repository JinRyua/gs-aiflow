import requests
from flask import json
from flask_api.global_def import config


class CenterClient:
    def __new__(cls, *args, **kwargs):
        """
        *args와 **kwargs는 무슨의미일까?
        여러 가변인자를 받겠다고 명시하는 것이며, *args는 튜플형태로 전달, **kwargs는 키:값 쌍의 사전형으로 전달된다.
        def test(*args, **kwargs):
            print(args)
            print(kwargs)

        test(5,10,'hi', k='v')
        결과 : (5, 10, 'hi') {'k': 'v'}
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(CenterClient, cls, *args, **kwargs).__new__(cls, *args, **kwargs)
        return cls.instance


def send_api(path, method, params=None, body=None, ):
    if config == None:
        return {}
    url = config.api_host + path
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*',
               'Authorization': "Bearer " + config.api_jwt}
    try:
        if (method == 'GET'):
            response = requests.get(url, headers=headers, params=params, verify=False)
        elif method == 'POST':
            response = requests.post(url, headers=headers, params=params,
                                     data=json.dumps(body, ensure_ascii=False, indent="\t"))
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, params=params,
                                     data=json.dumps(body, ensure_ascii=False, indent="\t"))

        if response.status_code == 401:
            jwtBody = {"Id": config.api_id, "Password": config.api_pass}
            jwtResponse = requests.post(config.api_host + "/auth", headers=headers, data=json.dumps(jwtBody))
            if jwtResponse.status_code == 200:
                JWT = jwtResponse.json()['accessToken']
                config.api_jwt = JWT

            headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*',
                       'Authorization': "Bearer " + JWT}
            if (method == 'GET'):
                response = requests.get(url, headers=headers, params=params, verify=False)
            elif method == 'POST':
                response = requests.post(url, headers=headers, params=params,
                                         data=json.dumps(body, ensure_ascii=False, indent="\t"))

        return response, response.status_code

    except Exception as ex:
        print(ex)


def getPods(workspace: str, cluster: str, project: str):
    query = dict()
    query['workspace'] = workspace
    query['cluster'] = cluster
    query['project'] = project

    response, code = send_api(path="/pods", method="GET", params=query)
    try:
        return response.json()
    except:
        return {}

def getPodDetail(podName : str, workspace: str, cluster: str, project: str):
    query = dict()
    query['workspace'] = workspace
    query['cluster'] = cluster
    query['project'] = project

    try:
        response, code = send_api(path="/pods/" + podName, method="GET", params=query)
        #없으면 패스
        if code == 404:
            response = {'data':{"name" : podName, "status" : "Waiting"}}
        else:
            response = response.json()

    except:
        return {'data':{"name" : podName, "status" : "Waiting"}}

    return response





def podsPost(body, workspace: str, cluster: str, project: str):
    query = dict()
    query['workspace'] = workspace
    query['cluster'] = cluster
    query['project'] = project

    response, code = send_api(path="/pods", method="POST", params=query, body=body)
    try:
        return response.json()
    except:
        return {}

def podsNameDelete(podName: str, workspace: str, cluster: str, project: str):
    query = dict()
    query['workspace'] = workspace
    query['cluster'] = cluster
    query['project'] = project

    response, code = send_api(path="/pods/" + podName, method="DELETE", params=query, body={})
    try:
        return response.json()
    except:
        return {}

def userProjectsNameGet(projectName: str):
    response, code = send_api(path="/userProjects/" + projectName, method="GET", params={}, body={})
    try:
        return response.json()
    except:
        return {}

body = {"projectName":"softonnet-test2",
        "projectDescription":"softonnet-test2",
        "projectType":"user",
        "clusterName":["onpremise(dongjak)","mec(ilsan)"],
        "workspaceName":"softonet",
        "memberName":"softonet",
        "istioCheck":"disabled"
        }
def projectsPost(workspaceName: str, memberName:str , projectname: str, projectDescription: str,  projectType: str = 'user', clusterName:list = [], istioCheck: str = 'disabled'):
    body = {"projectName": projectname,
        "projectDescription": projectDescription,
        "projectType": projectType,
        "clusterName": clusterName,
        "workspaceName": workspaceName,
        "memberName": memberName,
        "istioCheck": istioCheck
        }

    response, code = send_api('/projects', 'POST', params={}, body=body)
    if code != 201 and code != 200:
        return {'status' : 'failed'}

    try:
        return response.json()
    except:
        return {'status' : 'failed'}