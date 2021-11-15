import os
from . import posted
from django.shortcuts import render, redirect
from .models import company, Post, application
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.
from pytz import timezone
from datetime import datetime


def index(request):
    return render(request, "placement/index.html")


def show_campus(request):
    return render(request, "placement/show_campus.html")


def show_company(request):
    all_companies = company.objects.all()
    if request.user.is_authenticated:
        try:
            entry = application.objects.get(name=request.user)
        except ObjectDoesNotExist:
            entry = application(name=request.user)
            entry.save()
        applied_applications = entry.applied_to.all()
    else:
        applied_applications = []
    return render(request, "placement/show_company.html", {
        'companies': all_companies,
        'applied_applications': applied_applications,
    })


def add_company(request):
    if request.method == "POST":
        company_name = request.POST['company_name']
        company_location = request.POST['location']
        company_ctc = request.POST['ctc']
        company_category = request.POST['category']
        job_profile = request.POST['profile']
        job_eligibility = request.POST['eligibility']
        job_skills = request.POST['skills']
        job_details = request.POST['details']
        print(company_name, company_location, company_ctc, company_category,
              job_profile, job_eligibility, job_skills, job_details)
        adcomp = company(company_name=company_name, company_location=company_location,
                         company_ctc=company_ctc, company_category=company_category, job_profile=job_profile, job_eligibility=job_eligibility, job_skills=job_skills, job_details=job_details)
        adcomp.save()
        print("Company :"+company_name +
              " has been successfully added to the database")
    return render(request, "placement/add_company.html")


def add_announcement(request):
    if request.method == "POST":
        form = posted.CreatePost(request.POST)
        if form.is_valid():
            # save post to db
            pt = form.save(commit=False)
            pt.date_posted = datetime.now(
                timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
            pt.author = request.user
            # print(pt.title, pt.content, pt.date_posted, pt.author)
            ptt = Post(title=pt.title, content=pt.content,
                       date_posted=pt.date_posted, author=pt.author)
            ptt.save()
            return render(request, "placement/index.html")
    else:
        form = posted.CreatePost()
        return render(request, "placement/add_announcement.html", {'post': form})


def resume(request):
    os.system("python3 Resume_Matcher/fileReader.py")
    # os.system("streamlit run Resume_Matcher/app.py")
    return redirect("http://localhost:8502/")


def add_stats(request):
    return render(request, "placement/add_stats.html")


def company_view(request):
    return render(request, "placement/company_view.html")


@login_required
def show_description(request, company_id):
    # print(company_id)
    all_companies = company.objects.get(pk=company_id)
    return render(request, "placement/show_description.html", {'companies': all_companies})


def announcement(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'placement/announcement.html', context)


@login_required
def apply_job(request, company_id):
    current_user = request.user
    print(current_user)
    comp = company.objects.get(pk=company_id)

    try:
        entry = application.objects.get(name=current_user)
    except ObjectDoesNotExist:
        entry = application(name=current_user)
        entry.save()
    if comp in entry.applied_to.all():
        messages.success(request, 'You have ALREADY applied to ' +
                         comp.company_name + ' job profile')
    else:
        entry.applied_to.add(comp)
        messages.success(request, 'You have applied to ' +
                         comp.company_name + ' job profile')

    all_companies = company.objects.all()
    return redirect('show_company')


@login_required
def your_app(request):
    try:
        app = application.objects.get(name=request.user)
    except ObjectDoesNotExist:
        app = []
    return render(request, "placement/your_app.html", {'apps': app})
