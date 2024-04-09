from django.shortcuts import render, redirect

from callboard.models import User
from django.views.generic import UpdateView, TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# ------подтверждение авторизации ---------


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, template_name='callboard/invalid_code.html')
        return redirect('account_login')


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'callboard/profile.html'  # возвращаемся после авторизации


# class UserList(ListView):
#     model = User
#     queryset = User.objects.all()
