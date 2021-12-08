from django.db import models

# Contact us page model


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()

    def __str__(self):
        return self.email
