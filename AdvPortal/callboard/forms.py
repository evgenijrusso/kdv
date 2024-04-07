from datetime import datetime

from allauth.account.forms import SignupForm
from string import hexdigits
import random
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import Advert, Response, CATEGORY


class CommonSignupForm(SignupForm):

    def save(self, request):
        # Ensure you call the parent class's save. Save() returns a User object.
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=_('Activation code'),           # Код активации
            message=_('Account activation code'),    # Код активации аккаунта
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return user


class AdvertForm(forms.ModelForm):

    # created = forms.DateTimeField(initial=datetime.utcnow(), label=(_('Created data')))
    category = forms.CharField(
        max_length=20, empty_value='Категория не выбрана',
        widget=forms.Select(choices=CATEGORY)
    )

    def __init__(self, *args, **kwargs):
        super(AdvertForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Advert
        fields = ['user', 'title', 'category', 'content']
        label = [_('User'), _('Title'), _('Category'),  _('Content')]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if content == title:
            raise ValidationError(
                'Текст не должен совпадать с заголовком.'
            )

        return cleaned_data


class ResponseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Response
        fields = ['advert', 'user', 'text']
        label = [_('Advert'), _('User'), _('Text'), ]
        widgets = {
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 1, 'required': True}),
        }
