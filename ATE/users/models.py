from django.db import models
from django.db.models.expressions import F
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from .choices import TYPE_OF_PAPER, PAPER_FORMAT, SUBJECT_CHOICES, ACADEMICS_LEVEL, HLE_CHOICES


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
    subject_Area = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    title = models.CharField(max_length=250)
    paper_instructions = models.TextField()
    Additional_materials = models.FileField(
        # widge= models.ClearableFileInput(attrs={'multiple': True}),
        help_text='Please upload any additional files here! ZIP multiple files'
    )
    paper_format = models.CharField(max_length=50, choices=PAPER_FORMAT)
    number_of_pages = models.IntegerField()
    spacing = models.CharField(
        max_length=50,
        choices=[
            ('Null', '*Select'),
            ('single', 'Single spaced'),
            ('double', 'Double spaced')
        ])
    currency = models.CharField(max_length=50, default='$', help_text='currency is always in US dollars')
    date_posted = models.DateTimeField(default=timezone.now, help_text="This is an automatically generated field, don't fill in")
    # price = models.FloatField(editable=False)

    def __str__(self):
        return self.title

# new applicant writer model


class Applicant(models.Model):
    First_Name = models.CharField(max_length=50,)
    Last_Name = models.CharField(max_length=50,)
    Highest_Level_of_Education = models.CharField(max_length=3, choices=HLE_CHOICES)
    CourseField_of_Study = models.CharField(max_length=250,)
    CV = models.FileField(verbose_name='C.V',
                          null=False,
                          blank=False,
                          help_text='Drag and drop or click to upload your cv'
    )

    def __str__(self):
        return self.First_Name