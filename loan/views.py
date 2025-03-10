
from datetime import datetime, date, timedelta
import decimal
import uuid
import imp
import json
from random import randint
from time import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from home.models import Apply, GroupApply, PermitApply, SmsCallBack, Support
from .models import AddPayment, AddPermitPayment, BodaInformation, CashFlow, FileUpload, GroupAddPayment, Replies, BodaApply, BodaWeeklyPay
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth import get_user_model
# Create your views here.
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import requests
import http.client
import africastalking
from django.db.models import Q
from django.core.serializers import serialize
import csv
from django.db.models import Count

# username = "EREMIT"

# AT API KEY
api_key = "atsk_9e6afc19b040e7f6a8924f1d12b66c3ec6ee283609a3901cb2c3443e257e6010b1165c10"
username = "breniel"
yolasms_apiKey = "DNlh3cFmJyXO96gsM9xf2360zk797Y2qRuSh31o4a82Hj3gAKc05r78Izlgr1BzD"

# ESMS API KEY
# api_key = "c155994b2b8a797901f5a1aeb29dcfc3b1b6f7c8631f484a046bffce7b010bd3402fee21f0c513723818c017259ff6f8"


def dashboard(request):
    if request.user.is_superuser:
        applied_loans = Apply.objects.count()
        total_loans = Apply.objects.aggregate(Sum('loan_amount'))
        totalLoans = total_loans['loan_amount__sum']
        total_sales = Apply.objects.aggregate(Sum('deposits'))
        totalSales = total_sales['deposits__sum']
        recent_loans = reversed(Apply.objects.filter(status = 'pending').order_by('date')[:3])
        loans = Apply.objects.all()

        context = {
            'applied_loans': applied_loans,
            'total_loans': totalLoans,
            'recent_loans': recent_loans,
            'total_sales': totalSales,
            'loans': loans
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('account:admin-login')

# single loans
def manage_loans(request):
    if request.user.is_superuser:
        loans = Apply.objects.all()
        context = {
            'loans': loans,
        }
        return render(request, 'manage_loans.html', context)
    else:
        return redirect('account:admin-login')


# group loans
def manage_group_loans(request):
    if request.user.is_superuser:
        group_loans = GroupApply.objects.all()
        context = {
            'group_loans': group_loans,
        }
        return render(request, 'manage_group_loans.html', context)
    else:
        return redirect('account:admin-login')

# single loan approve
def loan_approve(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            if request.POST['loan_id'] == '':
                messages.info(request, 'there is something wrong!!!')
                return redirect('loan:dashboard')
            else:
                loan_id = request.POST['loan_id']

                if Apply.objects.filter(id=loan_id):
                    Apply.objects.filter(id=loan_id).update(status = 'approved')
                    return redirect('loan:dashboard')
                else:
                    return redirect('loan:dashboard')
        else:
            return HttpResponse('Bad request')
    else:
        return redirect('account:admin-login')

# single loan reject
def loan_remove(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            if request.POST['loan_id'] == '':
                messages.info(request, 'there is something wrong!!!')
                return redirect('loan:dashboard')
            else:
                loan_id = request.POST['loan_id']

                if Apply.objects.filter(id=loan_id):
                    Apply.objects.filter(id=loan_id).update(status = 'removed')
                    return redirect('loan:dashboard')
                else:
                    return redirect('loan:dashboard')
        else:
            return HttpResponse('Bad request')
    else:
        return redirect('account:admin-login')

# single loan completing
def loan_complete(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            if request.POST['loan_id'] == '':
                messages.info(request, 'there is something wrong!!!')
                return redirect('loan:dashboard')
            else:
                loan_id = request.POST['loan_id']
                if Apply.objects.filter(id=loan_id):
                    Apply.objects.filter(id=loan_id).update(status = 'completed')
                    return redirect('loan:dashboard')
                else:
                    return redirect('loan:dashboard')
        else:
            return HttpResponse('Bad request')
    else:
        return redirect('account:admin-login')

#daily single loan payment
def add_payment(request):
    if request.user.is_superuser:
        loans = Apply.objects.all()
        context = {
            'loans': loans
        }
        username = request.user.username
        if request.method == 'POST':
            data = request.POST
            loanId = request.POST.get('loan_id', 'none')
            payment_fee = data['payment_fee']
            phone_number = data['phone_number']
            print(phone_number)

            #form validation
            if loanId == '':
                messages.info(request, 'loan ID cant be null')
            elif payment_fee == '':
                messages.info(request, 'payment fee cant be null')
            else:
                ref = uuid.uuid4()
                conn = http.client.HTTPSConnection("api.cissytech.com")
                payload = json.dumps({
                "apiKey": "cf5eaeba-fbb4-42e2-8c3f-de00ce969a4f",
                "phone": phone_number,
                "amount": payment_fee,
                "reference": str(ref)
                })
                headers = {
                'Content-Type': 'application/json'
                }
                conn.request("POST", "/pay/moneyaccess/requestToPay", payload, headers)
                res = conn.getresponse()
                data = json.load(res)
                # response = data.decode("utf-8")
                result = data['data']['requestToPay']
                transId = data['data']['transactionId']
                if result == True:
                    print(result)
                    date = request.POST.get('date', datetime.now())
                    AddPayment.objects.create(
                        loan_id = loanId,
                        payment_fee = payment_fee,
                        transaction_id = transId,
                        status = 'pending',
                        reference = str(ref),
                        date = date,
                        admin = username
                    )
                return redirect('loan:dashboard')
        else:
            return render(request, 'add_payment.html', context)

    else:
        return redirect('account:admin-login')


# check daily payment
def pay_details(request, ref):
    if request.user.is_superuser:
        record = AddPayment.objects.filter(reference=ref)
        for recd in record:
            fee = recd.payment_fee
            loanId = recd.loan_id
            trans_id = recd.transaction_id
            statuss = recd.status
        print(fee)
        print(ref)
        print(trans_id)
        payload = {
        "apiKey": "cf5eaeba-fbb4-42e2-8c3f-de00ce969a4f",
        "transactionId": str(trans_id)
        }
        headerss = {
        'Content-Type': 'application/json'
        }
        res = requests.post("https://api.cissytech.com/pay/moneyaccess/requestToPayStatus", headers=headerss, json=payload)
        data = res.json()
        result = data['data']['data']['status']
        print(data)
        print(result)
        if result == 'INPROCESS' or result == 'FAILED':
            AddPayment.objects.filter(reference=ref).update(status = 'pending')
            messages.info(request, "user with Loan ID " + loanId + " haven't paid yet for the specific day")
            return redirect('loan:payment-record')
        elif result == 'SUCCESSFUL' and statuss == 'pending':
            AddPayment.objects.filter(reference=ref).update(status = 'paid')
            single_loan = get_object_or_404(Apply, loan_id=loanId)
            latest_deposit = single_loan.deposits + fee
            new_balance = single_loan.payback - latest_deposit
            PermitApply.objects.filter(loan_id=loanId).update(deposits=latest_deposit, balance=new_balance)

            messages.info(request, "user with Loan ID " + loanId + " paid " + str(fee) + " successfully!")
            return redirect('loan:payment-record')
        elif result == 'SUCCESSFUL' and statuss == 'paid':
            AddPayment.objects.filter(reference=ref).update(status = 'paid')
            messages.info(request, "user with Loan ID " + loanId + " paid " + str(fee) + " successfully!")
            return redirect('loan:payment-record')
        else:
            AddPayment.objects.filter(reference=ref).update(status = 'pending')
            messages.info(request, "user with Loan ID " + loanId + " haven't paid yet for the specific day")
            return redirect('loan:payment-record')
    else:
        return redirect('account:admin-login')

# check loan application fee
def fee_details(request, loan_id):
    if request.user.is_superuser:
        record = Apply.objects.filter(loan_id=loan_id)
        for recd in record:
            trans_id = recd.transction_id
        conn = http.client.HTTPSConnection("api.cissytech.com")
        payload = json.dumps({
        "apiKey": "cf5eaeba-fbb4-42e2-8c3f-de00ce969a4f",
        "transactionId": str(trans_id)
        })
        headers = {
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/pay/moneyaccess/requestToPayStatus", payload, headers)
        res = conn.getresponse()
        data = json.load(res)
        result = data['data']['data']['status']
        if result == 'FAILED' or result == 'INPROCESS':
            Apply.objects.filter(loan_id=loan_id).update(status = 'fee_not_paid')
            messages.info(request, "user with loan ID " + loan_id + " haven't paid 5000 application fee")
            return redirect('loan:manage-loans')
        elif result == 'SUCCESSFUL':
            Apply.objects.filter(loan_id=loan_id).update(status = 'pending')
            messages.info(request, "user paid application fee successfully, check in pending loans to approve")
            return redirect('loan:manage-loans')
        else:
            Apply.objects.filter(loan_id=loan_id).update(status = 'fee_not_paid')
            messages.info(request, "user with loan ID " + loan_id + " haven't paid 5000 application fee")
            return redirect('loan:manage-loans')
    else:
        return redirect('account:admin-login')

# single loan daily payment view
def payment_record(request):
    if request.user.is_superuser:
        payments = AddPayment.objects.all()
        context = {
            'payments': payments
        }
        return render(request, 'payment_record.html', context)
    else:
        return redirect('account:admin-login')

# single loan deatils view
def loan_details(request, loan_id):
    if request.user.is_superuser:
        loan = get_object_or_404(Apply, pk=loan_id)
        context = {
            'loan': loan
        }
        return render(request, 'loan_details.html', context)
    else:
        return redirect('account:admin-login')

#group loan approve
def group_loan_approve(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            if request.POST['loan_id'] == '':
                messages.info(request, 'there is something wrong!!!')
                return redirect('loan:dashboard')
            else:
                loan_id = request.POST['loan_id']

                if GroupApply.objects.filter(id=loan_id):
                    GroupApply.objects.filter(id=loan_id).update(status = 'approved')
                    return redirect('loan:dashboard')
                else:
                    return redirect('loan:dashboard')
        else:
            return HttpResponse('Bad request')
    else:
        return redirect('account:admin-login')

# group loan reject
def group_loan_remove(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            if request.POST['loan_id'] == '':
                messages.info(request, 'there is something wrong!!!')
                return redirect('loan:dashboard')
            else:
                loan_id = request.POST['loan_id']

                if GroupApply.objects.filter(id=loan_id):
                    GroupApply.objects.filter(id=loan_id).update(status = 'removed')
                    return redirect('loan:dashboard')
                else:
                    return redirect('loan:dashboard')
        else:
            return HttpResponse('Bad request')
    else:
        return redirect('account:admin-login')

# group loan completing
def group_loan_complete(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            if request.POST['loan_id'] == '':
                messages.info(request, 'there is something wrong!!!')
                return redirect('loan:dashboard')
            else:
                loan_id = request.POST['loan_id']
                if GroupApply.objects.filter(id=loan_id):
                    GroupApply.objects.filter(id=loan_id).update(status = 'completed')
                    return redirect('loan:dashboard')
                else:
                    return redirect('loan:dashboard')
        else:
            return HttpResponse('Bad request')
    else:
        return redirect('account:admin-login')


#daily group loan payment
def group_add_payment(request):
    if request.user.is_superuser:
        loans = GroupApply.objects.all()
        context = {
            'loans': loans
        }
        username = request.user.username
        if request.method == 'POST':
            data = request.POST
            loan_id = request.POST.get('loan_id', 'none')
            payment_fee = data['payment_fee']
            transaction_id = data['transaction_id']
            paid = request.POST.get('paid', 'no')
            date = request.POST.get('date', datetime.now())

            #form validation
            if loan_id == '':
                messages.info(request, 'loan ID cant be null')
            elif payment_fee == '':
                messages.info(request, 'payment fee cant be null')
            elif transaction_id == '':
                messages.info(request, 'transaction id cant be empty')
            elif paid == '':
                messages.info(request, 'paid section cant be null')
            else:
                # insert records the database
                GroupAddPayment.objects.create(
                    loan_id = loan_id,
                    payment_fee = payment_fee,
                    transaction_id = transaction_id,
                    paid = paid,
                    date = date,
                    admin = username
                )
                return redirect('loan:dashboard')
        else:
            return render(request, 'group_add_payment.html', context)

    else:
        return redirect('account:admin-login')


# group loan daily payment view
def group_payment_record(request):
    if request.user.is_superuser:
        payments = GroupAddPayment.objects.all()
        context = {
            'payments': payments
        }
        return render(request, 'group_payment_record.html', context)
    else:
        return redirect('account:admin-login')


def all_clients(request):
    if request.user.is_superuser:
        User = get_user_model()
        users = User.objects.all()
        payment = AddPayment.objects.filter(status = 'pending').all()
        person = Apply.objects.all()
        context = {
            'users': users,
            'person': person,
            'payment': payment,
        }
        return render(request, 'all-clients.html', context)
    else:
        return redirect('account:admin-login')

def staff(request):
    if request.user.is_superuser:
        User = get_user_model()
        users = User.objects.all()
        context = {
            'users': users,
        }
        return render(request, 'staff.html', context)
    else:
        return redirect('account:admin-login')

def complaints(request):
    if request.user.is_superuser:
        errors = Support.objects.filter(answered='NO').all()
        context = {
            'errors': errors
        }
        return render(request, 'complaints.html', context)
    else:
        return redirect('account:admin-login')

def reply(request, error_id):
    if request.user.is_superuser:
        error = get_object_or_404(Support, pk=error_id)

        context ={
            'error': error
        }
        if request.method == 'POST':
            data = request.POST
            feedback = data['feedback']

            # inserting them to the database
            Replies.objects.create(
                question_id = error.id,
                feedback = feedback,
            )
            messages.error(request, 'successfuly replied')
            return render(request, 'reply_error.html', {'error': error, 'done': 'done'})
        return render(request, 'reply_error.html', context)
    else:
        return redirect('account:admin-login')

def done(request, quest_id):
    Support.objects.filter(id=quest_id).update(
        answered = 'YES'
    )
    return redirect('loan:complaints')


def group_details(request, group_l_id):
    if request.user.is_superuser:
        loan = get_object_or_404(GroupApply, pk=group_l_id)
        context = {
            'loan': loan
        }
        return render(request, 'group_loan_details.html', context)
    else:
        return redirect('account:admin-login')


def send_report(request):

    payments = AddPayment.objects.all()
    for pay in payments:
        loan_ID = pay.loan_id
    subject = 'hello everyone'
    recipient = 'mutagayageorge14@gmail.com'
    sender = 'ntwaliandy90@gmail.com'
    message = 'amount ' + str(payments[1])
    print(message)

    msg = EmailMessage(subject, message, sender, [recipient])
    msg.content_subtype = "html"
    msg.send()

    return redirect('loan:dashboard')


# PERMIT SECTION

def permit_dashboard(request):
    if request.user.is_superuser:
        user_name = request.user.username
        permits = PermitApply.objects.filter(Q(admin=user_name) | Q(admin="null")).all()
        admin_permit = PermitApply.objects.all()
        in_process_permits_count = PermitApply.objects.filter(status='applied').count()
        done_permits_count = PermitApply.objects.filter(status='finished').count()
        all_application_count = PermitApply.objects.all().count()
        duplicate = PermitApply.objects.values('permit_id').annotate(count=Count('permit_id')).filter(count__gt=1).values_list('permit_id', flat=True)
        print(len(duplicate))
        for permit_id in duplicate:
            print(permit_id)
        context = {
            'permits': permits,
            'in_process': in_process_permits_count,
            'admin_permit': admin_permit,
            'done': done_permits_count,
            'all_permits_count': all_application_count,
        }
        return render(request, 'permit_dashboard.html', context)

    else:
        return redirect('accounts:admin-login')


def permit_add_payment(request):
    if request.user.is_superuser:
        user_name = request.user.username
        permits = PermitApply.objects.filter(Q(status = "applied"), Q(admin = user_name) |Q(admin = "null")).all()
        context = {
            "permits": permits
        }
        username = request.user.username
        if request.method == 'POST':
            data = request.POST
            permitId = data.get('permit_id', 'none')
            print("permit ID ", permitId)
            paymentFee = data['payment_fee']
            phoneNumber = data['phone_number']
            ref = uuid.uuid4()
            conn = http.client.HTTPSConnection("api.cissytech.com")
            payload = json.dumps({
            "apiKey": "cf5eaeba-fbb4-42e2-8c3f-de00ce969a4f",
            "phone": phoneNumber,
            "amount": paymentFee,
            "reference": str(ref)
            })
            headers = {
            'Content-Type': 'application/json'
            }
            conn.request("POST", "/pay/moneyaccess/requestToPay", payload, headers)
            res = conn.getresponse()
            data = json.load(res)
            print(data)
            # response = data.decode("utf-8")
            result = data['data']['requestToPay']
            if result == True:
                transId = data['data']['transactionId']
                AddPermitPayment.objects.create(
                    permit_id = permitId,
                    payment_fee = paymentFee,
                    phone_number = phoneNumber,
                    reference = ref,
                    transaction_id = transId,
                    status = 'pending',
                    admin = username
                )
                messages.info(request, "user with permit ID " + str(permitId) +" paid " + str(paymentFee) + " successfully. Go to Permit Details and view so that you can finally confirm the transaction.")
                return redirect('loan:permit-dashboard')
            elif result == False:
                AddPermitPayment.objects.create(
                    permit_id = permitId,
                    payment_fee = paymentFee,
                    phone_number = phoneNumber,
                    reference = ref,
                    transaction_id = "NOT PAID",
                    status = 'NOT PAID',
                    admin = username
                )
                messages.info(request, "repeat the tansaction please!!!!!!!!")
                return redirect('loan:permit-dashboard')
            else:
                messages.info(request, "Transaction Error... REPEAT AGAIN")
                return redirect('loan:permit-dashboard')


        else:
            return render(request, 'add_permit_payment.html', context)
    else:
        return redirect('accounts:admin-login')


def manual_add_payment(request):
    if request.user.is_superuser:
        permits = PermitApply.objects.filter(status = "applied").all()
        context = {
            "permits": permits
        }

        username = request.user.username
        if request.method == 'POST':
            data = request.POST
            permitId = data.get('permit_id', 'none')
            paymentFee = data['payment_fee']
            phoneNumber = data['phone_number']
            status = "paid"

            reference = uuid.uuid4()
            transaction_id = "manual pay"

            if permitId == "":
                messages.info(request, "Try writing the user correctly")
                return render(request, 'add_permit_payment.html', context)

            create_payment = AddPermitPayment.objects.create(
                permit_id = permitId,
                payment_fee = paymentFee,
                phone_number = phoneNumber,
                reference = reference,
                transaction_id = transaction_id,
                status = status,
                admin = username
            )

            africastalking.initialize(username, api_key)
            sms = africastalking.SMS


            single_permit = get_object_or_404(PermitApply, permit_id=permitId)

            latest_deposit = single_permit.deposits + int(paymentFee)
            new_balance = single_permit.final_amount - latest_deposit

            new_phoneNumber = "+" + phoneNumber
            service = single_permit.service
            full_name = single_permit.first_name + " " + single_permit.last_name
            PermitApply.objects.filter(permit_id=permitId).update(deposits=latest_deposit, balance=new_balance)

            if new_balance <= 0:
                PermitApply.objects.filter(permit_id=permitId).update(status="finished")
            print("sending")
            response = sms.send(
                "hey " + full_name + ", you have successfully paid " + str(paymentFee) + "UGX for your " + service + " permit service and your outstanding balance is " + str(new_balance) + "UGX. Thank you!!!",
                [new_phoneNumber]
            )

            if response:
                print(":: response ::", response)
                id = response['SMSMessageData']['Recipients'][0]['messageId']
                print(":: message ID ::", id)

                create_payment.reference = id
                create_payment.save()

            messages.info(request, "user with Permit ID " + permitId + " paid " + str(paymentFee) + " successfully!")
            return redirect('loan:permit-dashboard')
        else:
            messages.info(request, "failed to add the record manually")
            return render(request, 'add_permit_payment.html', context)
    else:
        messages.info(request, "User not Allowed")
        return redirect('loan:permit-add-payment')


def permit_payment_details(request):
    if request.user.is_superuser:
        user_name = request.user.username
        payments = reversed(AddPermitPayment.objects.filter(admin = user_name).all())
        admin_payments = reversed(AddPermitPayment.objects.all())
        context = {
            'payments': payments,
            'admin_payments': admin_payments
        }
        return render(request, 'permit_payment_details.html', context)
    else:
        return redirect('account:admin-login')


def permit_pay_details(request, ref):
    if request.user.is_superuser:
        record = AddPermitPayment.objects.filter(reference=ref)
        for recd in record:
            fee = recd.payment_fee
            phone_number = recd.phone_number
            permitId = recd.permit_id
            trans_id = recd.transaction_id
            statuss = recd.status
        print(fee)
        print(ref)
        print(trans_id)
        payload = {
        "apiKey": "cf5eaeba-fbb4-42e2-8c3f-de00ce969a4f",
        "transactionId": str(trans_id)
        }
        headerss = {
        'Content-Type': 'application/json'
        }
        res = requests.post("https://api.cissytech.com/pay/moneyaccess/requestToPayStatus", headers=headerss, json=payload)
        data = res.json()
        result = data['data']['data']['status']
        print(data)
        print(result)
        if result == 'INPROCESS' or result == 'FAILED':
            AddPermitPayment.objects.filter(reference=ref).update(status = 'not paid')
            messages.info(request, "user with Permit ID " + permitId + " haven't paid yet for the specific day")
            return redirect('loan:permit-payment-details')

        elif result == 'SUCCESSFUL' and statuss == 'pending':
            africastalking.initialize(username, api_key)
            sms = africastalking.SMS


            AddPermitPayment.objects.filter(reference=ref).update(status = 'paid')
            single_permit = get_object_or_404(PermitApply, permit_id=permitId)
            latest_deposit = single_permit.deposits + fee
            new_balance = single_permit.final_amount - latest_deposit
            new_phoneNumber = "+" + phone_number
            service = single_permit.service
            full_name = single_permit.first_name + " " + single_permit.last_name
            PermitApply.objects.filter(permit_id=permitId).update(deposits=latest_deposit, balance=new_balance)

            if new_balance <= 0:
                PermitApply.objects.filter(permit_id=permitId).update(status="finished")

            sms.send(
                "hey " + full_name + ", you have successfully paid " + str(fee) + "UGX for your " + service + " permit service and your outstanding balance is " + str(new_balance) + "UGX. Thank you!!!", [new_phoneNumber],
                callback=on_finish
            )
            messages.info(request, "user with Permit ID " + permitId + " paid " + str(fee) + " successfully!")
            return redirect('loan:permit-payment-details')
        elif result == 'SUCCESSFUL' and statuss == 'paid':
            messages.info(request, "user with Permit ID " + permitId + " paid " + str(fee) + " successfully!")
            return redirect('loan:permit-payment-details')
        else:
            AddPermitPayment.objects.filter(reference=ref).update(status = 'not paid')
            messages.info(request, "user with permit ID " + permitId + " haven't paid yet for the specific day")
            return redirect('loan:permit-payment-details')
    else:
        return redirect('account:admin-login')

def permit_clients(request):
    if request.user.is_superuser:
        clients = PermitApply.objects.all()
        context = {
            "clients": clients
        }
        return render(request, "permit_clients.html", context)
    else:
        return redirect('accounts:admin-login')


def files_upload(request):
    if request.user.is_superuser:
        permits = PermitApply.objects.exclude(balance = 0).all()
        context = {
            "permits": permits
        }
        username = request.user.username
        if request.method == 'POST':
            data = request.POST
            permitId = data.get('permit_id', 'none')
            File_upload = data.get('upload_file')
            message = data['message']

            print(File_upload)
            FileUpload.objects.create(
                permit_id = permitId,
                uploaded_file = File_upload,
                message = message,
                admin = username
            )

            return redirect('loan:permit-dashboard')

        else:
            return render(request, 'permit_file_upload.html', context)
    else:
        return redirect('account:admin-login')



def file_details(request, permitId):
    if request.user.is_superuser:
        individual_files = FileUpload.objects.filter(permit_id=permitId).all()
        permit_payments = AddPermitPayment.objects.filter(permit_id=permitId).all()
        permit_obj = PermitApply.objects.filter(permit_id=permitId).first()

        context = {
            'permitObj': permit_obj,
            'files': individual_files,
            'permit_payments': permit_payments
        }

        return render(request, 'individual_files.html', context)

    else:
        return redirect('account:admin-login')


def permit_logs(request):
    if request.user.is_superuser:
        user_name = request.user.username
        # today results
        today_res = AddPermitPayment.objects.filter(date__date=date.today(), status='paid', admin=user_name).all()
        admin_today_res = AddPermitPayment.objects.filter(date__date=date.today(), status='paid').all()
        today_no_tr = AddPermitPayment.objects.filter(date__date=date.today(), status='paid').all().count()
        today_fee = AddPermitPayment.objects.filter(date__date=date.today(), status='paid').aggregate(Sum('payment_fee'))
        today_fee_res = today_fee['payment_fee__sum']

        # weekly results
        current_date = date.today()
        today_date = current_date + timedelta(days=1)
        past_days = current_date - timedelta(days=7)
        week_res = AddPermitPayment.objects.filter(date__range=(past_days, today_date), status='paid', admin=user_name).all()
        admin_week_res = AddPermitPayment.objects.filter(date__range=(past_days, today_date), status='paid').all()
        week_no_tr = AddPermitPayment.objects.filter(date__range=(past_days, today_date), status='paid').all().count()
        week_fee = AddPermitPayment.objects.filter(date__range=(past_days, today_date), status='paid').aggregate(Sum('payment_fee'))
        week_fee_res = week_fee['payment_fee__sum']

        # monthly results
        week_current_date = date.today()
        week_today_date = week_current_date + timedelta(days=1)
        past_weeks = week_current_date - timedelta(days=31)
        month_res = AddPermitPayment.objects.filter(date__range=(past_weeks, week_today_date), status='paid', admin=user_name).all()
        admin_month_res = AddPermitPayment.objects.filter(date__range=(past_weeks, week_today_date), status='paid').all()
        month_no_tr = AddPermitPayment.objects.filter(date__range=(past_weeks, week_today_date), status='paid').all().count()
        month_fee = AddPermitPayment.objects.filter(date__range=(past_weeks, week_today_date), status='paid').aggregate(Sum('payment_fee'))
        month_fee_res = month_fee['payment_fee__sum']


        # All Payments
        allPay = AddPermitPayment.objects.filter(status='paid', admin=user_name).all()
        admin_allPay = AddPermitPayment.objects.filter(status='paid').all()
        total_no_tr = AddPermitPayment.objects.filter(status='paid').all().count()
        allPayFee = AddPermitPayment.objects.filter(status='paid').aggregate(Sum('payment_fee'))
        allPayFee_res = allPayFee['payment_fee__sum']






        print(date.today())
        print(datetime.now())
        context = {
            'todayRes': today_res,
            'todayFee': today_fee_res,
            'weekRes': week_res,
            'weekFee': week_fee_res,
            'monthRes': month_res,
            'monthFee': month_fee_res,
            'allPay': allPay,
            'allfeeRes': allPayFee_res,
            'today_no': today_no_tr,
            'weekly_no': week_no_tr,
            'monthly_no': month_no_tr,
            'total_no': total_no_tr,
            'admin_today_res': admin_today_res,
            'admin_week_res': admin_week_res,
            'admin_month_res': admin_month_res,
            'admin_allPay': admin_allPay
        }
        return render(request, 'permit-logs.html', context)
    else:
        return redirect('account:admin-login')


#  search client
def search_client(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            data = request.POST
            search_entry = data['client_search']
            if PermitApply.objects.filter(first_name=search_entry).first():
                client = PermitApply.objects.filter(first_name=search_entry).all()
                context = {
                    "client": client
                }
                return render(request, "search_client.html", context)
            elif PermitApply.objects.filter(last_name=search_entry).first():
                client = PermitApply.objects.filter(last_name=search_entry).all()
                context = {
                    "client": client
                }
                return render(request, "search_client.html", context)
            elif PermitApply.objects.filter(phone_number=search_entry).first():
                client = PermitApply.objects.filter(phone_number=search_entry).all()
                context = {
                    "client": client
                }
                return render(request, "search_client.html", context)
            elif PermitApply.objects.filter(permit_id=search_entry).first():
                client = PermitApply.objects.filter(permit_id=search_entry).all()
                context = {
                    "client": client
                }
                return render(request, "search_client.html", context)
            elif PermitApply.objects.filter(admin=search_entry).first():
                client = PermitApply.objects.filter(admin=search_entry).all()
                context = {
                    "client": client
                }
                return render(request, "search_client.html", context)
            else:
                messages.info(request, "No such User")
                return redirect('loan:permit-dashboard')
        else:
            return redirect('loan:permit-dashboard')

    else:
        return redirect('account:user_login')


# search client for triggering
def search_client_trigger(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            data = request.POST
            search_entry = data.get('client_search', False)
            print(search_entry)
            if PermitApply.objects.filter(first_name=search_entry, status="applied").first():
                client = PermitApply.objects.filter(first_name=search_entry, status="applied").all()

                serialized_data = serialize("json", client)
                data = json.loads(serialized_data)
                return JsonResponse ({"status": "success", "data": data})
            elif PermitApply.objects.filter(last_name=search_entry, status="applied").first():
                client = PermitApply.objects.filter(last_name=search_entry, status="applied").all()

                serialized_data = serialize("json", client)
                data = json.loads(serialized_data)
                return JsonResponse({"status": "success", "data": data})
            elif PermitApply.objects.filter(phone_number=search_entry, status="applied").first():
                client = PermitApply.objects.filter(phone_number=search_entry, status="applied").all()

                serialized_data = serialize("json", client)
                data = json.loads(serialized_data)
                return JsonResponse({"status": "success", "data": data})
            elif PermitApply.objects.filter(permit_id=search_entry, status="applied").first():
                client = PermitApply.objects.filter(permit_id=search_entry, status="applied").all()

                serialized_data = serialize("json", client)
                data = json.loads(serialized_data)
                return JsonResponse({"status": "success", "data": data})
            else:
                return JsonResponse({"status": "failed"})
        else:
            return redirect('loan:dashboard')

    else:
        return redirect('account:user_login')


# loanlogs
def loan_logs(request):
    if request.user.is_superuser:
        # today results
        today_res = AddPayment.objects.filter(date__date=date.today(), status='paid').all()
        today_fee = AddPayment.objects.filter(date__date=date.today(), status='paid').aggregate(Sum('payment_fee'))
        today_fee_res = today_fee['payment_fee__sum']

        # weekly results
        current_date = date.today()
        today_date = current_date + timedelta(days=1)
        past_days = current_date - timedelta(days=7)
        week_res = AddPayment.objects.filter(date__range=(past_days, today_date), status='paid').all()
        week_fee = AddPayment.objects.filter(date__range=(past_days, today_date), status='paid').aggregate(Sum('payment_fee'))
        week_fee_res = week_fee['payment_fee__sum']

        # monthly results
        week_current_date = date.today()
        week_today_date = week_current_date + timedelta(days=1)
        past_weeks = week_current_date - timedelta(days=31)
        month_res = AddPayment.objects.filter(date__range=(past_weeks, week_today_date), status='paid').all()
        month_fee = AddPayment.objects.filter(date__range=(past_weeks, week_today_date), status='paid').aggregate(Sum('payment_fee'))
        month_fee_res = month_fee['payment_fee__sum']


        # All Payments
        allPay = AddPayment.objects.filter(status='paid').all()
        allPayFee = AddPayment.objects.filter(status='paid').aggregate(Sum('payment_fee'))
        allPayFee_res = allPayFee['payment_fee__sum']






        print(date.today())
        print(datetime.now())
        context = {
            'todayRes': today_res,
            'todayFee': today_fee_res,
            'weekRes': week_res,
            'weekFee': week_fee_res,
            'monthRes': month_res,
            'monthFee': month_fee_res,
            'allPay': allPay,
            'allfeeRes': allPayFee_res
        }
        return render(request, 'loan-logs.html', context)
    else:
        return redirect('account:admin-login')



def permit_edit_details(request, permitID):
    if request.user.is_superuser:
        permit_details = get_object_or_404(PermitApply, permit_id=permitID)
        context = {
            "permit_details": permit_details
        }

        return render(request, "permit_edit_details.html", context)
    else:
        return redirect('account:admin-login')


def post_permit_edit(request):
    if request.user.is_superuser and request.method == 'POST':
        data = request.POST
        permitId = data['permit_id']
        first_name = data['first_name']
        last_name = data['last_name']
        phone_number = data['phone_number']
        service = data['service']
        final_amount = data['service_amount']

        permit = get_object_or_404(PermitApply, permit_id=permitId)
        deposits = permit.deposits

        balance = decimal.Decimal(final_amount) - deposits

        PermitApply.objects.filter(permit_id=permitId).update(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            service=service,
            final_amount=final_amount,
            balance = balance
        )

        messages.info(request, "user with Permit ID " + permitId + " has been updated successfully!")

        return redirect('loan:permit-dashboard')

    else:
        messages.info(request, "failed to update!")

        return redirect('loan:permit-dashboard')


def client_csv(request):
    low_client = AddPermitPayment.objects.filter(transaction_id="manual pay").all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=all_applicants' + str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow([
        'permit_id',
        'first_name',
        'service',
        'phone_number',
        'message',
        'final_amount',
        'deposits',
        'balance',
    ])

    for cl in low_client:
       writer.writerow([
            cl.permit_id,
            cl.payment_fee,
            cl.phone_number,
            cl.date,
            cl.transaction_id
        ]) 
    return response
def on_finish(error, response):
    if error is not None:
        raise error
    print(response)


# BODA BODA SECTION
def add_boda(request):
    if request.method == 'POST':
        data = request.POST
        boda_firstName = data.get('boda_first_name')
        boda_lastName = data.get('boda_last_name')
        boda_numberPlate = data.get('boda_number_plate')
        boda_amount = data.get('boda_amount')
        boda_weeklyPay = data.get('boda_weekly_pay')
        boda_phone = data.get('boda_phone_number')
        boda_nin = data.get('boda_nin_number')
        boda_ninPic = request.FILES.get('boda_nin_picture')
        boda_stage = data.get('boda_work_stage', 'None')

        # gurantor1
        gua1_name = data.get('gua1_name')
        gua1_stage = data.get('gua1_stage_name')
        gua1_phone = data.get('gua1_phone_number')
        gua1_nin = data.get('gua1_nin_number')
        gua1_ninPic = request.FILES.get('gua1_nin_picture')

        # guarantor 2
        gua2_name = data.get('gua2_name')
        gua2_stage = data.get('gua2_stage_name')
        gua2_phone = data.get('gua2_phone_number')
        gua2_nin = data.get('gua2_nin_number')
        gua2_ninPic = request.FILES.get('gua2_nin_picture')

        # guarantor 3
        gua3_name = data.get('gua3_name')
        gua3_stage = data.get('gua3_stage_name')
        gua3_phone = data.get('gua3_phone_number')
        gua3_nin = data.get('gua3_nin_number')
        gua3_ninPic = request.FILES.get('gua3_nin_picture')

        print(gua3_ninPic)
        print(":: gua2_phone ::", gua2_phone)

        date_of_application = data.get("date_of_application", None)
        parsedDate = datetime.now()
        if date_of_application and date_of_application != "":
            parsedDate = datetime.strptime(date_of_application, '%Y-%m-%d %H:%M')

        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_last_week = start_of_week - timedelta(days=6)
        
        try:


            add_boda_guy = BodaApply.objects.create(
                boda_guy_firstName=boda_firstName,
                boda_guy_lastName=boda_lastName,
                boda_numberPlate=boda_numberPlate,
                final_amount=boda_amount,
                weekly_pay=boda_weeklyPay,
                phone_number=boda_phone,
                nin_number=boda_nin,
                nin_picture=boda_ninPic,
                work_stage=boda_stage,
                guarantor1_name=gua1_name,
                guarantor1_stage_name=gua1_stage,
                guarantor1_number=gua1_phone,
                guarantor1_nin=gua1_nin,
                guarantor1_nin_picture=gua1_ninPic,
                guarantor2_name=gua2_name,
                guarantor2_stage_name=gua2_stage,
                guarantor2_number=gua2_phone,
                guarantor2_nin=gua2_nin,
                guarantor2_nin_picture=gua2_ninPic,
                guarantor3_name=gua3_name,
                guarantor3_stage_name=gua3_stage,
                guarantor3_number=gua3_phone,
                guarantor3_nin=gua3_nin,
                guarantor3_nin_picture=gua3_ninPic,
                date_of_application=parsedDate,
                latest_dateOfPay=start_of_last_week,
            )
            messages.success(request, boda_firstName + " " + boda_lastName + " Added successfully")

            return redirect('loan:add-boda')
        except Exception as e:
            print(str(e))

            messages.success(request, "Error, Kindly Try to check all the fields well and submit again!")

            return redirect('loan:add-boda')
    else:

        return render(request, "add_boda.html")


def boda_dashboard(request):
    if request.user.is_superuser:
        boda_monday = BodaApply.objects.filter(day_of_the_week="Monday", status="ACTIVE").all()
        boda_tuesday = BodaApply.objects.filter(day_of_the_week="Tuesday", status="ACTIVE").all()
        boda_wednesday = BodaApply.objects.filter(day_of_the_week="Wednesday", status="ACTIVE").all()
        boda_thursday = BodaApply.objects.filter(day_of_the_week="Thursday", status="ACTIVE").all()
        boda_friday = BodaApply.objects.filter(day_of_the_week="Friday", status="ACTIVE").all()
        boda_saturday = BodaApply.objects.filter(day_of_the_week="Saturday", status="ACTIVE").all()
        boda_sunday = BodaApply.objects.filter(day_of_the_week="Sunday", status="ACTIVE").all()

        context = {
            "boda_mon": reversed(boda_monday),
            "boda_tue": reversed(boda_tuesday),
            "boda_wed": reversed(boda_wednesday),
            "boda_thur": reversed(boda_thursday),
            "boda_fri": reversed(boda_friday),
            "boda_sat": reversed(boda_saturday),
            "boda_sun": reversed(boda_sunday),
            "mon_len": len(boda_monday),
            "tue_len": len(boda_tuesday),
            "wed_len": len(boda_wednesday),
            "thur_len": len(boda_thursday),
            "fri_len": len(boda_friday),
            "sat_len": len(boda_saturday),
            "sun_len": len(boda_sunday)
        }

        return render(request, "boda_dashboard.html", context)
    else:
        return redirect('account:admin-login')
        
#  search client boda
def search_client_boda(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            data = request.POST
            search_entry = data['client_search']
            if BodaApply.objects.filter(boda_guy_firstName=search_entry, status="ACTIVE").first():
                client = BodaApply.objects.filter(boda_guy_firstName=search_entry, status="ACTIVE").all()
                context = {
                    "client": client
                }
                return render(request, "search_client_boda.html", context)
            elif BodaApply.objects.filter(boda_guy_lastName=search_entry, status="ACTIVE").first():
                client = BodaApply.objects.filter(boda_guy_lastName=search_entry, status="ACTIVE").all()
                context = {
                    "client": client
                }
                return render(request, "search_client_boda.html", context)
            elif BodaApply.objects.filter(phone_number=search_entry, status="ACTIVE").first():
                client = BodaApply.objects.filter(phone_number=search_entry, status="ACTIVE").all()
                context = {
                    "client": client
                }
                return render(request, "search_client_boda.html", context)
            elif BodaApply.objects.filter(boda_numberPlate=search_entry, status="ACTIVE").first():
                client = BodaApply.objects.filter(boda_numberPlate=search_entry, status="ACTIVE").all()
                context = {
                    "client": client
                }
                return render(request, "search_client_boda.html", context)
            else:
                messages.info(request, "No such User")
                return redirect('loan:boda-dashboard')
        else:
            return redirect('loan:boda-dashboard')

    else:
        return redirect('account:user_login')

# manual add boda boda payment
def manual_add_boda_pay(request):
    if request.user.is_superuser:
        if request.method == "POST":
            data = request.POST
            bodaId = data.get('boda_id', 'none')
            paymentFee = data['payment_fee']
            phoneNumber = data['phone_number']
            status = "paid"

            print(bodaId)
            reference = uuid.uuid4()
            transaction_id = "manual pay"
            boda_obj = get_object_or_404(BodaApply, boda_id=bodaId)
            create_payment = BodaWeeklyPay.objects.create(
                boda_id = bodaId,
                boda_firstName = boda_obj.boda_guy_firstName,
                boda_lastName = boda_obj.boda_guy_lastName,
                payment_fee = paymentFee,
                phone_number = phoneNumber,
                reference = reference,
                transaction_id = transaction_id,
                status = status,
            )

            single_boda = boda_obj

            latest_deposit = single_boda.deposits + int(paymentFee)
            new_balance = single_boda.final_amount - latest_deposit

            new_phoneNumber = "+" + phoneNumber
            first_name = single_boda.boda_guy_firstName
            full_name = single_boda.boda_guy_firstName + " " + single_boda.boda_guy_lastName
            BodaApply.objects.filter(boda_id=bodaId).update(deposits=latest_deposit, balance=new_balance, latest_dateOfPay=datetime.today())

            try:
                response = send_boda_sms(first_name, paymentFee, datetime.today(), new_balance, new_phoneNumber)

            except Exception as e:
                print(str(e))
                pass
                
            messages.info(request, "user with BODA ID " + bodaId + " " + full_name + " paid " + str(paymentFee) + " successfully!")
            return redirect('loan:boda-dashboard')
        else:

            return render(request, "manual_add_boda_pay.html")

    else:
        return redirect('account:user_login')

# search client-boda for triggering
def search_boda_trigger(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            data = request.POST
            search_entry = data.get('client_search', False)
            print(search_entry)
            if BodaApply.objects.filter(boda_guy_firstName=search_entry, status="ACTIVE").first():
                client = BodaApply.objects.filter(boda_guy_firstName=search_entry, status="ACTIVE").all()

                serialized_data = serialize("json", client)
                data = json.loads(serialized_data)
                return JsonResponse ({"status": "success", "data": data})
            elif BodaApply.objects.filter(boda_guy_lastName=search_entry, status="ACTIVE").first():
                client = BodaApply.objects.filter(boda_guy_lastName=search_entry, status="ACTIVE").all()

                serialized_data = serialize("json", client)
                data = json.loads(serialized_data)
                return JsonResponse({"status": "success", "data": data})
            elif BodaApply.objects.filter(boda_numberPlate=search_entry, status="ACTIVE").first():
                client = BodaApply.objects.filter(boda_numberPlate=search_entry, status="ACTIVE").all()

                serialized_data = serialize("json", client)
                data = json.loads(serialized_data)
                return JsonResponse({"status": "success", "data": data})
            else:
                return JsonResponse({"status": "failed"})
        else:
            return redirect('loan:dashboard')

    else:
        return redirect('account:user_login')


# weekly logs
def weekly_logs(request):
    if request.user.is_superuser:
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        start_of_last_week = start_of_week - timedelta(days=7)
        end_of_last_week = start_of_week - timedelta(days=1)

        start_of_last_2weeks = start_of_last_week - timedelta(days=7)
        end_of_last_2week = start_of_last_week - timedelta(days=1)

        weekly_paid_bodas = BodaApply.objects.filter(latest_dateOfPay__gte=start_of_week, latest_dateOfPay__lte=end_of_week, status="ACTIVE").order_by('latest_dateOfPay').all()
        
        # Unpaid bodas for the current week
        weekly_unpaid_bodas = BodaApply.objects.filter(latest_dateOfPay__gte=start_of_last_week, latest_dateOfPay__lte=end_of_last_week, status="ACTIVE").order_by('latest_dateOfPay').all()
        
        # Unpaid bodas for the past two weeks excluding the current week
        two_weeks_unpaid_bodas = BodaApply.objects.filter(latest_dateOfPay__lte=end_of_last_2week, status="ACTIVE").order_by('latest_dateOfPay').all()

        context = {
            "paid": weekly_paid_bodas,
            "unpaid": weekly_unpaid_bodas,
            "len_paid": len(weekly_paid_bodas),
            "len_unpaid": len(weekly_unpaid_bodas),
            "two_weeks_unpaid_bodas": two_weeks_unpaid_bodas,
            "len_two_weeks_unpaid_bodas": len(two_weeks_unpaid_bodas)
        }
        return render(request, "boda_paid_weekly_logs.html", context)
    
    else:
        return redirect('account:user_login')


def full_week_logs(request):
    if request.user.is_superuser:
        today_res = BodaWeeklyPay.objects.filter(date__date=date.today()).all()
        today_no_tr = BodaWeeklyPay.objects.filter(date__date=date.today()).all().count()
        today_fee = BodaWeeklyPay.objects.filter(date__date=date.today()).aggregate(Sum('payment_fee'))
        today_fee_res = today_fee['payment_fee__sum']

        # weekly results
        current_date = date.today()
        today_date = current_date + timedelta(days=1)
        past_days = current_date - timedelta(days=7)
        week_res = BodaWeeklyPay.objects.filter(date__range=(past_days, today_date)).all()
        week_no_tr = BodaWeeklyPay.objects.filter(date__range=(past_days, today_date)).all().count()
        week_fee = BodaWeeklyPay.objects.filter(date__range=(past_days, today_date)).aggregate(Sum('payment_fee'))
        week_fee_res = week_fee['payment_fee__sum']

        # monthly results
        week_current_date = date.today()
        week_today_date = week_current_date + timedelta(days=1)
        past_weeks = week_current_date - timedelta(days=31)
        month_res = BodaWeeklyPay.objects.filter(date__range=(past_weeks, week_today_date)).all()
        month_no_tr = BodaWeeklyPay.objects.filter(date__range=(past_weeks, week_today_date)).all().count()
        month_fee = BodaWeeklyPay.objects.filter(date__range=(past_weeks, week_today_date)).aggregate(Sum('payment_fee'))
        month_fee_res = month_fee['payment_fee__sum']


        # All Payments
        allPay = BodaWeeklyPay.objects.all()
        total_no_tr = BodaWeeklyPay.objects.all().count()
        allPayFee = BodaWeeklyPay.objects.aggregate(Sum('payment_fee'))
        allPayFee_res = allPayFee['payment_fee__sum']






        print(date.today())
        print(datetime.now())
        context = {
            'todayRes': reversed(today_res),
            'todayFee': today_fee_res,
            'weekRes': reversed(week_res),
            'weekFee': week_fee_res,
            'monthRes': reversed(month_res),
            'monthFee': month_fee_res,
            'allPay': reversed(allPay),
            'allfeeRes': allPayFee_res,
            'today_no': today_no_tr,
            'weekly_no': week_no_tr,
            'monthly_no': month_no_tr,
            'total_no': total_no_tr,
        }
        return render(request, "all_boda_logs.html", context)

    else:
        return redirect('account:user_login')


def boda_details(request, bodaId):
    boda_obj = get_object_or_404(BodaApply, boda_id=bodaId)
    boda_payments = BodaWeeklyPay.objects.filter(boda_id=bodaId)
    print(len(boda_payments))
    context = {
        "boda_obj": boda_obj,
        "bodaPaymentObj": boda_payments
    }

    return render(request, "boda_details.html", context)

def sms_statuses(request):
    get_insights = reversed(SmsCallBack.objects.all())

    context = {
        "SMSz": get_insights
    }
    return render(request, "sms.html", context)


def edit_boda(request, bodaId):
    boda_obj = get_object_or_404(BodaApply, boda_id=bodaId)
    context = {}
    if boda_obj:
        context.update({
            "boda": boda_obj
        })

    if request.method == "POST":
        data = request.POST
        date_of_application = data.get("date_of_application", None)
        firstName = data.get("firstName", None)
        lastName = data.get("lastName", None)
        fullAmount = data.get("fullAmount", None)
        deposits = data.get("deposits", None)
        balance = data.get("balance", None)
        bodaNumberPlate = data.get("numberPlate", None)

        boda_obj.boda_guy_firstName = firstName
        boda_obj.boda_guy_lastName = lastName
        boda_obj.final_amount = fullAmount
        boda_obj.deposits = deposits
        boda_obj.balance = balance
        boda_obj.boda_numberPlate = bodaNumberPlate
        
        try:
            if date_of_application:
                parsed_date = datetime.strptime(date_of_application, '%b. %d, %Y, %I:%M %p')
                boda_obj.date_of_application = parsed_date

        except Exception as e:
            print(":: e ::", str(e))

        boda_obj.save()

        messages.info(request, str(boda_obj.boda_guy_firstName) + " " + str(boda_obj.boda_guy_lastName + "'s date of pay has been updated!!"))
        return redirect('loan:boda-dashboard')
        
    else:
        messages.info(request, 'there is something wrong!!!')
        return render(request, "edit_boda.html", context)


    return render(request, "edit_boda.html", context)


# make boda Active/InActive
def change_boda_status(request, boda_id):
    if request.user.is_superuser:
            data = request.POST
            if boda_id:
                boda_object = BodaApply.objects.filter(boda_id=boda_id).first()
                boda_status = boda_object.status
                new_status = "ACTIVE"
                if boda_status == "ACTIVE":
                    new_status = "INACTIVE"

                boda_object.status = new_status

                boda_object.save()

                messages.success(request, 'Boda status updated successfully!')

            else: 
                messages.error(request, 'failed to update boda status!')

            return redirect('loan:boda-dashboard')
    else:
        return redirect('account:user_login')




def archived_boda(request):
    if request.user.is_superuser:
        bodaPlate = request.GET.get("search_boda", None)
        if bodaPlate:
            bodas = BodaApply.objects.filter(boda_numberPlate=bodaPlate, status="INACTIVE").all()
        else:
            bodas = BodaApply.objects.filter(status="INACTIVE").all()

        context = {
            "client": bodas,
            "archived": True
        }
        return render(request, "search_client_boda.html", context)

    else:
        return redirect('account:user_login')


def cashflows(request):
    if request.user.is_superuser:
        date_search = request.GET.get("date_search", None)
        if date_search:
            parsedDate = datetime.strptime(date_search, '%b. %d, %Y, %I:%M %p').date()
            all_cashflows = CashFlow.objects.filter(date__date=parsedDate).all()
        else:
            all_cashflows = CashFlow.objects.all()
        context = {
            "cashflows": all_cashflows
        }
        return render(request, "all_cashflows.html", context)
    
    else:
        return redirect('account:user_login')
    
def addCashFlow(request):
    if request.user.is_superuser:
        if request.method == "GET":
            return render(request, "add_cashflow.html")
        
        if request.method == "POST":
            data = request.POST
            expenditures = data.get("expenditure", None)
            collections = data.get("collection", None)
            banked_amount = data.get("banked_amount", None)
            note = data.get("note", None)
            dateOfEntry = data.get("date_of_cashflow", None)

            parsedDate = datetime.now()
            if dateOfEntry and dateOfEntry != "":
                parsedDate = datetime.strptime(dateOfEntry, '%b. %d, %Y, %I:%M %p')

            create_record = CashFlow.objects.create(
               expenditures=expenditures,
               collections=collections,
               banked_balance=banked_amount,
               note=note,
               date=parsedDate
            )

            messages.success(request, "Expenditures & Collections Added successfully")
            return redirect("loan:cashflows")
        
    else:
        return redirect('account:user_login')
    

def advancedBodaInformation(request):
    if request.user.is_superuser:
        if request.method == "GET":
            numberPlate = request.GET.get("boda_search", None)
            if numberPlate:
                bodas = BodaInformation.objects.filter(numberPlate=numberPlate).all()
            else:
                bodas = BodaInformation.objects.all()

            context = {
                "bodas": bodas
            }
            return render(request, "boda_informations.html", context)
        
    else:
        return redirect('account:user_login')
    

def addBodainformation(request):
    if request.user.is_superuser:
        if request.method == "GET":
            all_bodas = BodaApply.objects.all()
            context = {
                "all_bodas": all_bodas
            }
            return render(request, "add_information.html", context)
        
        if request.method == "POST":
            data = request.POST
            BodaBodaNumberPlate = data.get("BodaBoda", None)
            rider = data.get("rider", None)
            amountBought = data.get("amountBought", None)
            whereBought = data.get("whereBought", None)
            LogBookNames = data.get("LogBookNames", None)
            demandedAmount = data.get("demandedAmount", None)
            isCompleted = data.get("isCompleted", None)
            is_complete = False
            if isCompleted == "True":
                is_complete = True

            add_record = BodaInformation.objects.create(
                numberPlate=BodaBodaNumberPlate,
                rider=rider,
                amountBought=amountBought,
                whereBought=whereBought,
                LogBookNames=LogBookNames,
                demandedAmount=demandedAmount,
                isCompleted=is_complete
            )

            messages.success(request, "Boda Information added successfully.")
            return redirect("loan:advanced-information")
        
def editBodaInformation(request, NumberPlate):
    if request.user.is_superuser:
        if request.method == "GET":
            bodaInfo = BodaInformation.objects.filter(numberPlate=NumberPlate).first()
            all_bodas = BodaApply.objects.all()
            context = {
                "all_bodas": all_bodas,
                "bodaInfo": bodaInfo
            }
            return render(request, "edit_boda_information.html", context)
        
        if request.method == "POST":
            data = request.POST
            BodaBodaNumberPlate = data.get("BodaBoda", None)
            rider = data.get("rider", None)
            amountBought = data.get("amountBought", None)
            whereBought = data.get("whereBought", None)
            LogBookNames = data.get("LogBookNames", None)
            demandedAmount = data.get("demandedAmount", None)
            isCompleted = data.get("isCompleted", None)
            
            is_complete = False
            if isCompleted == "True":
                is_complete = True

            get_InfoRecord = BodaInformation.objects.filter(numberPlate=NumberPlate).first()
            if get_InfoRecord:
                get_InfoRecord.numberPlate = BodaBodaNumberPlate
                get_InfoRecord.rider = rider
                get_InfoRecord.amountBought = amountBought
                get_InfoRecord.whereBought = whereBought
                get_InfoRecord.LogBookNames = LogBookNames
                get_InfoRecord.demandedAmount = demandedAmount
                get_InfoRecord.isCompleted = is_complete

                get_InfoRecord.save()

            messages.success(request, "Boda Information updated successfully.")
            return redirect("loan:advanced-information")
        

def resend_boda_sms(request, transID):
    get_payment = BodaWeeklyPay.objects.filter(id=transID).first()
    if not get_payment:
        messages.error(request, "Payment Not found.")
        return redirect("loan:full-week-logs")

    new_phoneNumber = "+" + get_payment.phone_number
    first_name = get_payment.boda_firstName
    full_name = get_payment.boda_firstName + " " + get_payment.boda_lastName
    paymentFee = get_payment.payment_fee
    bodaId = get_payment.boda_id

    boda_object = BodaApply.objects.filter(boda_id=bodaId).first()
    if not boda_object:
        messages.error(request, "Boda Boda Not found.")
        return redirect("loan:full-week-logs")
    
    new_balance = boda_object.balance
    date = get_payment.date
    try:
        response = send_boda_sms(first_name, paymentFee, date, new_balance, new_phoneNumber)

    except Exception as e:
        print(str(e))
        pass
        
    messages.info(request, "user with BODA ID " + bodaId + " " + full_name + " paid " + str(paymentFee) + " successfully!")
    return redirect('loan:boda-dashboard')


def send_boda_sms(full_name, paymentFee, date, new_balance, new_phoneNumber):
    message = "Hi " + full_name + ", paid " + str(paymentFee) + "UGX for BODA at Breniel on " + str(date.date()) + ". Bal: " + str(new_balance) + "UGX."
    url = "https://yoolasms.com/api/v1/send"
    payload = json.dumps({
        "phone": new_phoneNumber,
        "message": message,
        "api_key": yolasms_apiKey
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': str(uuid.uuid4())
    }
    response = requests.post(url, headers=headers, data=payload)
    print(":: response.text ::", response.text)
    print(":: response obj ::", response)

    return response