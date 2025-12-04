from django.contrib.auth.models import User
from django import forms
from .models import Note
class Signup_form(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email']
    def clean(self):
            cleaned=super().clean()
            p1=cleaned.get('password')
            p2=cleaned.get('confirm_password')
            if p1 and p2 and p1 != p2:
                self.add_error("confirm_password",'password do not match ')
            return cleaned
    def clean_username(self):
         username=self.cleaned_data.get('username')
         if User.objects.filter(username=username).exists():
              raise forms.ValidationError('This username already taken')
         return username
class Noteform(forms.ModelForm):
     class Meta:
          model=Note
          fields=['title','content']
              