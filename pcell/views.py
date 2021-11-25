import os
from . import posted
from django.shortcuts import render, redirect
from .models import company, Post
from users.models import Profile
from placement.models import application
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.
from pytz import timezone
from datetime import datetime


def pcell_index(request):
    all_companies = company.objects.filter(visited_year=datetime.now().year)
    companies_count=0
    average=0
    highest=0
    for comp in all_companies:
        companies_count+=1
        # average+=comp.company_ctc
        #if( comp.company_ctc > highest):
        #    highest=comp.company_ctc

    average=average/companies_count

    all_users = Profile.objects.all()
    offer = []
    placed=0
    for i in range(len(all_users)):
        if all_users[i].placed_in != 'NoOffer':
            placed+=1
            offer.append(all_users[i])

        

    return render(request, "pcell/index.html", {
        'companies_visited' : companies_count,
        'average': average,
        'highest':highest,
        'placed':placed
    })

def pcell_show_campus(request):
    return render(request, "pcell/show_campus.html")

def pcell_show_company(request):
    all_companies = company.objects.filter(visited_year=datetime.now().year)
    return render(request, "pcell/show_company.html", {'companies': all_companies})

def pcell_add_company(request):
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
        return render(request, "pcell/add_company.html")
    else:
        form = posted.CreateCompany()
        return render(request, "pcell/add_company.html",{'company': form})

def pcell_add_announcement(request):
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
            return render(request, "pcell/index.html")
    else:
        form = posted.CreatePost()
        return render(request, "pcell/add_announcement.html", {'post': form})

def pcell_add_stats(request):
    return render(request, "pcell/add_stats.html")

def pcell_company_view(request):
    return render(request, "pcell/company_view.html")

@login_required
def pcell_show_description(request, company_id):
    all_companies = company.objects.get(pk=company_id)
    return render(request, "pcell/show_description.html", {'companies': all_companies})


def pcell_announcement(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'pcell/announcement.html', context)