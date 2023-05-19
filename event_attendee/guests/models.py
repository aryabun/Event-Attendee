from django.db import models
# Create your models here.

class Csv(models.Model):
    file_name =  models.FileField(upload_to="files")
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"
    
class Guest(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField()

class UpcomingInput(models.Model):
    STATUS = (
        (1, 'Coming'),
        (2, 'Not Coming'),
    )
    phone_number = models.CharField() #Using Regex to validate only integer
    timestamps = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS,default=2,)
    # status = 