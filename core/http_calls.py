import requests
import json

canvas_base_URL = "https://canvas.uw.edu/api/v1/"

f = open("canvasCredentials.json")
json_object = json.load(f)
#canvasToken = "Bearer " + json_object['token']
access_token = json_object['token']
f.close()

#headers = {'Authorization': canvasToken}
headers = {"Authorization": "Bearer {}".format(access_token)}


class httpCalls():
    def httpDelete(added_url):
        full_url = canvas_base_URL + added_url
        response = requests.delete(full_url, headers=headers)
        if response.status_code != 200:
            return ("Error")
        return ("Success")

    def httpGet(added_url, params=None):
        full_url = canvas_base_URL + added_url
        response = requests.get(full_url, headers=headers, params=params)
        response.raise_for_status() # raise error if 4xx or 5xx
        if response.status_code != 200:
            return ("Error")
        return response

    def httpPut(added_url, data=None):
        full_url = canvas_base_URL + added_url
        response = requests.put(full_url, headers=headers, data=data)
        if response.status_code != 200:
            return ("Error")
        return response

    def httpPutWithData(added_url, data):
        full_url = canvas_base_URL + added_url
        response = requests.put(full_url, data=data, headers=headers)
        if response.status_code != 200:
            return ("Error")
        return response

    def httpPost(added_url, data=None):
        full_url = canvas_base_URL + added_url
        response = requests.post(full_url, headers=headers, data=data)
        if response.status_code != 200:
            return ("Error")
        return response

    def httpPostWithData(added_url, data):
        full_url = canvas_base_URL + added_url
        response = requests.post(
            full_url, data=data, headers=headers)
        if response.status_code != 200:
            return ("Error")
        return response

    def httpUpload(URL, data, files):
        step1 = requests.post(URL, data=data, headers=headers)
        if step1.status_code != 200:
            return ("Error")
        step2 = step1.json()['upload_url']
        post_step2 = requests.post(step2, files=files)
        if post_step2.status_code != 201:
            return ("Error")
        get_api_url = post_step2.json()['location']
        step3 = requests.get(get_api_url, headers=headers)
        if step3.status_code != 200:
            return ("Error")
        return "Success"
