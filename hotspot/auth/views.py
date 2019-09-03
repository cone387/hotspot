from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from website.response import ApiResponse
from django.utils.decorators import method_decorator
from django.forms import ModelForm, model_to_dict

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model

User = get_user_model()


class CreateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserView(View):
    def post(self, request, option):
        if option == 'login':
            return self.login(request)
        elif option == 'logout':
            return self.logout(request)
        elif option == 'register':
            return self.register(request)
        elif option == 'change_password':
            return self.change_password(request)
        elif option == 'forget_password':
            return self.forget_password(request)
        else:
            return ApiResponse("forbidden option", code=400)
        return ApiResponse("login")

    def login(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return ApiResponse(data='unvalid username or password', code=400)
        request.session['user'] = model_to_dict(user, fields=['username', 'id'])
        if not request.session.session_key:
            request.session.create()
        user_info = {
            'username': user.username,
            'session_id': request.session.session_key,
        }
        return ApiResponse(user_info)

    def logout(self, request):
        out = logout(request)
        return ApiResponse("退出登录")

    def register(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            return ApiResponse('register success')
        return ApiResponse(form.errors.as_json(), code=400)

    def forget_password(self, request):
        return ApiResponse("忘记密码")

    def change_password(self, request):
        if request.user is None:
            return ApiResponse(code=400, data="forbidden request")
        return ApiResponse("修改密码")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)