from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
import os

# Create your views here.
def index(request):
  return render(request, 'web_app/index.html')

def test(request):
  if request.method == 'POST':

    # Gather data submitted from the "Contact Us" form
    name = request.POST['name']
    address = request.POST['address']
    phone = request.POST['phone']
    email = request.POST['email']
    message = request.POST['message']

    # print('name: ', name, 'address: ', address, 'phone: ', phone, 'email: ', email, 'message: ', message)

    # Save data submitted from the "Contact Us" form to sqlite3 database
    from web_app.models import Message
    m = Message(name=name, address=address, phone=phone, email=email, message=message)
    m.save()

    # Set the email address for the site administrator
    email_admin = os.getenv("EMAIL_ADMIN")

    # Send a notification message to the site administrator when "Contact Us" form
    # is submitted
    send_mail(
      'River City Pro Wash -- Contact Us form submission notification',
      'Name: {}\nAddress: {}\nPhone: {}\nEmail: {}\nMessage: {}'.format(name, address, phone, email, message),
      email_admin,
      [email_admin],
      fail_silently=False,
    )

    # Send a thank you message to the user who submitted the "Contact Us" form
    send_mail(
      'Thank you for contacting River City Pro Wash!',
      'Dear {},\n\nThank you for contacting River City Pro Wash! A member of our team will be in touch with you shortly.\n\nRegards,\nRiver City Pro Wash'.format(name),
      email_admin,
      [email],
      fail_silently=False,
    )

  return render(request, 'web_app/test.html')