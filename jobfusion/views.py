from django.shortcuts import render,redirect

def dummypage_view(request):
    return render(request,'dummypage.html',{})