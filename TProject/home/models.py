from django.db import models

# Create your models here.
class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    phone=models.CharField(max_length=14)
    content=models.TextField()
    TimeDate=models.DateField(auto_now_add=True,blank=True)

    def __str__(self):
        return 'Message from'+" "+ self.name + '-' + self.email 


    