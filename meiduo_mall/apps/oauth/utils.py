"""对openid进行加密和解密的操作"""
from itsdangerous import BadSignature,TimedJSONWebSignatureSerializer as Serializer


def generic_openid(openid):
    # 1 创建一个实例对象
    s = Serializer(secret_key='123', expires_in=3600)
    # 2 组织数据 加密数据
    # 3 返回加密数据
    data = {
        'openid': openid
    }
    secret_data = s.dumps(data)
    return secret_data.decode()

def check_token(token):
    # 1 创建一个实例对象
    s = Serializer(secret_key='123',expires_in=3600)

    try:
        data = s.loads(token)
    except BadSignature:
        return None
    return data.get('openid')