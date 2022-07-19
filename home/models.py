from django.db import models
import random
from datetime import datetime

# Create your models here.
def random_string():
    return str(random.randint(1000, 9999))

class Apply(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    national_id = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    pic_id = models.FileField()
    person_pic = models.FileField()
    first_guarrante_full_names = models.CharField(max_length=200)
    first_guarrante_national_id = models.CharField(max_length=200)
    first_guarrante_telephone = models.CharField(max_length=200)
    first_guarrante_pic_id = models.FileField()
    second_guarrante_full_names = models.CharField(max_length=200)
    second_guarrante_national_id = models.CharField(max_length=200)
    second_guarrante_telephone = models.CharField(max_length=200)
    second_guarrante_pic_id = models.FileField()
    transction_id = models.CharField(max_length=200)
    loan_amount = models.DecimalField(max_digits=8, decimal_places=2)
    loan_id = models.CharField(default= random_string, max_length=200)
    reference = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(max_length=50, default='fee_not_paid')
    user = models.CharField(max_length=200)
    payback = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')
    deposits = models.DecimalField(max_digits=12, decimal_places=2, default='0')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default='0')
    

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.payback = 10.00/100.00 * int(self.loan_amount) + int(self.loan_amount)
        self.balance = int(self.payback) - int(self.deposits)
        return super(Apply, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.user + ' loan amout of ' + '' + str(self.loan_amount)


class GroupApply(models.Model):
    loan_id = models.CharField(default= random_string, max_length=200)
    general_number = models.CharField(max_length=20, default='xxx')
    first_person_full_names = models.CharField(max_length=200, default='null')
    first_person_telephone = models.CharField(max_length=200, default='xxx')
    first_person_national_id = models.CharField(max_length=200, default='null')
    first_person_national_id_pic = models.FileField()
    first_person_pic = models.FileField()
    second_person_full_names = models.CharField(max_length=200, default='null')
    second_person_telephone = models.CharField(max_length=200, default='xxx')
    second_person_national_id = models.CharField(max_length=200, default='null')
    second_person_national_id_pic = models.FileField()
    second_person_pic = models.FileField()
    third_person_full_names = models.CharField(max_length=200, default='null')
    third_person_telephone = models.CharField(max_length=200, default='xxx')
    third_person_national_id = models.CharField(max_length=200, default='null')
    third_person_national_id_pic = models.FileField()
    third_person_pic = models.FileField()
    fourth_person_full_names = models.CharField(max_length=200, default='null')
    fourth_person_telephone = models.CharField(max_length=200, default='xxx')
    fourth_person_national_id = models.CharField(max_length=200, default='null')
    fourth_person_national_id_pic = models.FileField()
    fourth_person_pic = models.FileField()
    status = models.CharField(max_length=50, default='pending')
    user = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now, blank=True)
    loan_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payback = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.payback = 20.00/100.00 * int(self.loan_amount) + int(self.loan_amount)
        return super(GroupApply, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return 'Group loan, amout of :- ' + str(self.loan_amount) + ' ' + ' with a loan ID of ' + ' ' + str(self.loan_id)


class PermitApply(models.Model):
    permit_id = models.CharField(default=random_string, max_length=200)
    first_name = models.CharField(max_length=200, default='null')
    last_name = models.CharField(max_length=200, default='null')
    service = models.CharField(max_length=200, default='null')
    phone_number = models.CharField(max_length=20, default='0000000')
    date_modified = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(max_length=50, default='pending')
    message = models.CharField(max_length=200, default='null')
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default='0')
    deposits = models.DecimalField(max_digits=12, decimal_places=2, default='0')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default='0')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.balance = int(self.final_amount) - int(self.deposits)
        return super(PermitApply, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' applied for => ' + self.service




class Support(models.Model):
    user = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    question = models.CharField(max_length=200)
    answered = models.CharField(max_length=10, default='NO')

    def __str__(self):
        return self.user


    




