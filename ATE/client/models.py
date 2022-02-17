from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .choices import (
    TYPE_OF_PAPER,
    PAPER_FORMAT,
    SUBJECT_CHOICES,
    ACADEMICS_LEVEL,
)
from django.shortcuts import reverse


class ProjectOrder(models.Model):
    academic_level = models.CharField(max_length=20, choices=ACADEMICS_LEVEL,)
    type_of_paper = models.CharField(max_length=50, choices=TYPE_OF_PAPER)
    subject_area = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    title = models.CharField(max_length=250)
    paper_instructions = models.TextField()
    Additional_materials = models.FileField(
        null=True, blank=True,
        # widget= models.ClearableFileInput(attrs={'multiple': True}),
        help_text='Please upload any additional files here! ZIP multiple files'
    )
    paper_format = models.CharField(max_length=50, choices=PAPER_FORMAT)
    number_of_pages = models.IntegerField(help_text='0 words approx')
    spacing = models.CharField(
        max_length=50,
        choices=[
            ('single', 'Single spaced'),
            ('double', 'Double spaced')
        ])
    currency = models.CharField(
        max_length=50, default='$', help_text='currency is always in US dollars')
    date_posted = models.DateTimeField(
        default=timezone.now, help_text="This is an automatically generated field, don't fill in")
    deadline = models.DateTimeField(default=timezone.now)
    update_time = models.DateField(auto_now_add=True)
    username = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    complete = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    price = models.FloatField(
        default=0.0, help_text="This field is auto-generated hence cannot be changed")

    def __str__(self):
        return "{} - {}".format(self.title, self.username)

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={
            "slug": self.slug
        })

    class Meta:
        ordering = ['-date_posted']
