from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from home.models import Apply, GroupApply, Support
from .models import AddPayment, GroupAddPayment, Replies
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth import get_user_model
# Create your views here.
from django.core.mail import send_mail
from django.core.mail import EmailMessage

def dashboard(request):
    if request.user.is_superuser:
        applied_loans = Apply.objects.count()
        total_loans = Apply.objects.aggregate(Sum('loan_amount'))
        total_sales = Apply.objects.filter(status='completed').aggregate(Sum('payback'))
        recent_loans = reversed(Apply.objects.filter(status = 'pending').order_by('date')[:3])
        loans = Apply.objects.all()

        context = {
            'applied_loans': applied_loans,
            'total_loans': total_loans,
            'recent_loans': recent_loans,
            'total_sales': total_sales,
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
                AddPayment.objects.create(
                    loan_id = loan_id,
                    payment_fee = payment_fee,
                    transaction_id = transaction_id,
                    paid = paid,
                    date = date,
                    admin = username
                )
                return redirect('loan:dashboard')
        else:
            return render(request, 'add_payment.html', context)

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
        payment = AddPayment.objects.filter(paid = 'NO').all()
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
    
    for payment in payments:
        single_loan_id = payment.loan_id
        payments = payment.payment_fee
        transaction = payment.transaction_id
        paid = payment.paid,
        dateofpay = payment.date,
        admin = payment.admin
    subject = 'hello everyone'
    recipient = 'ntwaliandy90@gmail.com'
    sender = 'ntwaliandrew00@gmail.com'
    message = '{ <br>' + 'LOAN ID: ' + str(single_loan_id) + '<br> Payments: ugx ' + str(payments) + '<br> Transaction ID: ' + str(transaction) + '<br> PAID? : ' + str(paid) + '<br> DATE of Pay: ' + str(dateofpay) + '<br> Approved By: ' + str(admin) + '<br> }'
    
    msg = EmailMessage(subject, message, sender, [recipient])
    msg.content_subtype = "html"
    msg.send()
    
    return redirect('loan:dashboard')
    
     