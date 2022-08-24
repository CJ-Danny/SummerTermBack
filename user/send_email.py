from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from django.conf import settings  # setting.py添加的的配置信息
from user.models import *

import datetime


# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def sendCodeEmail(email):
    EmailCode.objects.filter(email=email).delete()
    code = random_str(16)
    newCode = EmailCode()
    newCode.email = email
    newCode.code = code
    newCode.save()

    email_title = "注册激活验证码"
    email_body = "欢迎您!\n"
    email_body += "您的注册验证码为：{0}, 该验证码有效时间为三十分钟，请尽快进行验证.\n".format(code)
    email_body += "如果此操作非您本人所为,请忽略此邮件."

    send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
    return send_status


def sendPasswordCodeEmail(email):
    EmailCode.objects.filter(email=email).delete()
    code = random_str(16)
    newCode = EmailCode()
    newCode.email = email
    newCode.code = code
    newCode.save()

    email_title = "密码重置验证码"
    email_body = "您的密码重置验证码为：{0}, 该验证码有效时间为三十分钟，请及时修改密码.\n".format(code)
    email_body += "如果此操作非您本人所为,请忽略此邮件."

    send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
    return send_status


def checkCode(code, email):
    if not EmailCode.objects.filter(email=email, code=code).exists():
        return False
    else:
        EmailCode.objects.filter(email=email, code=code).delete()
        return True
