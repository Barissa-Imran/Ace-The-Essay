from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from .choices import (
    TYPE_OF_PAPER,
    PAPER_FORMAT,
    SUBJECT_CHOICES,
    ACADEMICS_LEVEL,
    HLE_CHOICES
)
from django.shortcuts import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='profile_pics/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # resize the image while saving
    def save(self, *args, **kwargs):
        super(Profile, self,).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


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
    number_of_pages = models.IntegerField()
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
    deadline = models.DateField(default=timezone.now)
    update_time = models.DateField(auto_now=True)
    username = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    complete = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    price = models.FloatField(default=4.0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={
            "slug": self.slug
        })

    class Meta:
        ordering = ['-date_posted']

# new applicant writer model


class Applicant(models.Model):
    username = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=128,)
    Last_Name = models.CharField(max_length=128,)
    Highest_Level_of_Education = models.CharField(
        max_length=3, choices=HLE_CHOICES)
    CourseField_of_Study = models.CharField(
        verbose_name='Course/Field of Study', max_length=250,)
    CV = models.FileField(verbose_name='C.V',
                          null=False,
                          blank=False,
                          upload_to='CVs',
                          help_text='Drag and drop or click to upload your cv'
                          )
    Identification = models.ImageField(default='profile_pics/default.jpg',
                                       upload_to='gov_id',
                                       help_text='scan of your government issued ID'
                                       )
    photo_id = models.ImageField(default='profile_pics/default.jpg',
                                 upload_to='photo_id',
                                 help_text='photo of you holding your ID'
                                 )

    def __str__(self):
        return self.First_Name + " - " + self.username


class Bid(models.Model):
    project = models.ForeignKey(
        ProjectOrder, default="null", on_delete=models.CASCADE)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        default="null",
        on_delete=models.CASCADE
    )
    date = models.DateField(auto_now_add=True)
    assign = models.BooleanField(default=False)

    def __str__(self):
        return self.project.title

    class Meta:
        ordering = ['-date']


class CompleteTask(models.Model):
    complete_task = models.FileField(
        upload_to='finals',
        help_text='upload the finished task here'
    )
    # set to project, delete all bids on complete project
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.bid.project.title


class TestTask(models.Model):
    test_task = models.FileField(
        upload_to='test_tasks',
        help_text='Upload the completed test task here')
    username = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
