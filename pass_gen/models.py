from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserDetails(models.Model):
    sno = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    phone_no = models.TextField()
    email = models.TextField()
    date_of_birth = models.DateField()
    username = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name



class UserPasswords(models.Model):
    sno = models.AutoField(primary_key=True)
    username = models.TextField()
    password = models.TextField()
    for_site = models.TextField()

    def __str__(self) -> str:
        return self.username + self.for_site