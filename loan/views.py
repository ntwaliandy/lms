from contextlib import redirect_stderr
from datetime import datetime, date, timedelta
import uuid
import imp
import json
from random import randint
from time import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from home.models import Apply, GroupApply, PermitApply, Support
from .models import AddPayment, AddPermitPayment, FileUpload, GroupAddPayment, Replies
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
                    status = 'paid',
                    admin = username
                )
                messages.info(request, "user with permit ID " + str(permitId) +" paid " + str(paymentFee) + " successfully")
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
    if request.user.username == "george@accessm.com":
        user_name = request.user.username
        permits = PermitApply.objects.filter(Q(status = "applied"), Q(admin = user_name) |Q(admin = "null")).all()
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

            AddPermitPayment.objects.create(
                permit_id = permitId,
                payment_fee = paymentFee,
                phone_number = phoneNumber,
                reference = reference,
                transaction_id = transaction_id,
                status = status,
                admin = username
            )

            username = "EREMIT" 
            api_key = "ecc0e2d4f576d07a7fe6b2268b1f0937d2c9a0a1949ed60036d2a5ca6c44826d"     
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

            sms.send("hey " + full_name + ", you have successfully paid " + str(paymentFee) + "UGX for your " + service + " permit service and your outstanding balance is " + str(new_balance) + "UGX. Thank you!!!", [new_phoneNumber], callback=on_finish)
            messages.info(request, "user with Permit ID " + permitId + " paid " + str(paymentFee) + " successfully!")
            return redirect('loan:permit-dashboard')
        else:
            messages.info(request, "failed to add the record manually")
            return render(request, 'add_permit_payment.html', context)
    else:
        messages.info(request, "Only George is Allowed to Enter values HERE!!!!!")
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
        elif result == 'SUCCESSFUL' and statuss == 'not paid':
            username = "EREMIT" 
            api_key = "ecc0e2d4f576d07a7fe6b2268b1f0937d2c9a0a1949ed60036d2a5ca6c44826d"     
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

            sms.send("hey " + full_name + ", you have successfully paid " + str(fee) + "UGX for your " + service + " permit service and your outstanding balance is " + str(new_balance) + "UGX. Thank you!!!", [new_phoneNumber], callback=on_finish)
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
        context = {
            'files': individual_files,
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
            else:
                messages.info(request, "No such User")
                return redirect('loan:dashboard')
        else:
            return redirect('loan:dashboard')

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

    
     



def on_finish(error, response):
    if error is not None:
        raise error
    print(response)