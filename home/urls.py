from django.contrib import admin
from django.urls import path

# from django.conf.urls import url
from home.views import enhance_section,view_post,PostComment,viewothersprofile,dislike_post,airesume,like_post,reject,accept,delete_post_view,deljob,send_request,courses,connections,chat_with_user,home_view,myposts,appliedpeople_view,deleteresume_view,applyjob_view,profile_edit_view,viewjob_view,profile_view,job_list_view,postjob_view,myapplications_view,uploadresume_view,contactus_view

from home.chat_views import chat_view,delchat,blockchat

urlpatterns = [
    path("<int:postid>/comment/", PostComment, name="PostComment"),
    path("AIResume_Generator/",airesume,name="airesume"),
    path("enhance-section/",enhance_section,name='enhance_section'),
    path("<int:id>/blockchat/",blockchat,name='blockchat'),
    path("<int:id>/deletechat/",delchat,name='delchat'),
    path("home/",home_view,name='home'),
    path("profile/",profile_view,name='profile'),
    path("joblistings/",job_list_view,name='joblistings'),
    path("postjobs/",postjob_view,name='postjobs'),
    path("myapplications/",myapplications_view,name='myapplications'),
    path("uploadresume/",uploadresume_view,name='resumes'),
    path("contactus/",contactus_view,name='contactus'),
    path("<int:job_id>/viewjob/",viewjob_view,name='viewjob'),
    path("<int:job_id>/apply/",applyjob_view,name='applyjob_view'),
    path("profile_edit/",profile_edit_view,name="profile_editpage"),
    path("deleteresume/",deleteresume_view,name="deleteresume"),
    path("appliedpeople/",appliedpeople_view,name='appliedpeople'),
    path("<int:jobid>/deljob/",deljob,name='deljob'),
    path("myposts/",myposts,name="myposts"),
    path("<int:userno>/viewothersprofile/",viewothersprofile,name="viewothersprofile"),
    path("chats/", chat_view, name="chats"),
    path("chat/<str:username>/", chat_with_user, name="chat"),
    path('connections/', connections, name='connections'),
    path('<int:sender_id>/accept/', accept, name='accept'),
    path('<int:sender_id>/reject/', reject, name='reject'),
    path('send/<int:profile_id>/',send_request, name='send_request'),
    path("courses/",courses,name="courses"),
    path("<int:postid>/delete_post/",delete_post_view,name="delete_post"),
    path("<int:postid>/like_post/",like_post,name="like_post"),
    path("<int:postid>/dislike_post/",dislike_post,name="dislike_post"),
    path("post/<int:postid>/", view_post, name="view_post")
]

