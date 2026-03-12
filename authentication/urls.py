
from django.contrib import admin
from django.urls import path,include
from authentication.views import login_view,signup_view,learnmore_view,logout_view,rolespage,page1_view,page3_view,page4_view
urlpatterns =[
    #path('',login_view),
    path("login/",login_view,name='login'),
    path('signup/',signup_view,name='signup'),
    path("learnmore/",learnmore_view,name='learnmore'),
    path('logout/',logout_view,name='logout'),
    path("basicinfo2/",rolespage,name='rolespage'),
    path("basicinfo1/",page1_view,name='page1'),
    path("basicinfo3/",page3_view,name='page3'),
    path('basicinfo4/',page4_view,name='page4'),
]