from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignupForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "w-full border rounded-lg p-2 bg-white dark:bg-gray-700 dark:text-white"
        })
    )

    class Meta:
        model = User
        fields = ["username","email","password1","password2"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields["username"].widget.attrs.update({
            "class":"w-full border rounded-lg p-2 bg-white dark:bg-gray-700 dark:text-white"
        })

        self.fields["password1"].widget.attrs.update({
            "class":"w-full border rounded-lg p-2 bg-white dark:bg-gray-700 dark:text-white"
        })
        self.fields["password2"].label = "Confirm Password"
        self.fields["password2"].widget.attrs.update({
            "class":"w-full border rounded-lg p-2 bg-white dark:bg-gray-700 dark:text-white"
        })

class PasswordResetFormStyled(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            "class": "w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
        })