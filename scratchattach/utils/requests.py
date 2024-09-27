import requests
from . import exceptions

proxies = None

class Requests:
    """
    Centralized HTTP request handler (for better error handling and proxies)
    """

    @staticmethod
    def check_response(r : requests.Response):
        if r.status_code == 403 or r.status_code == 401:
            raise exceptions.Unauthorized
        if r.status_code == 500:
            raise exceptions.APIError("Internal Scratch server error")
        if r.status_code == 429:
            raise exceptions.Response429("You are being rate-limited (or blocked) by Scratch")
        if r.text == '{"code":"BadRequest","message":""}':
            raise exceptions.BadRequest("Make sure all provided arguments are valid")
        if r.text == '{"code":"BadRequest","message":""}':
            raise exceptions.BadRequest("Make sure all provided arguments are valid")

    @staticmethod
    def get(url, *, data=None, json=None, headers=None, cookies=None, timeout=None):
        try:
            r = requests.get(url, data=data, json=json, headers=headers, cookies=cookies, timeout=timeout, proxies=proxies)
        except Exception as e:
            raise exceptions.FetchError(e)
        Requests.check_response(r)
        return r
    
    @staticmethod
    def post(url, *, data=None, json=None, headers=None, cookies=None, timeout=None):
        try:
            r = requests.post(url, data=data, json=json, headers=headers, cookies=cookies, timeout=timeout, proxies=proxies)
        except Exception as e:
            raise exceptions.FetchError(e)
        Requests.check_response(r)
        return r

    @staticmethod
    def delete(url, *, data=None, json=None, headers=None, cookies=None, timeout=None):
        try:
            r = requests.delete(url, data=data, json=json, headers=headers, cookies=cookies, timeout=timeout, proxies=proxies)
        except Exception as e:
            raise exceptions.FetchError(e)
        Requests.check_response(r)
        return r

    @staticmethod
    def put(url, *, data=None, json=None, headers=None, cookies=None, timeout=None):
        try:
            r = requests.put(url, data=data, json=json, headers=headers, cookies=cookies, timeout=timeout, proxies=proxies)
        except Exception as e:
            raise exceptions.FetchError(e)
        Requests.check_response(r)
        return r