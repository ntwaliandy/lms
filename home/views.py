
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Apply, GroupApply
from loan.models import AddPayment
from datetime import datetime

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('account:user_login')

# single application
def user_apply(request):
    if request.user.is_authenticated:
        username = request.user.username
        
        if request.method == 'POST':
            data = request.POST
            first_name = data['first_name']
            last_name = request.POST.get('last_name', 'null')
            national_id = data['national_id']
            telephone = data['telephone']
            pic_id = request.FILES.get('pic_id')
            person_pic = request.FILES.get('person_pic')
            first_guarrante_full_names = data['first_guarrante_full_names']
            first_guarrante_national_id = data['first_guarrante_national_id']
            first_guarrante_telephone = data['first_guarrante_telephone']
            first_guarrante_pic_id = request.FILES.get('first_guarrante_pic_id')
            second_guarrante_full_names = data['second_guarrante_full_names']
            second_guarrante_national_id = data['second_guarrante_national_id']
            second_guarrante_telephone = data['second_guarrante_telephone']
            second_guarrante_pic_id = request.FILES.get('second_guarrante_pic_id')
            transction_id = request.POST.get('transction_id', 'null')
            loan_amount = data['loan_amount']
            date = request.POST.get('date', datetime.now())
            

            # form validations
            if first_name == '':
                messages.info(request, 'first name cant be empty')
            elif last_name == '':
                messages.info(request, 'last name cant be empty!')
            elif national_id == '':
                messages.info(request, 'NIN cant be empty')
            elif telephone == '':
                messages.info(request, 'user field empty')
            elif pic_id == '':
                messages.info(request, 'user field empty')
            elif person_pic == '':
                messages.info(request, 'user field empty')
            elif first_guarrante_full_names == '':
                messages.info(request, 'user field empty')
            elif first_guarrante_national_id == '':
                messages.info(request, 'user field empty')
            elif first_guarrante_telephone == '':
                messages.info(request, 'user field empty')
            elif first_guarrante_pic_id == '':
                messages.info(request, 'user field empty')
            elif second_guarrante_full_names == '':
                messages.info(request, 'user field empty')
            elif second_guarrante_national_id == '':
                messages.info(request, 'user field empty')
            elif second_guarrante_telephone == '':
                messages.info(request, 'user field empty')
            elif second_guarrante_pic_id == '':
                messages.info(request, 'user field empty')
            elif transction_id == '':
                messages.info(request, 'user field empty')
            elif loan_amount == '':
                messages.info(request, 'user field empty')
            else:
                # insert the records to the database
                Apply.objects.create(
                    first_name = first_name,
                    last_name = last_name,
                    national_id = national_id,
                    telephone = telephone,
                    pic_id = pic_id,
                    person_pic = person_pic,
                    first_guarrante_full_names = first_guarrante_full_names,
                    first_guarrante_national_id = first_guarrante_national_id,
                    first_guarrante_telephone = first_guarrante_telephone,
                    first_guarrante_pic_id = first_guarrante_pic_id,
                    second_guarrante_full_names = second_guarrante_full_names,
                    second_guarrante_national_id = second_guarrante_national_id,
                    second_guarrante_telephone = second_guarrante_telephone,
                    second_guarrante_pic_id = second_guarrante_pic_id,
                    transction_id = transction_id,
                    loan_amount = loan_amount,
                    user = username,
                    date = date,
                )
                return redirect('home:index')
        else:
            return render(request, 'apply.html')
    else:
        return redirect('account:user_login')



# group application
def group_apply(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.method == 'POST':
            data = request.POST
            general_number = data['general_number']
            first_person_full_names = data['first_person_full_names']
            first_person_telephone = data['first_person_telephone']
            first_person_national_id = data['first_person_national_id']
            first_person_national_id_pic = request.FILES.get('first_person_national_id_pic')
            first_person_pic = request.FILES.get('first_person_pic')
            second_person_full_names = data['second_person_full_names']
            second_person_telephone = data['second_person_telephone']
            second_person_national_id = data['second_person_national_id']
            second_person_national_id_pic = request.FILES.get('second_person_national_id_pic')
            second_person_pic = request.FILES.get('second_person_pic')
            third_person_full_names = data['third_person_full_names']
            third_person_telephone = data['third_person_telephone']
            third_person_national_id = data['third_person_national_id']
            third_person_national_id_pic = request.FILES.get('third_person_national_id_pic')
            third_person_pic = request.FILES.get('third_person_pic')
            fourth_person_full_names = data['fourth_person_full_names']
            fourth_person_telephone = data['fourth_person_telephone']
            fourth_person_national_id = data['fourth_person_national_id']
            fourth_person_national_id_pic = request.FILES.get('fourth_person_national_id_pic')
            fourth_person_pic = request.FILES.get('fourth_person_pic')
            loan_amount = data['loan_amount']
            date = request.POST.get('date', datetime.now())

            GroupApply.objects.create(
                user = username,
                general_number = general_number,
                first_person_full_names = first_person_full_names,
                first_person_telephone = first_person_telephone,
                first_person_national_id = first_person_national_id,
                first_person_national_id_pic = first_person_national_id_pic,
                first_person_pic = first_person_pic,
                second_person_full_names = second_person_full_names,
                second_person_telephone = second_person_telephone,
                second_person_national_id = second_person_national_id,
                second_person_national_id_pic = second_person_national_id_pic,
                second_person_pic = second_person_pic,
                third_person_full_names = third_person_full_names,
                third_person_telephone = third_person_telephone,
                third_person_national_id = third_person_national_id,
                third_person_national_id_pic = third_person_national_id_pic,
                third_person_pic = third_person_pic,
                fourth_person_full_names = fourth_person_full_names,
                fourth_person_telephone = fourth_person_telephone,
                fourth_person_national_id = fourth_person_national_id,
                fourth_person_national_id_pic = fourth_person_national_id_pic,
                fourth_person_pic = fourth_person_pic,
                loan_amount = loan_amount,
                date = date
            )
            return redirect('home:index')
        else:
            return render(request, 'group-apply.html')
    else:
        return redirect('account:user_login')


# user loans records
def my_loans(request):
    if request.user.is_authenticated:
        username = request.user.username
        my_loans = reversed(Apply.objects.filter(user = username))
        
        context = {
            'my_loans': my_loans
        }
        return render(request, 'my-loans.html', context)
    else:
        return redirect('account:user_login')


# user daily payments
def my_payments(request):
    if request.user.is_authenticated:
        username = request.user.username
        my_loans = Apply.objects.filter(user = username)
        my_payments = AddPayment.objects.all()

        context = {
            'my_loans': my_loans,
            'my_payments': my_payments
        }
        return render(request, 'my_payments.html', context)
    else:
        return redirect('account:user_login')

