from django.db import models
from datetime import datetime
# Create your models here.
import random

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

class FileUpload(models.Model):
    permit_id = models.CharField(max_length=200, default='null')
    uploaded_file = models.FileField()
    message = models.TextField(default='null')
    admin = models.CharField(max_length=30, default='null')
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.message + ' for PERMIT ID => ' + str(self.permit_id)



# Create your models here.
def random_string():
    return str(random.randint(10000, 99999))

# creating a record
class BodaApply(models.Model):
    boda_id = models.CharField(default=random_string, max_length=200, unique=True)
    boda_guy_firstName = models.CharField(max_length=40, default='null')
    boda_guy_lastName = models.CharField(max_length=40, default='null')
    boda_numberPlate = models.CharField(max_length=10, default='null')
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default='0')
    deposits = models.DecimalField(max_digits=12, decimal_places=2, default='0')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default='0')
    weekly_pay = models.DecimalField(max_digits=12, decimal_places=2, default='0')
    phone_number = models.CharField(max_length=15, default='null')
    nin_number = models.CharField(max_length=30, default='null')
    nin_picture = models.FileField()
    work_stage = models.CharField(max_length=30, default='null')

    guarantor1_name = models.CharField(max_length=30, default='null')
    guarantor1_stage_name = models.CharField(max_length=30, default='null')
    guarantor1_number = models.CharField(max_length=15, default='null')
    guarantor1_nin = models.CharField(max_length=30, default='null')
    guarantor1_nin_picture = models.FileField()

    guarantor2_name = models.CharField(max_length=30, default='null')
    guarantor2_stage_name = models.CharField(max_length=30, default='null')
    guarantor2_number = models.CharField(max_length=15, default='null')
    guarantor2_nin = models.CharField(max_length=30, default='null')
    guarantor2_nin_picture = models.FileField()

    guarantor3_name = models.CharField(max_length=30, default='null')
    guarantor3_stage_name = models.CharField(max_length=30, default='null')
    guarantor3_number = models.CharField(max_length=15, default='null')
    guarantor3_nin = models.CharField(max_length=30, default='null')
    guarantor3_nin_picture = models.FileField()
    latest_dateOfPay = models.CharField(max_length=30, blank=True)
    date_of_application = models.DateTimeField(default=datetime.now, blank=True)
    day_of_the_week = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        # Get the day of the week from the datetime field
        day_of_week = self.date_of_application.strftime('%A')
        # Save the day of the week to the second field
        self.day_of_the_week= day_of_week
        # always saving the balance
        self.balance = int(self.final_amount) - int(self.deposits)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.boda_guy_firstName + " " + self.boda_guy_lastName + " ==> " + str(self.final_amount)

# weekly payment
class BodaWeeklyPay(models.Model):
    boda_id = models.CharField(max_length=200, default='null')
    boda_firstName = models.CharField(max_length=200, default='null')
    boda_lastName = models.CharField(max_length=200, default='null')
    payment_fee = models.DecimalField(max_digits=20, decimal_places=2, default='0')
    phone_number = models.CharField(max_length=20, default='null')
    transaction_id = models.CharField(max_length=200, default='null')
    status = models.CharField(max_length=200, default='null')
    reference = models.CharField(max_length=200, default='null')
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return 'Boda Weekly Pay ' + str(self.payment_fee) + ' by ' + self.boda_firstName + " " + self.boda_lastName

