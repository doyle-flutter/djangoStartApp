from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='kakao'),
    path('kakaoLoginLogic/', views.kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', views.kakaoLoginLogicRedirect),
    path('kakaoLogout/', views.kakaoLogout),
    path('kakaoPay/', views.kakaoPay),
    path('kakaoPayLogic/', views.kakaoPayLogic),
    path('paySuccess/', views.paySuccess),
    path('payFail/', views.payFail),
    path('payCancel/', views.payCancel),
]