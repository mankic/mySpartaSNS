from django.shortcuts import render, redirect   # render: html파일 화면에 보여준다
from .models import UserModel
from django.http import HttpResponse    # 화면에 글자 띄워주기
from django.contrib.auth import get_user_model  # 사용자가 데이터 베이스 안에 있는지 검사해주는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')    # / 는 tweet앱에 views.py의 home 함수와 연결
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        # html에서 name='username' 이름으로된 데이터를 가져온다. 없다면 빈칸처리
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        bio = request.POST.get('bio','')

        if password != password2:
            # 패스워드가 같지 않다고 알람
            return render(request, 'user/signup.html', {'error':'패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                return render(request,'user/signup.html',{'error':'빈칸을 채워주세요'})

            exist_user = get_user_model().objects.filter(username=username)
            # exist_user = UserModel.objects.filter(username=username)
            # .filter는 데이터가 없어도 에러발생을 안함

            if exist_user:
                return render(request, 'user/signup.html', {'error':'이미 존재하는 아이디 입니다.'})
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)

                # new_user = UserModel()    # 만든모델 사용할때 추가
                # new_user.username = username
                # new_user.password = password
                # new_user.bio = bio
                # new_user.save()

                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        # 인증기능 모듈. 암호화된 비밀번호와 입력된 비밀번호가 일치하는지, 사용자와 일치하는지까지
        me = auth.authenticate(request, username=username, password=password)
        # me = UserModel.objects.get(username=username)
        if me is not None:  # 사용자가 있다면
            auth.login(request, me) #
            # request.session['user'] = me.username   # session : 사용자정보를 저장할수있는 공간
            return redirect('/')    # 기본 url
        else:
            return render(request,'user/signin.html',{'error':'아이디 혹은 패스워드를 확인해주세요'})
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')


@login_required # 사용자가 꼭 로그인이 되어있어야만 접근이 가능한 함수
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')