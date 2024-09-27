from django.db import models

class Books(models.Model):
    title=models.CharField(max_length=100)
    page_number=models.IntegerField()
    publish_date=models.DateField(default='2022-01-01')
    stock=models.IntegerField()
    
