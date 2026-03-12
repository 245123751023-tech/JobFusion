from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

import cloudinary
import cloudinary.uploader

import os
from django.conf import settings
from django.http import HttpResponse

from django.utils import timezone
from datetime import date
from django.db.models import Q
from home.models import Profile,ApplicationJob,Contactus,Application,postjob,Posts,Requests
from firebase_config import firebase_db
from firebase_admin import storage
import cloudinary
import cloudinary.uploader

from ml.job_recommendation import recommend_jobs

from ml.post_recommendation import get_recommended_posts

def home_view(request):
    user = request.user
    job_facts = [
    # --- Workplace & Productivity ---
    "Standing meetings finish 30% faster and improve energy levels.",
    "Office plants reduce stress and increase productivity by 15%.",
    "Blue light exposure in offices helps workers stay alert.",
    "Taking micro-breaks every 20 minutes reduces fatigue.",
    "The average worker spends 28% of their day on email.",
    "Remote workers report being 13% more productive than in-office staff.",
    "Loud offices reduce concentration by up to 60%.",
    "Natural light in offices improves sleep quality for employees.",
    "90% of workers say ergonomic chairs improve focus.",
    "The average person checks work email 36 times per hour.",
    "Flexible work policies increase employee loyalty by 50%.",
    "Clutter-free desks are linked with faster task completion.",
    "Drinking water at work improves concentration by 14%.",
    "Workers exposed to nature views report 23% more satisfaction.",
    "Team lunches increase collaboration by 25%.",
    "Employees who nap at work show 34% higher alertness.",
    "Typing speed improves by 10% when using dual monitors.",
    "Workplace laughter reduces stress hormones immediately.",
    "Offices with standing desks see 12% higher productivity.",
    "Background noise from coffee shops improves creative thinking.",


    # --- Skills & Careers ---
    "Python is the most requested programming skill globally.",
    "Critical thinking is among the top 3 skills employers seek.",
    "Emotional intelligence is increasingly valued in leadership roles.",
    "Public speaking ranks as the most feared workplace skill.",
    "Project management certification raises salaries by 20%.",
    "AI literacy is now a requirement in many job descriptions.",
    "Cybersecurity skills earn premiums of 25% above average pay.",
    "Design thinking is taught in top MBA programs worldwide.",
    "Adaptability is ranked as the #1 future skill by employers.",
    "Coding bootcamps graduate over 100,000 students annually.",
    "Teamwork is mentioned in 60% of job postings.",
    "Excel remains one of the most in-demand business skills.",
    "Soft skills outweigh technical skills in 77% of hiring decisions.",
    "Data visualization expertise is sought in all industries.",
    "Digital literacy is a baseline requirement in 80% of careers.",
    "Negotiation training boosts sales performance by 30%.",
    "Emotional resilience reduces burnout risk significantly.",
    "Networking secures 70% of new career opportunities.",
    "AI engineers are among the top 5 highest-paid tech workers.",
    "Coding is taught in schools across 120+ countries.",

    # --- Workplace & Productivity (cont’d) ---
    "Standing desks reduce back pain for 54% of workers.",
    "Brainstorming in groups leads to 15% more ideas on average.",
    "Listening to instrumental music improves concentration.",
    "Writing to-do lists increases daily productivity by 25%.",
    "A messy desk can boost creativity but reduce accuracy.",
    "Emails written in the morning are 30% more polite.",
    "Video meetings longer than 45 minutes lower engagement sharply.",
    "Multitasking reduces efficiency by up to 40%.",
    "Workers exposed to daylight sleep 46 minutes longer at night.",
    "Aromatherapy in offices reduces stress in 70% of employees.",
    "Stretch breaks lower the risk of repetitive strain injuries.",
    "Daily journaling at work improves decision-making clarity.",
    "Water coolers remain top spots for informal collaboration.",
    "Wearing headphones signals 'do not disturb' to coworkers.",
    "Workers spend 2 hours daily recovering from distractions.",
    "Mindfulness programs cut workplace stress by 32%.",
    "Typing accuracy declines after 3 continuous hours of work.",
    "Task batching increases efficiency by nearly 25%.",
    "Remote workers save 8.5 hours weekly on commuting.",
    "Short emails get 40% faster replies than long ones.",

    # --- Job Market Trends (cont’d) ---
    "Data science remains one of the fastest-growing careers.",
    "Renewable energy jobs are projected to double by 2030.",
    "Pharmaceutical companies are among the top global employers.",
    "Digital marketing is now a core role in 80% of businesses.",
    "Machine learning engineers saw salaries rise 15% last year.",
    "Customer experience managers are in rising demand worldwide.",
    "By 2030, 85 million jobs may be displaced by automation.",
    "Logistics and supply chain roles are expanding globally.",
    "VR trainers are emerging as a professional niche.",
    "Esports coaching is now a recognized career path.",
    "Global consulting firms employ over 2 million workers.",
    "Teaching assistants are in highest demand in Asia.",
    "Biotech startups are creating thousands of new jobs annually.",
    "Hospitality is rebounding as one of the top hiring sectors.",
    "Remote healthcare monitoring created new job categories.",
    "Space exploration companies are hiring engineers worldwide.",
    "FinTech firms are the fastest recruiters in finance.",
    "Mobile app developers remain in high demand worldwide.",
    "Digital content creation is a leading freelance category.",
    "Global job seekers increasingly target remote-friendly firms.",

    # --- Corporate & Office Culture (cont’d) ---
    "Sweden tested a 6-hour workday with positive results.",
    "Some companies pay workers to take vacations.",
    "China has a 996 culture: 9 a.m. to 9 p.m., 6 days a week.",
    "Australian workers take more sick leave than global average.",
    "Friday dress-down policies started in Hawaii as 'Aloha Friday'.",
    "Over 20% of employees admit to napping at their desks.",
    "Corporate cafeterias boost employee satisfaction rates.",
    "Work anniversaries are celebrated in 60% of global firms.",
    "Mexico has one of the longest average workweeks worldwide.",
    "Flexible seating is replacing assigned office desks.",
    "U.S. workers spend 10 minutes a day making coffee at work.",
    "Nearly 80% of firms hold weekly status meetings.",
    "South Korea enforces a maximum 52-hour workweek.",
    "Office pets improve morale and reduce employee turnover.",
    "The U.K. was first to adopt casual Fridays in Europe.",
    "Many firms offer paid volunteer days to employees.",
    "Indian companies celebrate major festivals at workplaces.",
    "German firms often close offices early on Fridays.",
    "Free coffee is the most common workplace perk.",
    "Corporate gyms improve productivity by 15%.",

    # --- Skills & Careers (cont’d) ---
    "Java remains in the top 5 most in-demand coding languages.",
    "Employers value problem-solving above GPA scores.",
    "Creative thinking ranked #2 skill by World Economic Forum.",
    "Leadership training boosts promotion chances significantly.",
    "AI ethics is a growing area of professional specialization.",
    "Multilingual employees earn 10–15% more on average.",
    "Presentation design skills are in high demand across fields.",
    "Data analysis is expected to be critical in all careers by 2030.",
    "Time management training reduces project overruns by 25%.",
    "UX design jobs grew by 50% in the past five years.",
    "Negotiation is ranked the most undertrained workplace skill.",
    "Programming literacy improves job mobility across industries.",
    "Resume tailoring increases hiring chances by 40%.",
    "AI-assisted tools are now part of daily office workflows.",
    "Emotional intelligence boosts customer-facing performance.",
    "Agile project managers are highly sought after globally.",
    "Communication is ranked #1 in leadership hiring priorities.",
    "STEM graduates enjoy 20% lower unemployment rates.",
    "Digital storytelling is now a career in marketing.",
    "Curiosity is cited as a top skill for innovative companies.",

    # --- Motivational & Career Insights (cont’d) ---
    "Employees who take vacations return 40% more productive.",
    "Changing jobs often increases salary by 10–20%.",
    "Professional networking increases career longevity.",
    "Career growth depends more on mentors than luck.",
    "Job satisfaction is linked closely with physical health.",
    "Volunteer leadership roles improve career progression.",
    "Burnout affects over 50% of professionals worldwide.",
    "Remote employees report higher work-life balance.",
    "Salary transparency improves trust in companies.",
    "High performers often read at least one book per month.",
    "Workers who pursue side projects develop faster skills.",
    "People with creative hobbies are more innovative at work.",
    "Learning coding basics improves digital confidence.",
    "Career shifts often lead to unexpected satisfaction.",
    "Professionals who journal career goals achieve them faster.",
    "Half of global workers consider changing jobs annually.",
    "LinkedIn reports that 40% of users change jobs every 4 years.",
    "Work-life balance is a top priority for Gen Z professionals.",
    "Older workers are increasingly pursuing freelance careers.",
    "Happiness at work often predicts overall life happiness.",
]

    profile_object, _ = Profile.objects.get_or_create(user=request.user)
 
    from ml.job_recommendation    import recommend_jobs
    from ml.people_recommendation import recommend_people
 
    recommended_jobs = []
    suggested_people = []
 
    IS_JOB_SEEKER = profile_object.Role in ['Student', 'Intern', 'FreeLancer']
 
    # ── 1. ML Job Recommendations ─────────────────────────────────────────
    if IS_JOB_SEEKER and profile_object.skills:
        try:
            raw_jobs = recommend_jobs(
                user_skills   = profile_object.skills or '',
                user_job_type = 'Full Time',
                user_location = profile_object.location or '',
                top_n         = 10
            )
            if not raw_jobs.empty:
                job_ids   = raw_jobs['id'].tolist()
                score_map = dict(zip(raw_jobs['id'], raw_jobs['score']))
                for job in postjob.objects.filter(id__in=job_ids):
                    score = score_map.get(job.id, 0)
                    recommended_jobs.append({
                        'job':       job,
                        'score':     score,
                        'match_pct': int(score * 100),
                    })
                recommended_jobs.sort(key=lambda x: x['score'], reverse=True)
 
        except Exception as e:
            print(f"[JobRecommendation ERROR] {e}")
            # ── Fallback: your original keyword-based logic ────────────────
            fallback = []
            for skill in profile_object.skills.split(','):
                fallback.extend(
                    postjob.objects.filter(desc__icontains=skill.strip()) |
                    postjob.objects.filter(job__icontains=skill.strip())
                )
            seen = set()
            for j in fallback:
                if j.id not in seen:
                    recommended_jobs.append({'job': j, 'score': 0, 'match_pct': 0})
                    seen.add(j.id)
            recommended_jobs = recommended_jobs[:10]
 
    # ── 2. ML People Recommendations (all roles) ──────────────────────────
    try:
        raw_people = recommend_people(current_profile_id=profile_object.id, top_n=10)
 
        if raw_people:
            rec_ids   = [p['id'] for p in raw_people]
            score_map = {p['id']: p['score'] for p in raw_people}
 
            # Single DB query to get all request statuses
            all_requests = Requests.objects.filter(
                Q(sender=user) | Q(receiver=user)
            )
 
            for p in Profile.objects.filter(id__in=rec_ids).select_related('user'):
                is_friend = all_requests.filter(
                    Q(sender=user, receiver=p.user) | Q(sender=p.user, receiver=user),
                    IsFriend=True
                ).exists()
                request_sent = all_requests.filter(
                    sender=user, receiver=p.user, IsPending=True
                ).exists()
                request_received = all_requests.filter(
                    sender=p.user, receiver=user, IsPending=True
                ).exists()
 
                score = score_map.get(p.id, 0)
                suggested_people.append({
                    'profile':          p,
                    'score':            score,
                    'match_pct':        int(score * 100),
                    'is_friend':        is_friend,
                    'request_sent':     request_sent,
                    'request_received': request_received,
                })
 
            suggested_people.sort(key=lambda x: x['score'], reverse=True)
 
    except Exception as e:
        print(f"[PeopleRecommendation ERROR] {e}")
        # ── Fallback: your original skill-based people logic ───────────────
        if profile_object.skills:
            fallback = []
            all_requests = Requests.objects.filter(Q(sender=user) | Q(receiver=user))
            for skill in profile_object.skills.split(','):
                fallback.extend(
                    Profile.objects.filter(
                        skills__icontains=skill.strip()
                    ).exclude(user=user)
                )
            seen = set()
            for p in fallback:
                if p.id not in seen:
                    is_friend = all_requests.filter(
                        Q(sender=user, receiver=p.user) | Q(sender=p.user, receiver=user),
                        IsFriend=True
                    ).exists()
                    request_sent     = all_requests.filter(sender=user, receiver=p.user, IsPending=True).exists()
                    request_received = all_requests.filter(sender=p.user, receiver=user, IsPending=True).exists()
                    suggested_people.append({
                        'profile':          p,
                        'score':            0,
                        'match_pct':        0,
                        'is_friend':        is_friend,
                        'request_sent':     request_sent,
                        'request_received': request_received,
                    })
                    seen.add(p.id)
            suggested_people = suggested_people[:10]
 
    # ── 3. Posts ──────────────────────────────────────────────────────────
    posts = Posts.objects.all().order_by('-created_at')
    ranked_posts = get_recommended_posts(profile_object,posts)
    return render(request, "homepage.html", {
        'posts':            ranked_posts,
        'user':             user,
        'profile':          profile_object,
        'recommended_jobs': recommended_jobs,  # [{job, score, match_pct}]
        'suggested_people': suggested_people,  # [{profile, score, match_pct, is_friend, ...}]
        'jobfacts':         job_facts,
    })
 
from home.models import Requests

def viewothersprofile(request, userno):
    userdetail = get_object_or_404(Profile, id=userno)
    usersdata = []
    current_logined_user = request.user
    current_targeted_user = userdetail.user.email

    # here, i will Write the logic to send a mail to the current_targeted_user that,this currently_logined_user watched your profile.

    # Exclude both current user and the profile being viewed
    base_exclude = Profile.objects.exclude(user=request.user).exclude(id=userdetail.id)

    if userdetail.Role in ['Student','Intern','FreeLancer']:
        thispersonskills = [s.strip() for s in userdetail.skills.split(',')] if userdetail.skills else []
        thispersonbio = [b.strip() for b in userdetail.bio.split(',')] if userdetail.bio else []

        for skill in thispersonskills:
            usersdata.extend(base_exclude.filter(skills__icontains=skill))
        for bio_item in thispersonbio:
            usersdata.extend(base_exclude.filter(bio__icontains=bio_item))
    else:
        if userdetail.bio:
            for bio_item in userdetail.bio.split(','):
                usersdata.extend(base_exclude.filter(bio__icontains=bio_item.strip()))

    # Remove duplicates
    unique_users, seen_ids = [], set()
    for u in usersdata:
        if u.id not in seen_ids:
            unique_users.append(u)
            seen_ids.add(u.id)

    # ✅ Pass Requests table data for button logic
    reqsdata = Requests.objects.filter(
        sender=request.user
    ) | Requests.objects.filter(receiver=request.user)

    return render(
        request,
        "viewothersprofile.html",
        {
            'profile': userdetail,
            'usersdata': unique_users,
            'reqsdata': reqsdata,
        }
    )

def courses(request):
    return render(request,"courses.html",{})

def viewjob_view(request,job_id):
    job = get_object_or_404(postjob,id=job_id)
    return render(request,'viewjob.html',{'job':job})

def applyjob_view(request,job_id):
    job = get_object_or_404(postjob,id=job_id)
    user = request.user
    if Application.objects.filter(user=user,job=job).exists(): # If the user has already aplied to hte job
        messages.warning(request,"You have already applied for this job.")
        return redirect('viewjob',job_id=job_id)

    profile_object,created = Profile.objects.get_or_create(user=request.user)
    if not profile_object.resume: # Means no Resume with user
        result_from_applyjobview = "Please Upload your Resume/Cv to apply for the Job!"
        return render(request,"uploadresume.html",{'result_from_applyjobview':result_from_applyjobview})

    if not profile_object.skills: # Means no Skills with User
        result_from_applyjobview = "Please Complete Your Profile to Apply for the job"
        return render(request,"profile.html",{'result_from_applyjobview':result_from_applyjobview})


    app_obj,app_created = Application.objects.get_or_create(
        user=request.user,
        job=job,
        posted_by = str(job.user),
        #posted_by = job.posted_by)
        defaults={
            'applied_on':timezone.now()
                }
        )

    appjob_obj,appjob_created = ApplicationJob.objects.get_or_create(
        user=request.user,
        job=job,
        defaults={
            'applied_on':timezone.now()
                }
        )
    app_obj.save()
    appjob_obj.save()
    print(app_created)
    print(appjob_created)
    if app_created and appjob_created:
        messages.success(request,'Applied successfully !')
    else:
        messages.error(request,'You have already applied for this job!')

    return redirect('viewjob',job_id=job.id)

def profile_edit_view(request):
    user = request.user
    profile_object,created = Profile.objects.get_or_create(user=request.user)
    if(request.method=='POST'):
        user.email = request.POST.get("Email")
        user.save()

        profile_object.full_name = request.POST.get('full_name')
        profile_object.phone = request.POST.get('phno')
        profile_object.location = request.POST.get('location')
        profile_object.bio = request.POST.get('bio')
        profile_object.skills = request.POST.get('skills')

        # Handling File uploads in to dB
        if(request.FILES.get('profile_pic')):
            profile_object.profile_pic = request.FILES.get('profile_pic')

        if(request.FILES.get('resume')):
            profile_object.resume = request.FILES.get('resume')

        profile_object.save()
        messages.success(request,"Profile Updated Successfully !")
        return redirect('profile')

    return render(request,'profile_edit.html',{'user':user,'profile':profile_object})

def appliedpeople_view(request):
    user = request.user
    jobs_posted_by_hr = postjob.objects.filter(posted_by=request.user)
    print("DEGUG:Jobs posted by current HR:",list(jobs_posted_by_hr))
    applications = Application.objects.filter(job__posted_by = request.user)
    #applications = Application.objects.filter(job__user=request.user)
    #print("DEGUG:Applications found:",list(applications))
    return render(request,'appliedpeople.html',{'applications':applications})

import datetime

def profile_view(request):
    profile_data=None
    user = request.user
    profile_object,created = Profile.objects.get_or_create(user=request.user)
    print(profile_object)
    return render(request,'profile.html',{'profile':profile_object})

def job_list_view(request):
    query = ""
    jobs_data = postjob.objects.all()
    user = request.user
    profile_object,k = Profile.objects.get_or_create(user=request.user)
    if(profile_object.Role!='Student' and  profile_object.Role!='Intern' and profile_object.Role!='FreeLancer'):
        jobs_data_for_posted_people = postjob.objects.filter(user=request.user)
        print(jobs_data_for_posted_people)
        print("yaaaaaaaaaaaaaaho i am going to front now",profile_object.Role)
        return render(request,"jobs.html",{'jobs_data':jobs_data_for_posted_people,'profile':profile_object})

    # Below code for Searching feature
    if(request.method=='POST'):
        query = request.POST.get('key')

        if(query):
            jobs_data = postjob.objects.filter(
                Q(location__icontains=query)|
                Q(job__icontains=query)|
                Q(company_name__icontains=query)|
                Q(job_type__icontains=query)|
                Q(salary_range__icontains=query)|
                Q(desc__icontains=query)|
                Q(posted_on__icontains=query)
            ).distinct()
    return render(request,"jobs.html",{'jobs_data':jobs_data})

def postjob_view(request):
    jobpostedsuccessmsg = None
    if(request.method=='POST'):
        user = request.user
        job_title =  request.POST.get('jobtitle')
        print('Posted Job:',job_title)
        company_name = request.POST.get('companyname')
        location = request.POST.get('location')
        jt = request.POST.get('jobtype')
        print('job type=============',jt)
        # job_type = request.POST.get('jobtype')
        salary_range = request.POST.get('salary_range')
        desc= request.POST.get('desc')
        req = request.POST.get('req')
        posted_on = timezone.now()

        postjob.objects.create(
            user = request.user,
            job=job_title,
            company_name=company_name,
            location = location,
            job_type = jt,
            salary_range = salary_range,
            desc = desc,
            req = req,
            posted_by = request.user,
            posted_on = posted_on
        )

        messages.success(request, "Job Posted Successfully-!")
        #jobpostedsuccessmsg =  "Job Posted Successfully-!"
        print("I am in UNder Success---------------------------")
        return redirect('postjobs')

    return render(request,"postjob.html",{})

def deljob(request,jobid):
    job = get_object_or_404(postjob,pk=jobid)
    job.delete()
    return redirect("joblistings")

def myapplications_view(request):
    user = request.user
    app_obj = Application.objects.filter(user=request.user)
    print(app_obj)
    return render(request,"applications.html",{'app_obj':app_obj})

def deleteresume_view(request):
    user = request.user
    profile_object,created = Profile.objects.get_or_create(user=request.user)

    if(profile_object.resume):
        profile_object.resume.delete(save=False)
        profile_object.resume = None
        profile_object.save()
        messages.success(request,"Resume Deleted SUccessfull-Y!")
    return redirect("resumes")


def uploadresume_view(request):
    user = request.user
    profile_object,created = Profile.objects.get_or_create(user=request.user)
    if(request.method=='POST'):
        user = request.user
        profile_object,created = Profile.objects.get_or_create(user=request.user)
        resume = request.FILES.get("resume")
        print(resume)
        profile_object.resume = resume
        profile_object.save()
        result = "Resume Uploaded Successfully!."
        messages.success(request,"Resume Uploaded Successfully !")
        print(profile_object.resume)
        # print(profile_object.resume.url)
        return render(request,"uploadresume.html",{'profile':profile_object,'result':result})
    return render(request,"uploadresume.html",{'profile':profile_object})

def contactus_view(request):
    if(request.method=='POST'):
        user = request.user
        contactus_object,k = Contactus.objects.get_or_create(user=request.user)

        contactus_object.name = request.POST.get('name')
        contactus_object.phno = request.POST.get('phno')
        contactus_object.Email = request.POST.get('Email')
        contactus_object.msg = request.POST.get('msg')

        contactus_object.save()
        messages.success(request,"Message Sent  Successfully!")
        #redirect('contactus')
        result = "Message Sent  Successfully!"
        return render(request,'contactus.html',{'result':result})
    return render(request,'contactus.html',{})

def chat_with_user(request, username):
    return render(request, 'chat.html', {'username': username})


def connections(request):
    user = request.user

    # Friends: Requests where IsFriend=True and either sender or receiver is current user
    friends_qs = Requests.objects.filter(IsFriend=True).filter(Q(sender=user) | Q(receiver=user))

    # Build a deduplicated list of the *other* user for each friends request
    friends_seen = set()
    friends = []
    for req in friends_qs.select_related('sender__profile', 'receiver__profile'):
        other = req.receiver if req.sender == user else req.sender
        if other and other.id not in friends_seen:
            friends.append(other)
            friends_seen.add(other.id)

    # Pending requests sent by current user (outgoing)
    pending_out_qs = Requests.objects.filter(sender=user, IsPending=True, IsFriend=False)
    pending_out_seen = set()
    pending_out = []
    for req in pending_out_qs.select_related('receiver__profile'):
        other = req.receiver
        if other and other.id not in pending_out_seen:
            pending_out.append(other)
            pending_out_seen.add(other.id)

    # Incoming requests (sent to current user)
    incoming_qs = Requests.objects.filter(receiver=user, IsPending=True, IsFriend=False)
    incoming_seen = set()
    incoming = []
    for req in incoming_qs.select_related('sender__profile'):
        other = req.sender
        if other and other.id not in incoming_seen:
            incoming.append(other)
            incoming_seen.add(other.id)

    # Build excluded user ids: friends + pending_out + incoming + current user
    excluded_ids = set(friends_seen) | set(pending_out_seen) | set(incoming_seen) | {user.id}

    # All other profiles excluding excluded users
    others = Profile.objects.exclude(user__id__in=excluded_ids).select_related('user')

    context = {
        'friends': friends,
        'pending_out': pending_out,
        'incoming': incoming,
        'others': others,
    }
    return render(request, 'connections.html', context)


def accept(request, sender_id):
    """Accept an incoming request from sender_id (sender_id is a User.id)."""
    receiver = request.user
    sender = get_object_or_404(User, id=sender_id)

    # Find the pending request (sender -> receiver)
    req = get_object_or_404(Requests, sender=sender, receiver=receiver, IsPending=True)

    # Make it friend and clear pending
    req.IsPending = False
    req.IsFriend = True
    req.save()

    messages.success(request, f"You are now connected with {sender.username}.")
    return redirect('connections')

def reject(request, sender_id):
    """Reject (delete) an incoming request from sender_id"""
    receiver = request.user
    sender = get_object_or_404(User, id=sender_id)

    # Delete the pending request if exists
    req_qs = Requests.objects.filter(sender=sender, receiver=receiver, IsPending=True)
    if req_qs.exists():
        req_qs.delete()
        messages.info(request, f"Request from {sender.username} rejected.")
    else:
        messages.warning(request, "No pending request found to reject.")

    return redirect('connections')


def send_request(request, profile_id):
    """Send a connection request to a profile's user (profile_id is Profile.id)."""
    sender = request.user
    profile = get_object_or_404(Profile, id=profile_id)
    receiver = profile.user

    # Prevent sending to self
    if receiver == sender:
        messages.error(request, "You cannot connect to yourself.")
        return redirect('connections')

    # Check existing relationship
    existing = Requests.objects.filter(
        (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
    ).first()

    if existing:
        if existing.IsFriend:
            messages.info(request, "You are already connected.")
        elif existing.IsPending:
            # if they already sent you a request, suggest accepting instead
            if existing.sender == receiver:
                messages.info(request, f"{receiver.username} already sent you a request — accept from Incoming Requests.")
            else:
                messages.info(request, "Request already sent.")
    else:
        Requests.objects.create(sender=sender, receiver=receiver, IsPending=True, IsFriend=False)
        messages.success(request, "Connection request sent.")

    return redirect('connections')


def myposts(request):
    posts = Posts.objects.filter(user=request.user).order_by("-created_at")

    if(request.method=='POST'):
        caption = request.POST.get('caption')
        file = request.FILES.get('file')
        description = request.POST.get("desc")

        media_url = None
        media_type = None

        if file:
            print("i am here----------1")
            try:
                print("i am here----------2")
                # Upload to Cloudinary
                print(" 🚀 BEFORE UPLOAD")
                upload_result = cloudinary.uploader.upload(file,resource_type="auto",timeout=10)
                print(" 🚀 AFTER UPLOAD")
                print("i am here----------after upload_result")
                media_url = upload_result.get('secure_url')
                print("i am here----------aftyer media url")
                # type detection
                content_type = file.content_type
                if file.content_type.startswith('image'):
                    media_type = 'image'
                elif file.content_type.startswith('video'):
                    media_type = 'video'
                else:
                    media_type = 'unknown'
                
                print("i am here----------3;at the end")
            except Exception as e:
                print("i am here----------4")
                print("Cloudinary Upload Failed:", e)
                messages.error(request, "Failed to upload media. Please try again.")
                print("i am here----------5,at error")
                return redirect('myposts')

        Posts.objects.create(
            user = request.user,
            caption = caption,
            description = description,
            media_url = media_url,
            media_type = media_type
        )

        messages.success(request,"Post Uploaded Successfully!")
        print("i am here----------redirecting to myposts")
        return redirect('myposts')
    print("i am here----------simply rendering html page")
    return render(request,'myposts.html',{'posts':posts})



def delete_post_view(request,postid):
    if request.method=='POST':
        post = get_object_or_404(Posts,pk=postid,user=request.user)
        post.delete()
        messages.success(request, "Post deleted successfully!")
        
        return redirect('myposts')
    return render(request,"")

def like_post(request,postid):
    post = get_object_or_404(Posts,id=postid)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        try:
            post.dislikes.remove(request.user)
        except Exception:
            pass
    
    if request.user.username == post.user.username:
        return redirect('myposts')

    return redirect('home')

def dislike_post(request,postid):
    post = get_object_or_404(Posts,id=postid)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        try:
            post.likes.remove(request.user)
        except Exception:
            pass

    if request.user.username == post.user.username:
        return redirect('myposts')

    return redirect('home')


#Comments model regarding

from ml.predict import predict_toxic
from .models import Comment

def PostComment(request,postid):
    user = request.user
    post = get_object_or_404(Posts,pk=postid)
    usercomment = request.POST.get("usercomment")
    if not usercomment:
        messages.error(request,"Comment cannot be empty")
        return redirect("home")
    
    prediction = predict_toxic(usercomment)
    if prediction==0: #if comment is safe
        Comment.objects.create(
            post=post,
            user=user,
            text=usercomment
        )
    else:
        messages.error(request,"Your comment is harmful.")
    
    return redirect('home')

def view_post(request, postid):
    post = get_object_or_404(Posts, pk=postid)

    comments = Comment.objects.filter(post=post)

    return render(request, "post_detail.html", {
        "post": post,
        "comments": comments
    })



def airesume(request):
    profile_obj,k = Profile.objects.get_or_create(user=request.user)
    print(type(profile_obj))
    return render(request,'AiResume.html',{'profile':profile_obj})

# views.py
import json
import requests
from django.http import JsonResponse

def enhance_section(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "")

            # Prompt for AI
            prompt = (
                "Enhance the following resume professionally:\n"
                f"{text}\n\n"
                "Follow these instructions strictly:\n"
                "1. Use these section headings exactly: Name, Career Objective, Bio, Skills, "
                "Graduation Details, Intermediate Details, School Details, Projects, Experience, Certifications, Contact\n"
                "2. Only use the words provided in the text to construct meaningful, professional sentences.\n"
                "3. If a field like Bio or Career Objective is empty, create it using other details in the text.\n"
                "4. Return only the enhanced text, keep headings exactly as above.\n"
                "5. Format should be clean and professional, do not add extra suggestions or comments."
            )

            # RapidAPI GPT call
            url = "https://chatgpt-42.p.rapidapi.com/chat"
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": "e8b8f6f566mshd40c285a27eaec1p1108d0jsn06475eb84d40",
                "X-RapidAPI-Host": "chatgpt-42.p.rapidapi.com"
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}]
            }

            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            enhanced_text = result['choices'][0]['message']['content']

            return JsonResponse({"enhanced": enhanced_text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)




api = "e8b8f6f566mshd40c285a27eaec1p1108d0jsn06475eb84d40"