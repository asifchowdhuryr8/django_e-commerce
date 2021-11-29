from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Type password again'}))
    # You can add extra fields to the form like this. Confirm password is not in the model that's why I added it here.

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            # This is to add the class to all the fields in the form.
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        """Checking if the password and confirm password are the same"""
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match the confirm password")
