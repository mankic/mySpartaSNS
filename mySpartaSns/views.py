from django.http import HttpResponse  # 괄호안의 내용을 전달해준다.
from django.shortcuts import render  # HTML 파일을 보여준다.


def base_response(request):
    return HttpResponse("안녕하세요! 장고의 시작입니다!")


# html 파일 보여줌
def first_view(request):
    return render(request, 'my_test.html')
