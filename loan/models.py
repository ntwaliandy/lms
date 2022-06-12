from django.db import models
from datetime import datetime
# Create your models here.

class AddPayment(models.Model):
    loan_id = models.CharField(max_length=200)
    payment_fee = models.DecimalField(max_digits=10, decimal_places=0)
    transaction_id = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now, blank=True)
    admin = models.CharField(max_length=200)

    def __str__(self):
        return self.loan_id + ' ' + 'paid ' + str(self.payment_fee)

class GroupAddPayment(models.Model):
    loan_id = models.CharField(max_length=200)
    payment_fee = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=200)
    paid = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now, blank=True)
    admin = models.CharField(max_length=200)

    def __str__(self):
        return self.loan_id + ' ' + 'paid ' + str(self.payment_fee)
    
class Replies(models.Model):
    question_id = models.IntegerField()
    feedback = models.TextField(max_length=100000)
    
    def __str__(self):
        return self.feedback

