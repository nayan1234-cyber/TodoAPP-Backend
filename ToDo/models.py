from django.db import models
from django.contrib.auth.models import User

'''
==> choice ma ('C', 'COMPLETED') lakhvi ema.... data base ma 'C' store thay and user jyare set kare selection ma tyare 'COMPLETED' aa store thay.
==> choice eee apde Django form banavi emaj use thay baki ma use na thay always frist elements use thay if we not work in any django related form like react js form
'''

class TODO(models.Model):
    status_choice = [
        ('0', 'PENDING'),
        ('1', 'COMPLETED'),
    ]

    priority_choice = [
        ('1', '1'), 
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]

    user  = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=2 , choices=status_choice)
    date = models.DateTimeField(auto_now_add=True) # aamaa auto_now_add eee data-time apoapp store kare database ma
    priority = models.CharField(max_length=2, choices=priority_choice)