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
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
from pytz import timezone
from datetime import datetime


def pcell_index(request):
    all_companies = company.objects.filter(visited_year=datetime.now().year)
    companies_count = 0
    for comp in all_companies:
        companies_count += 1

    average = 0
    highest = 0
    all_users = Profile.objects.all()
    offer = []
    placed = 0
    for i in range(len(all_users)):
        if all_users[i].placed_in != 'NoOffer':
            placed += 1
            comp = all_companies.get(company_name=all_users[i].placed_in)
            average += comp.company_ctc
            average = average // placed
            if(comp.company_ctc > highest):
                highest = comp.company_ctc
            offer.append(all_users[i])

    return render(request, "pcell/index.html", {
        'companies_visited': companies_count,
        'average': average,
        'highest': highest,
        'placed': placed
    })

# def pcell_add_stats(request):
#     all_users = Profile.objects.all()
#     offer = []
#     IT_placed=0
#     ECE_placed=0
#     DUAL_placed=0
#     placed=0
#     for i in range(len(all_users)):
#         if all_users[i].placed_in != 'NoOffer' :
#             placed+=1
#             offer.append(all_users[i])
#             if all_users[i].stream=='IT':
#                 IT_placed+=1
#             if all_users[i].stream=='ECE':
#                 ECE_placed+=1
#             if all_users[i].stream=='DUAL':
#                 DUAL_placed+=1

#     return render(request, "pcell/add_stats.html", {
#         'placed':placed,
#         'IT_placed':IT_placed,
#         'ECE_placed':ECE_placed,
#         'DUAL_placed':DUAL_placed
#     })


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
        current_site = get_current_site(request)
        mail_subject = 'New Compay Added On Placement Portal'
        message = render_to_string('pcell/company_email.html', {
            'domain': current_site.domain,
            'company_name': company_name,
        })
        to_email = []
        for user in User.objects.all():
            to_email.append(user.email)
        email = EmailMessage(
            mail_subject, message, to=to_email
        )
        email.send()
        messages.info(request, "Company Added Successfully")
        print("Company :"+company_name +
              " has been successfully added to the database")
        return render(request, "pcell/add_company.html")
    else:
        form = posted.CreateCompany()
        return render(request, "pcell/add_company.html", {'company': form})


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
            current_site = get_current_site(request)
            mail_subject = 'New Announcement Added On Placement Portal'
            message = render_to_string('pcell/announcement_email.html', {
                'domain': current_site.domain,
            })
            to_email = []
            for user in User.objects.all():
                to_email.append(user.email)
            email = EmailMessage(
                mail_subject, message, to=to_email
            )
            email.send()
            messages.info(request, "Post Added Successfully")
            form = posted.CreatePost()
            return render(request, "pcell/add_announcement.html", {'post': form})
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
