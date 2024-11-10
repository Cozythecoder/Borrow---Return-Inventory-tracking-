from django import forms
from .models import BotDetail

class BotDetailForm(forms.ModelForm):
    class Meta:
        model = BotDetail
        fields = ['token', 'chat_id']
        widgets = {
            'token': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Telegram Bot Token'}),
            'chat_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Chat ID/Group ID'}),
        }