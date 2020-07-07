
from rest_framework import exceptions
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication,jwt_decode_handler

import jwt

class Jwt(BaseJSONWebTokenAuthentication):

    def authenticate(self, request):
        # huo获取前段的token
        # jwt_value = self.get_jwt_value(request)
        jwt_token = request.META.get("HTTP_AUTHENTICATION")
        #自定义的校验规则
        token = self.parse(jwt_token)
        if token is None:
            return None
        try:
            # 将发送过来token反解析出载荷
            payload = jwt_decode_handler(jwt_token)
        except jwt.ExpiredSignature:
           raise exceptions.AuthenticationFailed("签名已过期")
        except:
            raise exceptions.AuthenticationFailed('不合法的用户')
        # 如果没有任何错误  则将认证出的用户返回
        user = self.authenticate_credentials(payload)
        return user,token


    # 自定义token校验规则 auth token jwt

    def parse(self,jwt_token):
        tokenss = jwt_token.split()
        if len(tokenss) != 3 or tokenss[0].lower() != 'auth' or tokenss[2].lower() != 'jwt':
            return None
        return tokenss[1]
