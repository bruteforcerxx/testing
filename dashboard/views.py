from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Transaction, Account, Authentication
from home.models import UsersData
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.utils import dateformat
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from threading import Thread
from .email import send_email  # requires parameters context, subject, destination, template
import smtplib, ssl
import random


@api_view(['GET', 'POST'])
def login_user(request):
    try:
        logout(request)
        if request.method == 'GET':
            logout(request)
            page = 'home/login.html'
            template = loader.get_template(page)
            logout(request)
            context = {'message': 'Welcome Back!! Login To Your Account', 'color': 'green'}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        if request.method == 'POST':
            logout(request)
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            user = User.objects.filter(email=email)
            print(user)
            if len(user) > 0:
                user = user[0]
                print(user)
                user = authenticate(username=user, password=password)
                print(user)
                if authenticate(username=user, password=password):
                    user = User.objects.get(username=user)
                    login(request, user)
                    return redirect(dash)
                else:
                    logout(request)
                    page = 'home/login.html'
                    template = loader.get_template(page)
                    logout(request)
                    context = {'message': 'Incorrect password, please try again.',
                               'color': 'red'}
                    return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

            else:
                logout(request)
                page = 'home/login.html'
                template = loader.get_template(page)
                logout(request)
                context = {'message': 'User does not exist, please try again or register a new account.',
                           'color': 'red'}
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        page = 'home/index.html'
        template = loader.get_template(page)
        context = {}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def dash(request):
    try:
        user = request.user
        print(user)
        user = User.objects.get(username=user)
        email = user.email
        print(Account.objects.all())
        acc = Account.objects.get(user=user)

        stat = acc.status
        c = str(acc.card)
        c2 = str(acc.card2)

        a1 = c[0:4]
        a2 = c[4:8]
        a3 = c[8:12]
        a4 = c[12:16]

        b1 = c2[0:4]
        b2 = c2[4:8]
        b3 = c2[8:12]
        b4 = c2[12:16]

        history = Transaction.objects.filter(user=user)
        trans = []
        acc_bal = 0
        credit = 0
        debit = 0
        for x in history:
            i = {'account': x.account_number, 'amount': bal_converter(str(x.amount)), 'currency': x.currency,
                 'date': dateformat.format(x.date, 'Y-m-d H:i:s'),
                 'status': x.status, 'type': x.type}
            if x.type == 'credit':
                acc_bal += x.amount
                credit += x.amount
            if x.type == 'debit':
                acc_bal -= x.amount
                debit += x.amount
            if x.status == 'failed':
                acc_bal -= x.amount

            trans.append(i)

        bal = Account.objects.get(user=user)
        loan = bal.loan
        bal.balance = acc_bal
        bal.credit = credit
        bal.debit = debit
        bal.save()
        trans.reverse()
        if len(trans) == 1:
            recent = [trans[0]]
        elif len(trans) == 2:
            recent = [trans[0]]
        elif len(trans) > 2:
            recent = [trans[0], trans[1], trans[2]]
        else:
            recent = []
        fl = UsersData.objects.get(user=user)
        fullname = fl.fullname
        dates = fl.date_created
        acc_bal = bal_converter(str(acc_bal))
        credit = bal_converter(str(credit))
        debit = bal_converter(str(debit))
        loan = bal_converter(str(loan))
        if stat == 'active':
            request.session['message'] = ''
            page = 'dash/dashboard.html'
            template = loader.get_template(page)
            context = {'user': user, 'email': email, 'balance': acc_bal, 'recent': recent, 'fullname': fullname,
                        'dates': dateformat.format(dates, 'Y-m-d H:i:s'), 'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4,
                       'b1': b1, 'b2': b2, 'b3': b3, 'b4': b4, 'credit': credit, 'debit': debit, 'loan': loan}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
        else:
            page = 'temps/blocked.html'
            template = loader.get_template(page)
            context = {'user': user, 'email': email, 'balance': acc_bal, 'recent': recent,
                       'dates': dateformat.format(dates, 'Y-m-d H:i:s'), 'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4,
                       'b1': b1, 'b2': b2, 'b3': b3, 'b4': b4}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        page = 'home/login.html'
        template = loader.get_template(page)
        context = {}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)


def bal_converter(x):
    if len(x) == 7:
        a = x[0]
        b = x[1:]
        return f'{a},{b}'
    if len(x) == 8:
        a = x[:2]
        b = x[2:]
        return f'{a},{b}'
    elif len(x) == 9:
        a = x[:3]
        b = x[3:]
        return f'{a},{b}'
    elif len(x) == 10:
        a = x[0]
        b = x[1:4]
        c = x[4:]
        return f'{a},{b},{c}'
    elif len(x) == 11:
        a = x[:2]
        b = x[2:5]
        c = x[5:]
        return f'{a},{b},{c}'
    elif len(x) == 12:
        a = x[:3]
        b = x[3:6]
        c = x[6:]
        return f'{a},{b},{c}'
    elif len(x) == 13:
        a = x[:2]
        b = x[2:5]
        c = x[5:]
        return f'{a},{b},{c}'
    else:
        return x


@api_view(['GET'])
def profile(request):
    try:
        page = 'dash/profile.html'
        template = loader.get_template(page)
        userlogged = request.user
        user = User.objects.get(username=userlogged)
        acc = Account.objects.get(user=user)
        account_number = acc.account_number
        email = user.email
        user = UsersData.objects.get(user=user)
        name = user.fullname
        date_created = user.date_created
        mobile = user.mobile_number
        country = user.country
        account = user.account_type

        context = {'fullname': name, 'account_number': account_number, 'account_type': account,
                   'email': email, 'country': country, 'date': dateformat.format(date_created, 'Y-m-d H:i:s'),
                   'mobile': mobile, 'dates': dateformat.format(date_created, 'Y-m-d H:i:s')}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        page = 'home/index.html'
        template = loader.get_template(page)
        context = {}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)


@api_view(['GET'])
def send(request):
    try:
        user = request.user
        user = User.objects.get(username=user)
        email = user.email
        acc = Account.objects.get(user=user)
        balance = bal_converter(str(acc.balance))
        fl = UsersData.objects.get(user=user)
        fullname = fl.fullname
        page = 'dash/send.html'
        template = loader.get_template(page)
        message = request.session['message']
        dates = fl.date_created
        context = {'user': user, 'email': email, 'balance': balance, 'fullname': fullname,
                   'message': message, 'dates': dates}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return redirect(dash)


@api_view(['GET', 'POST'])
def loans(request):
    if request.method == 'GET':
        try:
            user = request.user
            user = User.objects.get(username=user)
            email = user.email
            acc = Account.objects.get(user=user)
            balance = bal_converter(str(acc.balance))
            fl = UsersData.objects.get(user=user)
            fullname = fl.fullname
            page = 'dash/loans.html'
            template = loader.get_template(page)
            message = request.session['message']
            dates = fl.date_created
            context = {'user': user, 'email': email, 'balance': balance, 'fullname': fullname,
                       'message': message, 'dates': dates}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return redirect(dash)
    if request.method == 'POST':
        try:
            amount = request.POST.get('amount', '')
            category = request.POST.get('cat', '')

            pin = request.POST.get('pin', '')
            user = request.user
            user = User.objects.get(username=user)
            email = user.email

            acc = Account.objects.get(user=user)
            balance = bal_converter(str(acc.balance))
            fl = UsersData.objects.get(user=user)
            fullname = fl.fullname
            dates = fl.date_created

            if str(pin) == str(fl.pin):
                acc.loan = float(amount) + float(acc.loan)
                acc.save()

                trans = Transaction(user=user, amount=amount, currency='dollar', account_number=category, type='credit')
                trans.save()
                page = 'dash/success.html'
                template = loader.get_template(page)
                print(category)
                context = {'user': user, 'email': email, 'balance': balance, 'fullname': fullname, 'amount': amount,
                           'cat': category, 'dates': dates}
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

            else:
                request.session['message'] = 'Incorrect pin, please try again.'
                return redirect(loans)

        except Exception as e:
            print(e)
            return redirect('dash')


@api_view(['POST'])
def sent(request):
    try:
        amount = request.POST.get('amount', '')
        account_num = request.POST.get('account_number', '')
        currency = request.POST.get('currency', '')
        bank = request.POST.get('bank', '')
        name = request.POST.get('name', '')

        pin = request.POST.get('pin', '')
        user = request.user
        user = User.objects.get(username=user)
        email = user.email

        acc = Account.objects.get(user=user)
        fl = UsersData.objects.get(user=user)
        if pin == fl.pin:
            if float(amount) < float(acc.balance):
                request.session['transaction'] = [amount, account_num, currency, bank]
                token = random.randint(11111, 99999)

                print('transaction token is', token)

                request.session['token'] = token

                company = 'Webster City Union'

                print('###########################sending mail.....#######################################')
                context = {'token': token, 'name': user, 'company': company}
                print(context)
                subject = 'One Time Password'
                template = 'email/email_auth.html'
                new_thrd = Thread(target=send_email, args=(context, subject, email, template))
                new_thrd.start()

                page = 'dash/otp-1.html'
                template = loader.get_template(page)
                context = {}
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

            else:
                request.session['message'] = 'Insufficient funds, please try a lower amount.'
                return redirect(send)
        else:
            request.session['message'] = 'Incorrect pin, please try again.'
            return redirect(send)

    except Exception as e:
        print(e)
        return redirect(dash)


@api_view(['POST'])
def otp(request):
    try:
        print('start collecting data...')
        otp = request.POST.get('token', '')
        print(otp)
        auc = request.session['token']
        print(auc)

        auc_data = Authentication.objects.all()[0]
        auc_2 = auc_data.auc_token

        user = request.user
        user = User.objects.get(username=user)
        email = user.email

        acc = Account.objects.get(user=user)
        balance = bal_converter(str(acc.balance))
        fl = UsersData.objects.get(user=user)
        fullname = fl.fullname
        dates = fl.date_created
        det = request.session['transaction']
        amount = det[0]
        account_num = det[1]
        currency = det[2]
        bank = det[3]
        if str(otp) == str(auc):
            print('right otp')
            acc.balance = float(acc.balance) - float(amount)
            acc.save()
            trans = Transaction(user=user, amount=amount, currency=currency, account_number=account_num)
            trans.save()
            page = 'dash/sent.html'
            template = loader.get_template(page)
            print(account_num)
            context = {'user': user, 'email': email, 'balance': balance, 'fullname': fullname,
                       'amount': bal_converter(str(amount)), 'account': account_num, 'dates': dates,
                       'bank': f"{bank} bank", 'type': ''}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
        elif str(otp) == str(auc_2):
            print('right admin otp')
            acc.balance = float(acc.balance) - float(amount)
            acc.save()
            trans = Transaction(user=user, amount=amount, currency=currency, account_number=account_num)
            trans.save()
            page = 'dash/sent.html'
            template = loader.get_template(page)
            print(account_num)
            context = {'user': user, 'email': email, 'balance': balance, 'fullname': fullname,
                       'amount': bal_converter(str(amount)),
                       'account_num': account_num, 'dates': dates, 'bank': f"{bank} bank",  'type': ''}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
        else:
            print('wrong otp')
            page = 'dash/otp-1.html'
            template = loader.get_template(page)
            context = {'message': 'Invalid otp, please try again', 'type': 'invalid'}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return redirect(dash)


def resend_otp(request):
    try:
        user = request.user
        user = User.objects.get(username=user)
        email = user.email

        fl = UsersData.objects.get(user=user)

        amount = request.session['transaction'][0]
        token = request.session['token']
        company = 'Aviasta Trust'

        print('transaction token is', token)

        request.session['token'] = token

        print('###########################sending mail.....#######################################')
        context = {'otp': token, 'user': fl, 'company': company, 'website': 'salford-capital.com', 'amount': amount}
        print(context)
        subject = 'Authentication Token'
        template = 'email/auc.html'
        new_thrd = Thread(target=send_email, args=(context, subject, email, template))
        new_thrd.start()

        page = 'dash/otp-1.html'
        template = loader.get_template(page)
        context = {}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return redirect(dash)


@api_view(['GET'])
def transactions(request):
    try:
        user = request.user
        user = User.objects.get(username=user)
        userdata = UsersData.objects.get(user=user)
        name = userdata.fullname
        dates = userdata.date_created
        email = user.email
        history = Transaction.objects.filter(user=user)
        trans = []
        for x in history:
            i = {'account': x.account_number, 'amount': bal_converter(str(x.amount)), 'currency': x.currency, 'date': x.date,
                 'status': x.status, 'type': x.type, }
            trans.append(i)
        page = 'temps/history.html'
        trans.reverse()
        pending = 0
        success = 0
        failed = 0
        for s in trans:
            if s['status'] == 'pending':
                pending += 1
            if s['status'] == 'success':
                success += 1
            if s['status'] == 'failed':
                failed += 1
        total = success + pending + failed
        template = loader.get_template(page)
        context = {'fullname': name, 'email': email, 'transactions': trans, 'pending': pending,
                   'success': success, 'failed': failed, 'total': total, 'dates': dates}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return redirect(dash)


@api_view(['GET'])
def sendmail(request):
    try:

        print('starting.........')
        ctx = {
            'user': "Ajay"
        }
        message = get_template('home.html').render(ctx)
        msg = EmailMessage(
            'Subject',
            message,
            'help.greentrust@outlook.com',
            ['olumichael2015@outlook.com'],
        )
        msg.content_subtype = "html"  # Main content is now text/html
        print('sending...........')
        msg.send()
        print("Mail successfully sent")
        page = 'temps/sendmail.html'
        template = loader.get_template(page)
        logout(request)
        return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return redirect(dash)


@api_view(['GET'])
def verifymail(request):
    try:
        page = 'temps/verified.html'
        template = loader.get_template(page)
        logout(request)
        email = ''
        name = User.objects.get(email=email)
        name = UsersData.objects.get(user=name)
        name = name.fullname
        context = {'message': '', 'name': name}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return redirect(dash)


