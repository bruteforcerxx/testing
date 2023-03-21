from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
# Create your views here.


def send_email(context, subject, destination, template):
    print('###########################sending mail.....#######################################')

    host = 'http://192.168.0.161:8000/'
    host2 = 'https://webstercitiunion.com'

    context['image1'] = f'{host}/static/emails/image-1.png'
    context['image2'] = f'{host}/static/emails/image-2.png'
    context['image3'] = f'{host}/static/emails/image-3.png'
    context['image4'] = f'{host}/static/emails/image-4.png'
    context['image5'] = f'{host}/static/emails/image-5.png'
    context['color'] = '#DAF7A6'
    context['subject'] = subject
    context['email'] = 'office@webstercitiunion.com'
    context['phone'] = ''
    context['company'] = 'Webster City Union'
    context['website'] = 'www.webstercitiunion.com'
    print(context)

    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    from_email = 'Webster City Union <office@webstercitiunion.com>'
    to = str(destination)
    print(context)
    print(mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message,
                         fail_silently=True))
    print(mail.send_mail(subject, plain_message, from_email, ['office@webstercitiunion.com'],
                         html_message=html_message, fail_silently=True))

    print('###########################sending mail completed#######################################')