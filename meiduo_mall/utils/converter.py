from django.urls import converters


class UsernameConverter:
    # 正则判断
    regex = '[a-zA-Z0-9]{5,20}'

    def to_python(self, value):
        # value 就是验证成功之后的数据
        return value
