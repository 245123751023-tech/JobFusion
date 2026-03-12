import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobfusion.settings')
django.setup()

from django.contrib.auth.models import User
from home.models import postjob

df = pd.read_csv('ml/cjobs.csv')

admin_user = User.objects.get(username='Praveen')

for _, row in df.iterrows():
    postjob.objects.create(
        user=admin_user,
        job=row['Job Title'],
        company_name=row['Industry'],
        location=row['Location'],
        job_type=row['Functional Area'],
        salary_range=row['Job Salary'],
        desc=row['Industry'],
        req=row['Key Skills'],
        posted_by=admin_user.username,
    )

print("Done! Jobs imported:", len(df))