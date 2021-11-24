from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class company(models.Model):
    company_name = models.CharField(max_length=100)
    company_location = models.CharField(max_length=100)
    company_ctc = models.CharField(max_length=100)
    company_category = models.CharField(max_length=100)
    job_profile = models.CharField(max_length=100)
    job_eligibility = models.CharField(max_length=100)
    job_skills = models.CharField(max_length=100)
    job_details = models.TextField()

    def __str__(self):
        return self.company_name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})