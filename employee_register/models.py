from django.db import models
from django.utils import timezone

# Create your models here.

class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    emp_id = models.CharField(max_length=6)
    asset_tag = models.CharField(max_length=50)
    model = models.CharField(max_length=50, default='Unknown')
    duration = models.CharField(max_length=50)
    status = models.CharField(max_length=10, default='Pending')
    return_by = models.CharField(max_length=40, default='N/A')
    created_at = models.DateTimeField()

class Staff(models.Model):
    fullname = models.CharField(max_length=100)
    emp_id = models.CharField(max_length=6)
    sex = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    department = models.CharField(max_length=30)
    
class Equipment(models.Model):
    asset_tag = models.CharField(max_length=10)
    display_name = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=40)
    model = models.CharField(max_length=100)
    quantity = models.CharField(max_length=20)
    asset_type = models.CharField(max_length=50)
    
class BotDetail(models.Model):
    token = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=20)
    last_modify = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Bot Token: {self.token} | Chat ID: {self.chat_id}"