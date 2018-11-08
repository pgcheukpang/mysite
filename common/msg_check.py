"""
@author: GZP
@contact: 449336625@qq.com
@file: msg_check.py
@time: 2018/9/12 0012 10:34
"""
from aip import AipImageCensor


class TextReviews:
    APP_ID = '11805205'
    API_KEY = '5S6dNYL2Pnyf9MhSGoN00qDA'
    SECRET_KEY = 'WfnqHkN6mQRes2PFuUStgR5oT5MhjIvI'

    @classmethod
    def get_check_json(cls, content):
        client = AipImageCensor(cls.APP_ID, cls.API_KEY, cls.SECRET_KEY)
        return client.antiSpam(content=content)
