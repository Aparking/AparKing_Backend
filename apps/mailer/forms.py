from django import forms

class EmailForm(forms.Form):
    mailTo = forms.EmailField(label='Destinatario')
    subject = forms.CharField(max_length=100, label='Asunto')
    message = forms.CharField(widget=forms.Textarea, label='Mensaje')
    