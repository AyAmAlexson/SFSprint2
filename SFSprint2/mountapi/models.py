from django.db import models


class User(models.Model):
   email = models.EmailField()
   phone = models.CharField(max_length=15)
   name = models.CharField(max_length=30)
   fam = models.CharField(max_length=30)
   otc = models.CharField(max_length=30)

class MountainPass(models.Model):
   beauty_title = models.CharField(max_length=255)
   title = models.CharField(max_length=255)
   other_titles = models.CharField(max_length=255)
   connect = models.TextField(blank=True)
   add_time = models.DateTimeField()
   user = models.ForeignKey('User', on_delete=models.CASCADE)
   coord = models.JSONField(default=dict)
   level = models.JSONField(default=dict)
   status_choices = [('new', 'New'), ('approved', 'Approved'), ('rejected', 'Rejected')]
   status = models.CharField(max_length=10, choices=status_choices, default='new')

class Image(models.Model):
   mountain_pass = models.ForeignKey(MountainPass, related_name='images', on_delete=models.CASCADE)
   data = models.ImageField()
   title = models.CharField(max_length=255)
