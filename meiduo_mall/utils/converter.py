from django.urls import converters


class UsernameConverter:
    # 正则判断
    regex = '[a-zA-Z0-9]{5,20}'

    def to_python(self, value):
        # value 就是验证成功之后的数据
        return value

class MobileConverter:
    # 定义匹配手机号的正则表达式
    regex = '1[3-9]\d{9}'

    def to_python(self, value):
        # to_python：将匹配结果传递到视图内部时使用
        return value