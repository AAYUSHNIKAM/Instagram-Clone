from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, authenticate

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # Change field name to "Email"

    def clean(self):
        email = self.cleaned_data.get("username")  # Get email instead of username
        password = self.cleaned_data.get("password")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            self.user_cache = authenticate(username=user.username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password.")
        else:
            raise forms.ValidationError("User with this email does not exist.")

        return self.cleaned_data