import http.client
import json
from random import randint
import uuid
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from .models import Apply, GroupApply, PermitApply, Support
from loan.models import AddPayment, Replies
from datetime import datetime
from django.contrib.auth import get_user_model
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.

def index(request):
        return render(request, 'index.html')

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
            elif loan_amount == '':
                messages.info(request, 'user field empty')
            else:
                ref = uuid.uuid4()
                conn = http.client.HTTPSConnection("api.cissytech.com")
                payload = json.dumps({
                "apiKey": "cf5eaeba-fbb4-42e2-8c3f-de00ce969a4f",
                "phone": telephone,
                "amount": 5000,
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
                        transction_id = transId,
                        loan_amount = loan_amount,
                        reference = ref,
                        status = "fee_not_paid",
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
                date = request.POST.get('date_modified', datetime.now())
            )
            return redirect('home:index')
        else:
            return render(request, 'group-apply.html')
    else:
        return redirect('account:user_login')



# permit Apply
def permit_apply(request):
    if request.user.is_authenticated:
        User = get_user_model()
        admin_users = User.objects.filter(is_staff=True)
        context = {"admin_users": admin_users}
        if request.method == 'POST':
            data = request.POST
            firstName = data['first_name']
            lastName = data['last_name']
            phoneNumber = data['telephone']
            service_price = data['service']
            mess = data['message']
            date = datetime.now()
            user_admin = data['assigned']

            PermitApply.objects.create(
                first_name = firstName,
                last_name = lastName,
                phone_number = phoneNumber,
                service = mess,
                final_amount = service_price,
                message = mess,
                status = 'applied',
                date_modified = date,
                admin = user_admin
            )

            return redirect('home:index')
        else:
            return render(request, 'apply-permit.html', context)
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


def support(request):
    if request.user.is_authenticated:
        username = request.user.username
        replies = Replies.objects.all()
        support = Support.objects.filter(user = username).all()
        context = {
            'replies': replies,
            'support': support,
        }
        if request.method == 'POST':
            data = request.POST
            email = data['email']
            question = data['question']

            #inserting them to the db
            Support.objects.create(
                user = username,
                email = email,
                question = question,
            )
            return redirect('home:index')
        return render(request, 'support.html', context)
    else:
        return redirect('account:user_login')
    
    
def about(request):
    return render(request, 'about.html')


@csrf_exempt
def sms(request):
    if request.method == 'GET':
        try:
            callback_data = request.GET
            
            print("Received Callback Data:", callback_data)

            return JsonResponse({'status': 'success'})
        
        except Exception as e:
            print("Error processing callback:", e)
            return JsonResponse({'status': 'error'})
    
    return JsonResponse({'status': 'method not allowed'}, status=405)