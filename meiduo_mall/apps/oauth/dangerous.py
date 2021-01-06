"""
加密
1 导入
2 创建实例对象
3 组织数据 然后加密
"""

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

s = Serializer(secret_key='123', expires_in=3600)

data = {
    'openid': '123',
}

s.dumps(data)
# b'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwOTg5Nzc5NywiZXhwIjoxNjA5OTAxMzk3fQ.eyJvcGVuaWQiOiIxMjMifQ.f5eCbgroYfRG_T5hNc-TDwO8me-pg8Ij8mSlvXLMQKlzmJKTG-_a7z1MNlug0R7yasLetYosckr4wCX2Y_o13A'

"""
解密数据
1 导入
2 创建实例对象
3 解密数据


"""

s = Serializer(secret_key='123', expires_in=3600)
try:
    s.loads(
        b'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwOTg5Nzc5NywiZXhwIjoxNjA5OTAxMzk3fQ.eyJvcGVuaWQiOiIxMjMifQ.f5eCbgroYfRG_T5hNc-TDwO8me-pg8Ij8mSlvXLMQKlzmJKTG-_a7z1MNlug0R7yasLetYosckr4wCX2Y_o13A')
except Exception as e:
    pass

