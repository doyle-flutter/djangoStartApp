from django.shortcuts import render, redirect
import requests
import json
from django.template import loader
from django.http import HttpResponse, JsonResponse


def test(request):
    _data = {
        "data": [
            {
                "title": "트로트",
                "datas": [
                    {'title': '노래제목1', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목1', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목1', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목1', 'name': '가수', 'des': '가사'},
                ]
            },
            {
                "title": "댄스",
                "datas": [
                    {'title': '노래제목2', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목2', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목2', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목2', 'name': '가수', 'des': '가사'},
                ]
            },
            {
                "title": "힙합",
                "datas": [
                    {'title': '노래제목3', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목3', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목3', 'name': '가수', 'des': '가사'},
                    {'title': '노래제목3', 'name': '가수', 'des': '가사'}
                ]
            }
        ]
    }
    return JsonResponse(_data)

def index(request):
    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'index.html', _context)

def kakaoLoginLogic(request):
    _restApiKey = '' # 입력필요
    _redirectUrl = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code']
    _restApiKey = '' # 입력필요
    _redirect_uri = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
    _res = requests.post(_url)
    _result = _res.json()
    request.session['access_token'] = _result['access_token']
    request.session.modified = True
    return render(request, 'loginSuccess.html')

def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
      'Authorization': f'bearer {_token}'
    }
    # _url = 'https://kapi.kakao.com/v1/user/unlink'
    # _header = {
    #   'Authorization': f'bearer {_token}',
    # }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    if _result.get('id'):
        del request.session['access_token']
        return render(request, 'loginoutSuccess.html')
    else:
        return render(request, 'logoutError.html')
def kakaoPay(request):
    return render(request, 'kakaopay.html')
def kakaoPayLogic(request):
    _admin_key = '' # 입력필요
    _url = f'https://kapi.kakao.com/v1/payment/ready'
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}',
    }
    _data = {
        'cid': 'TC0ONETIME',
        'partner_order_id':'partner_order_id',
        'partner_user_id':'partner_user_id',
        'item_name':'초코파이',
        'quantity':'1',
        'total_amount':'2200',
        'vat_amount':'200',
        'tax_free_amount':'0',
        # 내 애플리케이션 -> 앱설정 / 플랫폼 - WEB 사이트 도메인에 등록된 정보만 가능합니다
        # * 등록 : http://IP:8000 
        'approval_url':'http://127.0.0.1:8000/paySuccess', 
        'fail_url':'http://127.0.0.1:8000/payFail',
        'cancel_url':'http://127.0.0.1:8000/payCancel'
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()
    request.session['tid'] = _result['tid']
    return redirect(_result['next_redirect_pc_url'])
def paySuccess(request):
    _url = 'https://kapi.kakao.com/v1/payment/approve'
    _admin_key = '' # 입력필요
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}'
    }
    _data = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'],
        'partner_order_id':'partner_order_id',
        'partner_user_id':'partner_user_id',
        'pg_token': request.GET['pg_token']
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()
    if _result.get('msg'):
        return redirect('/payFail')
    else:
        # * 사용하는 프레임워크별 코드를 수정하여 배포하는 방법도 있지만
        #   Req Header를 통해 분기하는 것을 추천
        # - Django 등 적용 시
        # return render(request, 'paySuccess.html')
        print(_result)
        # - React 적용 시
        return redirect('http://localhost:3000')

# Flutter & Djnago
def kakaoPayLogic2(request):
    _admin_key = '' # 입력필요
    _url = f'https://kapi.kakao.com/v1/payment/ready'
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}',
    }
    _data = {
        'cid': 'TC0ONETIME',
        'partner_order_id':'partner_order_id',
        'partner_user_id':'partner_user_id',
        'item_name':'초코파이',
        'quantity':'1',
        'total_amount':'2200',
        'vat_amount':'200',
        'tax_free_amount':'0',
        # 내 애플리케이션 -> 앱설정 / 플랫폼 - WEB 사이트 도메인에 등록된 정보만 가능합니다
        # * 등록 : http://IP:8000 
        'approval_url':'http://127.0.0.1:8000/paySuccess2', 
        'fail_url':'http://127.0.0.1:8000/payFail',
        'cancel_url':'http://127.0.0.1:8000/payCancel'
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()
    request.session['tid'] = _result['tid']
    return redirect(_result['next_redirect_pc_url'])
def paySuccess2(request):
    _url = 'https://kapi.kakao.com/v1/payment/approve'
    _admin_key = '' # 입력필요
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}'
    }
    _data = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'],
        'partner_order_id':'partner_order_id',
        'partner_user_id':'partner_user_id',
        'pg_token': request.GET['pg_token']
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()
    if _result.get('msg'):
        return redirect('/payFail')
    else:
        return render(request, 'paySuccess2.html')
def payFail(request):
    return render(request, 'payFail.html')
def payCancel(request):
    return render(request, 'payCancel.html')

def methodsCheck(request, id):
    if(request.method == 'GET'):
        print(f"GET QS : {request.GET.get('data', '')}")
        print(f"GET Dynamic Path : {id}")
    
    # PostMan으로 Localhost 테스트를 위해 CSRF 해제
    # project/settings.py 파일에서 
    # MIDDLEWARE -> 'django.middleware.csrf.CsrfViewMiddleware' 주석 처리
    elif(request.method == 'POST'):
        print(f"POST QS : {request.GET.get('data', '')}")
        print(f"POST Dynamic Path : {id}")
        return HttpResponse("POST Request.", content_type="text/plain")
    return render(request, 'methodGet.html')