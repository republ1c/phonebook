from django import forms
from .models import User
from .models import PhoneNumber


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'user_surname', 'user_email']

        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_surname': forms.TextInput(attrs={'class': 'form-control'}),
            'user_email': forms.TextInput(attrs={'class': 'form-control'}),
                    }


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['phonenumber_city', 'phonenumber_mobile', 'phonenumber_other']
        # exclude = []

        widgets = {
            'phonenumber_city': forms.TextInput(attrs={'class': 'form-control'}),
            'phonenumber_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'phonenumber_other': forms.TextInput(attrs={'class': 'form-control'}),
                    }

#
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['user_name', 'user_surname', 'user_email']
#         model = PhoneNumber
#         fields = ['phonenumber_city', 'phonenumber_mobile', 'phonenumber_email']
#
#         widgets = {
#             'user_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'user_surname': forms.TextInput(attrs={'class': 'form-control'}),
#             'user_email': forms.TextInput(attrs={'class': 'form-control'}),
#             'phonenumber_city': forms.TextInput(attrs={'class': 'form-control'}),
#             'phonenumber_mobile': forms.TextInput(attrs={'class': 'form-control'}),
#             'phonenumber_other': forms.TextInput(attrs={'class': 'form-control'}),
#                     }
