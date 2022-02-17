from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from client.choices import HLE_CHOICES
from client.models import ProjectOrder
from django.core.validators import MaxValueValidator, MinValueValidator


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
        return "{} - {}".format(self.First_Name, self.username)


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
        return "{} - {}".format(self.project.title, self.made_by.username)

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

    class Meta:
        ordering = ['-upload_date']


class TestTask(models.Model):
    test_task = models.FileField(
        upload_to='test_tasks',
        help_text='Upload the completed test task here')
    username = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)


class Rating(models.Model):
    username = models.ForeignKey(
        User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0,
                                validators=[
                                    MaxValueValidator(5),
                                    MinValueValidator(0),
                                ]
                                )
    review = models.TextField(max_length=250, blank=True, null=True)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="review_user")

    def __str__(self):
        return str(self.username)
