from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .forms import EmailForm
# Create your views here.


def send_email(request):

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = request.POST.get("subject", "")
            message = request.POST.get("message", "")
            mailTo = request.POST.get("mailTo", "")

            email = EmailMessage(subject, message, to=[mailTo])
            reponse = email.send()
            return redirect('/')
    else:
        form = EmailForm()
    
    return render(request, 'mailer/email_form_page.html', {'form': form})

