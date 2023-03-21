from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import UsersData, Contact
from dashboard.models import Account
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
import random
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from threading import Thread
from .email import send_email  # requires parameters context, subject, destination, template
import smtplib, ssl

# Create your views here.


@api_view(['GET'])
def home_page(request):
    page = 'home/index.html'
    template = loader.get_template(page)
    logout(request)
    return HttpResponse(template.render({'header': 'TESTING ABOUT VIEW'}, request), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def register(request):
    print('STARTING REGISTER FUNCTION')
    try:
        if request.method == 'GET':
            page = 'home/register.html'
            template = loader.get_template(page)
            logout(request)
            return HttpResponse(template.render({'form': ''}, request), status=status.HTTP_200_OK)

        if request.method == 'POST':

            firstname = request.POST.get('firstname', '')
            lastname = request.POST.get('lastname', '')
            phone = request.POST.get('phone', '')
            email = request.POST.get('email', '')
            account_type = request.POST.get('account', '')
            dob = request.POST.get('dob', '')
            gender = request.POST.get('gender', '')
            fname = request.POST.get('fathersname', '')
            mname = request.POST.get('mothersname', '')
            marry_type = request.POST.get('marry', '')
            spousename = request.POST.get('sname', '')
            nation = request.POST.get('nation', '')
            occupation = request.POST.get('occupation', '')
            income = request.POST.get('income', '')
            address = request.POST.get('address', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip = request.POST.get('zip', '')
            country = request.POST.get('country', '')

            name = f'{firstname} {lastname}'

            details = [name, phone, email, account_type, dob, gender, fname, mname, marry_type, spousename,
                       nation, occupation, income, address, city, state, zip, country]
            check = User.objects.filter(email=details[2])
            check2 = User.objects.filter(username=details[0])

            if check:
                message = 'email already in use, please try another'
                page = 'home/register..html'
                template = loader.get_template(page)
                logout(request)
                context = {'message': message, 'color': 'red'}
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

            if check2:
                message = 'name already in use, please try another'
                page = 'home/register..html'
                template = loader.get_template(page)
                logout(request)
                context = {'message': message, 'color': 'red'}
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

            print('REDIRECTING OTP')
            request.session['register'] = details
            return redirect(otp)

        else:
            page = 'index.html'
            template = loader.get_template(page)
            logout(request)
            return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        page = 'index.html'
        template = loader.get_template(page)
        logout(request)
        return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def otp(request):
    print('STARTING OTP FUNCTION')
    try:
        if request.method == 'GET':
            token = random.randint(11111, 99999)


            print('token is', token)
            request.session['token'] = token
            user_data = request.session['register']

            username = user_data[0]
            email = user_data[2]
            company = 'Webster City Union'

            print('###########################sending mail.....#######################################')
            context = {'token': token, 'name': username, 'company': company}
            print(context)
            subject = 'One Time Password'
            template = 'email/email.html'
            new_thrd = Thread(target=send_email, args=(context, subject, email, template))
            new_thrd.start()

            page = 'home/otp.html'
            template = loader.get_template(page)
            context = {'message': f'An otp was sent to {email}, please provide the email below to continue',
                       'color': ''}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        if request.method == 'POST':
            print('STARTING OTP POST FUNCTION')
            otp = request.POST.get('otp', '')
            otp_token = request.session['token']
            user_data = request.session['register']

            print(otp, otp_token)

            if str(otp) == str(otp_token):
                print(otp)
                print('OTP IS VALID')
                page = 'home/password.html'
                template = loader.get_template(page)
                context = {'message': 'Email verified successfully!, please create a password to continue',
                           'color': 'green'}
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
            else:
                page = 'home/otp.html'
                template = loader.get_template(page)
                context = {'message': 'incorrect otp!, please try again', 'color': 'red'}
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return redirect(' ')


@api_view(['POST'])
def password(request):
    print('STARTING PASSWORD FUNCTION')
    try:
        pwd1 = request.POST.get('password1', '')
        pwd2 = request.POST.get('password2', '')
        pin1 = request.POST.get('pin1', '')
        pin2 = request.POST.get('pin2', '')

        if pwd1 == pwd2:
            if pin1 == pin2:
                data = request.session['register']
                print('REGISTERING USER')
                new_user = f'{data[0]}{random.randint(1111, 9999)}'
                info = User.objects.create_user(username=new_user, email=data[2], password=pwd1)
                info.save()
                user = User.objects.get(username=new_user)
                print('saving user data...')
                user_data = UsersData(user=user, fullname=data[0], mobile_number=data[1], email_address=data[2], account_type=data[3],
                                      date_of_birth=data[4], gender=data[5], fathers_name=data[6], mothers_name=data[7],
                                      marital_status=data[8], spouses_name=data[9], nationality=data[10], occupation=data[11],
                                      monthly_income=data[12], address=data[13], city=data[14], state=data[15], zip_code=data[16],
                                      country=data[17], pin=pin1, password=pwd1)
                user_data.save()
                print('user data saved')
                account = Account(user=user)
                account.save()
                print('user account saved')

                if authenticate(username=user, password=pwd1):
                    logout(request)
                    login(request, user)
                    return redirect('dash')
                else:
                    logout(request)
                    return redirect('home')
            else:
                page = 'home/password.html'
                template = loader.get_template(page)
                return HttpResponse(template.render({'message': 'pins do not match', 'color': 'red'}, request), status=status.HTTP_200_OK)
        else:
            page = 'home/password.html'
            template = loader.get_template(page)
            return HttpResponse(template.render({'message': 'passwords do not match', 'color': 'red'}, request), status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        page = 'home/index.html'
        template = loader.get_template(page)
        logout(request)
        return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return redirect(home_page)


def test(request):
    token = '939393'
    username = 'tester'
    company = 'Aviasta Trust'
    email = 'olumichael2016x@gmail.com'
    context = {'otp': token, 'user': username, 'company': company, 'email': email}
    print(context)
    subject = 'One Time Password'
    template = 'email/otp.html'
    new_thrd = Thread(target=send_email, args=(context, subject, email, template))
    new_thrd.start()

    page = 'email/register_otp.html'

    template = loader.get_template(page)
    return HttpResponse(template.render({'otp': token, 'user': username, 'company': company, 'email': email}, request), status=status.HTTP_200_OK)


def about(request):
    page = 'home/about.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'header': 'TESTING SERVICES VIEW'}, request), status=status.HTTP_200_OK)


def loans(request):
    page = 'home/loans.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'header': 'TESTING SERVICES VIEW'}, request), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def contact(request):
    try:
        if request.method == 'GET':
            page = 'home/contact.html'
            template = loader.get_template(page)
            return HttpResponse(template.render({'header': 'TESTING SERVICES VIEW'}, request),
                                status=status.HTTP_200_OK)

        if request.method == 'POST':
            name = request.POST.get('name', '')
            phone = request.POST.get('phone', '')
            email = request.POST.get('email', '')
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')

            cont = Contact(fullname=name, mobile_number=phone, email_address=email, subject=subject, message=message)
            cont.save()
            page = 'home/thanks.html'
            template = loader.get_template(page)
            logout(request)
            return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)

        else:
            page = 'home/index.html'
            template = loader.get_template(page)
            logout(request)
            return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        page = 'home/index.html'
        template = loader.get_template(page)
        logout(request)
        return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def support(request):
    try:
        if request.method == 'GET':
            page = 'home/support.html'
            template = loader.get_template(page)
            return HttpResponse(template.render({'header': 'TESTING SERVICES VIEW'}, request),
                                status=status.HTTP_200_OK)

        if request.method == 'POST':
            name = request.POST.get('name', '')
            phone = request.POST.get('phone', '')
            email = request.POST.get('email', '')
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')

            cont = Contact(fullname=name, mobile_number=phone, email_address=email, subject=subject, message=message)
            cont.save()
            page = 'home/thanks.html'
            template = loader.get_template(page)
            logout(request)
            return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)

        else:
            page = 'home/index.html'
            template = loader.get_template(page)
            logout(request)
            return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        page = 'home/index.html'
        template = loader.get_template(page)
        logout(request)
        return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)


@api_view(['GET'])
def test(request):
    try:
        name = 'Michael'
        phone = '08108105750'
        email = 'olumichael2016x@gmail.com'
        service = 'logistics'
        message = 'message'
        date = '20/3/2005'
        token = '55993'

        context = {'name': name, 'email': email, 'service': service, 'message': message, 'date': date,
                   'token': token, 'website': 'www.webstercitiunion.com'}
        template = 'email/email.html'
        subject = 'Appointment Booked'

        print('***********mail sender starting************')
        new_thrd = Thread(target=send_email, args=(context, subject, email, template))
        new_thrd.start()

        page = 'email/email.html'
        template = loader.get_template(page)
        host = 'http://192.168.0.161:8000/'
        host2 = 'https://hobnobng.org'

        context['name'] = 'Mike'
        context['image1'] = f'{host}/static/emails/image-1.png'
        context['image2'] = f'{host}/static/emails/image-2.png'
        context['image3'] = f'{host}/static/emails/image-3.png'
        context['image4'] = f'{host}/static/emails/image-4.png'
        context['image5'] = f'{host}/static/emails/image-5.png'
        context['color'] = '#DAF7A6'
        context['subject'] = 'One time password '
        context['email'] = 'office@webstercitiunion.com'
        context['phone'] = ''
        context['company'] = 'Webster City Union'
        context['website'] = 'www.webstercitiunion.com'
        print(context)
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        page = 'index.html'
        template = loader.get_template(page)
        logout(request)
        return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)

