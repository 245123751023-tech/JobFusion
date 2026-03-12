import os 
os.environ.setdefault("DJANGO_SETTINGS_MODULE","jobfusion.settings")
import django
django.setup()

from faker import Faker
from random import *

from home.models import *

fake = Faker()
def phnogen():
    d1 = randint(6,9)
    num = ' ' + str(d1)
    for i in range(9):
        num += str(randint(0,9))
    return int(num)

def populate(n):
    for i in range(n):
        fdate = fake.date()
        fcompany = fake.company()
        ftitle = fake.random_element(elements=("project manager","Team Lead","Software engineer"))
        flocation = fake.address()
        fsal = fake.random_element(elements=(1000,10,000,125000,200000,250000,50000,70000,40000,35000))
        fjobtype = fake.random_element(elements=("Intern","Full time","Part Time",'only night shifts'))
        fphno = phnogen()
        fposted_on = fake.random_element(elements=("Oct",'nov',"feb","dec","apr","jan",'july','sep'))
        fdesc = fake.random_element(elements=("Good Company","Bad behaviour","High salaries","Low mainatance","No respect","High stipend",'Worst manager',"Great employees"))
        jobs_records = postjob.objects.get_or_create(job=ftitle,company_name = fcompany,location=flocation,job_type=fjobtype,salary_range = fsal,desc=fdesc,posted_on=fposted_on)


populate(50)