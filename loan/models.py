from django.db import models
from datetime import datetime
# Create your models here.

class AddPayment(models.Model):
    loan_id = models.CharField(max_length=200)
    payment_fee = models.DecimalField(max_digits=10, decimal_places=0)
    transaction_id = models.CharField(max_length=200)
    reference = models.CharField(max_length=200)
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
    feedback = models.TextField(max_length=200)
    
    def __str__(self):
        return self.feedback


class AddPermitPayment(models.Model):
    permit_id = models.CharField(max_length=200, default='null')
    payment_fee = models.DecimalField(max_digits=20, decimal_places=2, default='0')
    phone_number = models.CharField(max_length=20, default='null')
    transaction_id = models.CharField(max_length=200, default='null')
    status = models.CharField(max_length=200, default='null')
    reference = models.CharField(max_length=200, default='null')
    date = models.DateTimeField(default=datetime.now, blank=True)
    admin = models.CharField(max_length=200, default='null')

    def __str__(self):
        return 'a request of ' + str(self.payment_fee) + ' from ' + str(self.permit_id)

