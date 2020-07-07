import re
from django.contrib.auth.hashers import check_password,make_password
from rest_framework import exceptions, serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.settings import api_settings


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from day7.models import User, Computer


class UserMS(ModelSerializer):
    #自定义反序列化字段 只参与反序列化 不要求与model映射字段
    account = serializers.CharField(write_only = True)
    pwd = serializers.CharField(write_only = True)
    class Meta:
        model =User
        fields = ["account","pwd","phnoe","email","username"]
        extra_kwargs = {
            "username":{
                "read_only":True,
            },
            "phnoe":{
                "read_only": True,
            },
            "email":{
                "read_only": True,
            }
        }


        # 全局校验钩子  可以通过attrs获取到前台发送的所有的参数
    def validate(self, attrs):
        account = attrs.get("account")
        pwd = attrs.get("pwd")
         #对数据库里的书库进行判断 手机号 邮箱 账号
        if re.match(r".+@.+",account):
            use = User.objects.filter(email=account).first()
        elif re.match(r"1[3-9][0-9]{9}",account):
            use = User.objects.filter(phnoe=account).first()
        else:
            use=  User.objects.filter(username = account).first()
#pad判断用户存在与否
        if use and use.check_password(pwd):
            #签发token
            pay = jwt_payload_handler(use)  #shen生成载荷信息
            token = jwt_encode_handler(pay)  #生成token
            self.token = token
            self.obj = use
        return attrs


class Computerss(ModelSerializer):
    class Meta:
        model = Computer
        #写all的话代表和模型所有的字段映射
        # fields = '__all__'
        fields = ('name',"price","brand")