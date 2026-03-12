from django.contrib import admin
from home.models import Profile,postjob,Application,ApplicationJob,Contactus
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name','Email','phone','location','bio','profile_pic','skills']

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Application)


class postjobAdmin(admin.ModelAdmin):
    list_display = ["job","company_name","location","job_type","salary_range","desc","posted_on"]
admin.site.register(postjob,postjobAdmin)

admin.site.register(ApplicationJob)
admin.site.register(Contactus)