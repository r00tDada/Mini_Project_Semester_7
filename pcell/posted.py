from django import forms
from . import models


class CreatePost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'content', 'author']

class CreateCompany(forms.ModelForm):
    class Meta:
        model = models.company
        fields = ['company_name', 'company_location', 'company_ctc',
        'company_category','job_profile','job_eligibility','job_skills','job_details']