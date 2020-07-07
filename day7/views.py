import re

from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework.filters import SearchFilter,OrderingFilter

from day7.filter import LimitFilter
from day7.models import User, Computer
from day7.paginations import MyPageNumberPagination, MyLimitPagination, MyCoursePagination
from day7.serializers import UserMS, Computerss
from utils.response import APIResponse


#
class Users(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self,request,*args,**kwargs):
        return APIResponse(results={"username":request.user.username})

class Login(APIView):
    '''
    实现多方式登录token 的账号 手机 邮箱等登录
    '''
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        #账号 account 密码 pwd
        account = request.data.get('account')
        pwd = request.data.get("pwd")
        user_a = UserMS(data=request.data)
        user_a.is_valid(raise_exception=True)
        return APIResponse(data_message="ok" ,token=user_a.token,results=UserMS(user_a.obj).data)

    # 面向过程的写法 高耦合 无法服用 达米安逻辑太强
    def demo(self,request,*args,**kwargs):
        account = request.data.get("account")
        pwd = request.data.get("pwd")
        # 对于各种登录方式做处理  账号  邮箱  手机号
        if re.match(r'.+@.+', account):
            user_obj = User.objects.filter(email=account).first()
        elif re.match(r'1[3-9][0-9]{9}', account):
            user_obj = User.objects.filter(phone=account).first()
        else:
            user_obj = User.objects.filter(username=account).first()

        # 判断用户是否存在 且用户密码是否正确
        if user_obj and user_obj.check_password(pwd):
            # 签发token
            payload = jwt_payload_handler(user_obj)  # 生成载荷信息
            token = jwt_encode_handler(payload)  # 生成token
            return APIResponse(results={"username": user_obj.username}, token=token)

        return APIResponse(data_message="错误了")


#y游标分页
class Computers(ListAPIView):
    queryset = Computer.objects.all()
    serializer_class = Computerss

    #通过此参数配置过滤器的器类
    filter_backends = [SearchFilter,OrderingFilter,LimitFilter]
    #指定的当前的搜索
    search_fields = ["name","price"]
    #指顶排序的条件
    ordering = ["price"]


    #指定分页器  不适用列表或元组
    # pagination_class = MyPageNumberPagination
    # pagination_class = MyLimitPagination
    pagination_class = MyCoursePagination

