from django import forms
from .models import User

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username)
        if not user.exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не существует')
        if user.first():
            if not user.first().check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password')


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField()
    address = forms.CharField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердить пароль'
        self.fields['email'].label = 'Электронная почта'

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        user_email = User.objects.filter(email=email).exists()
        if user_email:
            raise forms.ValidationError('Этот электронный адрес почты уже существует')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        username_check = User.objects.filter(username=username).exists()
        if username_check:
            raise forms.ValidationError('Имя пользователя уже существует')
        return username

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email')


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Оставьте комментарий')
