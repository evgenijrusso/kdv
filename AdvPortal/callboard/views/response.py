from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ..models import Response, Advert
from ..forms import ResponseForm


class ResponseList(ListView):
    model = Response
    template_name = 'callboard/responses.html'
    context_object_name = 'responses'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of responses'
        return context


class ResponseDetail(DetailView):
    model = Response
    template_name = 'callboard/response_detail.html'
    context_object_name = 'response'


class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    context_object_name = 'response'
    template_name = 'callboard/response_create.html'
    success_url = '/callboard/responses/'

    def form_valid(self, form):
        response = form.save(commit=False)
        if response.user == response.advert.user:
            messages.warning(self.request, "You can't send a response to yourself")
            return HttpResponseRedirect('/callboard/responses/create')
        else:
            response.save()
            response.status_on()
            messages.success(self.request, "The response was created successfully, the status was changed")
            return super(ResponseCreate, self).form_valid(form)


class ResponseUpdate(UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = 'callboard/response_update.html'

    def get_object(self, **kwargs):
        idu = self.kwargs.get('pk')
        return Response.objects.get(pk=idu)

    def form_valid(self, form):
        messages.success(self.request, "The response was updated successfully.")
        return super(ResponseUpdate, self).form_valid(form)


class ResponseDelete(DeleteView):  # PermissionRequiredMixin, LoginRequiredMixin,
    permission_required = 'callboard.advert_delete'
    permission_denied_message = "Permission Denied"
    model = Response
    template_name = 'callboard/response_delete.html'
    success_url = '/callboard/responses/'

    # def form_valid(self, form):
    #     if self.request.user == self.object.user or self.request.user == self.object.advert.user:
    #         success_url = '/callboard/responses/'
    #         self.object.delete()
    #         return HttpResponseRedirect(success_url)
    #     else:
    #         return self.handle_no_permission()


