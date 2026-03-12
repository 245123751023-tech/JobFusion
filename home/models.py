from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    #name = ONe to one field to User
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,related_name='profile')
    full_name = models.CharField(max_length=50)
    Email = models.EmailField(default=True)
    Role = models.CharField(max_length=20,default="user")
    liurl = models.URLField(max_length=50,default='NA',null=True,blank=True)
    #Username = models.CharField(max_length=50,default=False)
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    bio = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to='profile_pics/',null=True,blank=True)
    skills = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resumes/',null=True,blank=True)
    otherskills = models.CharField(max_length=200,null=True,blank=True)
    exp = models.SmallIntegerField(null=True,blank=True)
    gclg = models.CharField(max_length=30,null=True,blank=True)
    gstartingyear = models.CharField(max_length=10,null=True,blank=True)
    gendingyear = models.CharField(max_length=10,null=True,blank=True)
    gbranch = models.CharField(max_length=20,null=True,blank=True)
    gcgpa = models.CharField(max_length=5,null=True,blank=True)
    gclgadd = models.CharField(max_length=100,null=True,blank=True)
    iclg = models.CharField(max_length=30,null=True,blank=True)
    istartingyear = models.CharField(max_length=10,null=True,blank=True)
    iendingyear = models.CharField(max_length=10,null=True,blank=True)
    ibranch = models.CharField(max_length=20,null=True,blank=True)
    imarks = models.CharField(max_length=5,null=True,blank=True)
    schoolname = models.CharField(max_length=30,null=True,blank=True)
    sscyear = models.CharField(max_length=5,null=True,blank=True)
    cname = models.CharField(max_length=50,null=True,blank=True)
    industry = models.CharField(max_length=20,null=True,blank=True)
    cadd = models.CharField(max_length=100,null=True,blank=True)
    hiringneeds = models.CharField(max_length=50,null=True,blank=True)
    cemail = models.EmailField(max_length=40,null=True,blank=True)

class postjob(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    job = models.CharField(max_length=50,null=True)
    company_name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=30)
    #salary_range = models.IntegerField(default=10000)
    salary_range = models.TextField(max_length=10,default="$one-rupee",null=True,blank=True)
    desc = models.TextField(max_length=200)
    req = models.CharField(max_length=200,default=1)
    posted_by = models.TextField(max_length=20,null=True)
    posted_on = models.DateTimeField(auto_now_add=True,null=True)

class ApplicationJob(models.Model): # this table has data about the people who applied to jobs posted by HR
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    job = models.ForeignKey(postjob,on_delete=models.CASCADE)
    others = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,null=True,default='In-Touch')

class Application(models.Model): # this table has jobs for which user applied.
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    job = models.ForeignKey(postjob,on_delete=models.CASCADE,null=True)
    applied_on = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=20,null=True,default='In-Touch') # like in-touch, will contact
    posted_by = models.TextField(max_length=20,null=True)
    #applied_on = models.DateTimeField(null=True,blank=True,default='Jan 2026')


class Contactus(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    phno = models.CharField(max_length=10)
    Email = models.EmailField()
    msg = models.TextField()


class Requests(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_reqs")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="received_reqs")
    IsFriend = models.BooleanField(default=False)
    IsPending = models.BooleanField(default=False)



class Posts(models.Model):
    MEDIA_TYPES=(
        ('image','Image'),
        ('video','Video'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    caption = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    media_url = models.URLField()
    media_type=models.CharField(max_length=10,choices=MEDIA_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    
    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()

class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)


class NotRequired(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="prefs")
    deleted_chats = models.JSONField(default=list,blank=True)
    blocked_chats = models.JSONField(default=list,blank=True)

