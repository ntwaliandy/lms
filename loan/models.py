from pyexpat import model
from django.db import models
from datetime import datetime, timedelta
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
    initial_payment = models.DecimalField(max_digits=12, decimal_places=2, default='0')
    deposits = models.DecimalField(max_digits=12, decimal_places=2, default='0')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default='0')
    weekly_pay = models.DecimalField(max_digits=12, decimal_places=2, default='0')
    phone_number = models.CharField(max_length=15, default='null')
    nin_number = models.CharField(max_length=30, default='null')
    nin_picture = models.FileField(null=True, blank=True, default=None)
    work_stage = models.CharField(max_length=30, default='null')
    status = models.CharField(max_length=10, default="ACTIVE")

    guarantor1_name = models.CharField(max_length=30, default='null')
    guarantor1_stage_name = models.CharField(max_length=30, default='null')
    guarantor1_number = models.CharField(max_length=15, default='null')
    guarantor1_nin = models.CharField(max_length=30, default='null')
    guarantor1_nin_picture = models.FileField(null=True, blank=True, default=None)

    guarantor2_name = models.CharField(max_length=30, default='null')
    guarantor2_stage_name = models.CharField(max_length=30, default='null')
    guarantor2_number = models.CharField(max_length=15, default='null')
    guarantor2_nin = models.CharField(max_length=30, default='null')
    guarantor2_nin_picture = models.FileField(null=True, blank=True, default=None)

    guarantor3_name = models.CharField(max_length=30, default='null')
    guarantor3_stage_name = models.CharField(max_length=30, default='null')
    guarantor3_number = models.CharField(max_length=15, default='null')
    guarantor3_nin = models.CharField(max_length=30, default='null')
    guarantor3_nin_picture = models.FileField(null=True, blank=True, default=None)
    latest_dateOfPay = models.CharField(max_length=30, blank=True)
    date_of_application = models.DateTimeField(default=datetime.now, blank=True)
    day_of_the_week = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        # Get the day of the week from the datetime field
        paying_day = self.date_of_application + timedelta(days=1)
        day_of_week = paying_day.strftime('%A')
        # Save the day of the week to the second field
        self.day_of_the_week= day_of_week
        # always saving the balance
        from decimal import Decimal
        self.balance = Decimal(str(self.final_amount)) - Decimal(str(self.deposits))
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

# expenditures and collections
class CashFlow(models.Model):
    cash_id = models.CharField(max_length=200, default=random_string)
    expenditures = models.DecimalField(max_digits=20, decimal_places=2, default='0')
    collections = models.DecimalField(max_digits=20, decimal_places=2, default='0')
    banked_balance = models.DecimalField(max_digits=20, decimal_places=2, default='0')
    note = models.TextField()
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return 'Banked => ' + str(self.banked_balance) + "UGX On " + str(self.date)
    

class BodaInformation(models.Model):
    numberPlate = models.CharField(max_length=200, default="")
    rider = models.CharField(max_length=200, default="")
    amountBought = models.DecimalField(max_digits=20, decimal_places=2, default='0')
    whereBought = models.CharField(max_length=200, default="")
    LogBookNames = models.CharField(max_length=200, default="")
    demandedAmount = models.DecimalField(max_digits=20, decimal_places=2, default='0')
    isCompleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.rider) + " with " + str(self.numberPlate)


# Boda Inventory — bodas the business purchases, can be sold cash or assigned to a loan
class BodaInventory(models.Model):
    STATUS_IN_STOCK = 'IN_STOCK'
    STATUS_SOLD_CASH = 'SOLD_CASH'
    STATUS_LOAN = 'LOAN'
    STATUS_CHOICES = [
        (STATUS_IN_STOCK, 'In Stock'),
        (STATUS_SOLD_CASH, 'Sold - Cash'),
        (STATUS_LOAN, 'Gone to Loan'),
    ]

    number_plate = models.CharField(max_length=20)
    boda_type = models.CharField(max_length=100, blank=True, default='')
    chassis_no = models.CharField(max_length=100, blank=True, default='')
    engine_no = models.CharField(max_length=100, blank=True, default='')
    colour = models.CharField(max_length=50, blank=True, default='')
    amount_bought_at = models.DecimalField(max_digits=14, decimal_places=2, default='0')
    date_purchased = models.DateField(default=datetime.now)
    notes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_IN_STOCK)

    # Filled when status = SOLD_CASH
    buyer_name = models.CharField(max_length=100, blank=True, default='')
    buyer_phone = models.CharField(max_length=20, blank=True, default='')
    buyer_id = models.CharField(max_length=50, blank=True, default='')
    buyer_address = models.CharField(max_length=200, blank=True, default='')
    amount_sold_for = models.DecimalField(max_digits=14, decimal_places=2, default='0')
    date_sold = models.DateField(null=True, blank=True)

    # Filled when status = LOAN
    boda_apply_id = models.CharField(max_length=200, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def profit(self):
        return self.amount_sold_for - self.amount_bought_at

    def __str__(self):
        return self.number_plate + " (" + self.status + ")"


# Impounded Bikes — bodas seized from clients who failed to pay
class ImpoundedBike(models.Model):
    STATUS_HELD = 'HELD'
    STATUS_RETURNED = 'RETURNED'
    STATUS_CHOICES = [
        (STATUS_HELD, 'Being Held'),
        (STATUS_RETURNED, 'Returned'),
    ]

    boda_id = models.CharField(max_length=200, blank=True, default='')
    number_plate = models.CharField(max_length=20)
    client_name = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=20, blank=True, default='')
    date_impounded = models.DateField(default=datetime.now)
    amount_demanded = models.DecimalField(max_digits=14, decimal_places=2, default='0')
    deficit_at_impound = models.DecimalField(max_digits=14, decimal_places=2, default='0')
    reason = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_HELD)

    # Filled when returned
    date_returned = models.DateField(null=True, blank=True)
    return_notes = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def days_held(self):
        from datetime import date as d
        end = self.date_returned if self.date_returned else d.today()
        return (end - self.date_impounded).days

    def __str__(self):
        return self.number_plate + " — " + self.client_name + " (" + self.status + ")"
