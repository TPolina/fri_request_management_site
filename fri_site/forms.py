from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['responsible', 'status']
        labels = {'responsible': 'Відповідальний:', 'status': 'Змінити статус:'}
        widgets = {'responsible': forms.TextInput(attrs={'class': 'form_box'}),
                   'status': forms.Select(attrs={'class': 'form_box'})}
