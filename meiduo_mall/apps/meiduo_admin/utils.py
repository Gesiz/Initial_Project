def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        'user_id': user.id
    }


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNum(PageNumberPagination):
    page_size = 5
    page_size_query_description = 'pagesize'

    def get_paginated_response(self, data):
        return Response(
            {
                'count': self.page.paginator.count,
                'lists': data,
                'page': self.page.number,
                'pages': self.page.paginator.num_pages,
                'pagesize': self.page_size,
            }
        )


from qiniu import Auth, put_data
import logging


def PutImage(data):
    """
    :param image_name:  上传到服务器所保存的图片名 随机不重复
    :param data:    图片的二进制数据
    :return: 上传成功返回的结果及返回状态
    """
    # 初始化 Auth 类
    access_key = 'q9crPZPROOXrykaH85q_zpEEll0f_LsjXwUnXHRo'
    secret_key = 'lG_4_tI8bJTR8Zk6z8fGwYp79aQHkJgolvvBL_qm'
    q = Auth(access_key, secret_key)
    # 设定 七牛云空间名
    bucket_name = "shunyi44"
    # 设定上传的文件名
    key = None
    try:
        # 生成上传凭证
        token = q.upload_token(bucket=bucket_name, key=key, expires=3600)
        ret, info = put_data(token, key, data)
        image_url = ret['key']
    except Exception as e:
        logging.error(e)
        return None, None
    else:
        return image_url
