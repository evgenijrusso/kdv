from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.shortcuts import redirect

from .models import Response, Advert
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

""" post_save запускает действие всякий раз, когда 
    пользователь сохраняет какой-либо объект в базе данных
  -- if created:   проверяет, создана модель или нет ----  
  --  create_advert: реагирует на создание нового объявления -- 
"""


# @receiver(post_save, sender=Advert)
# def create_advert(sender, instance, created, **kwargs):
#     if created:
#         print(f'New instance created: {instance.title} {instance.created.strftime("%Y-%M-%d")}')
#     else:
#         print(f' Instance updated: {instance.title} {instance.created.strftime("%Y-%M-%d")}')


@receiver(post_save, sender=Advert)
def update_advert(sender, instance, created, **kwargs):
    print(f'New instance created: {instance}')
    # if not created:
    #     print(f'New instance created: {instance.title}')
    # post_save.connect(update_advert, sender=Advert)


@receiver(post_save, sender=Response)
def send_message(instance, created, **kwargs):

    html_content = render_to_string('callboard/email_message.html', {'instance': instance, })

    msg = EmailMultiAlternatives(
        subject=f'Отклик на пост - {instance.text}',
        from_email=settings.DEFAULT_FROM_EMAIL,  # instance.user.email,
        to=(instance.advert.user.email,)
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


"""  проверка в shell_plus  
send_mail(Response, "Test messsage", settings.EMAIL_HOST_USER, ("tar800-upgrade@yandex.ru",)) 
"""
