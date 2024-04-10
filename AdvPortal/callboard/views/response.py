from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ..models import Response
from ..forms import ResponseForm
from ..filter import ResponseFilter


class ResponseList(ListView):
    model = Response
    template_name = 'callboard/responses.html'
    context_object_name = 'responses'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
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
         #   response.status_on()
            messages.success(self.request, "The response was created successfully, the status was changed")
            return super(ResponseCreate, self).form_valid(form)


class ResponseUpdate(LoginRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = 'callboard/response_update.html'

    def get_object(self, **kwargs):
        idu = self.kwargs.get('pk')
        return Response.objects.get(pk=idu)

    def form_valid(self, form):
        messages.success(self.request, "The response was updated successfully.")
        return super(ResponseUpdate, self).form_valid(form)


class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'callboard/response_delete.html'
    success_url = '/callboard/responses/'


class ReplyDelete(LoginRequiredMixin, DeleteView):
    model = Response
    success_url = '/'


# ----------  Private -----------------

class PrivateView(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-response_date'
    template_name = 'callboard/private_response.html'
    context_object_name = 'responses'
    paginate_by = 3

    def get_queryset(self):
        queryset = Response.objects.filter(advert__user=self.request.user).order_by('response_date')
        self.filterset = ResponseFilter(self.request.GET, queryset=queryset,request=self.request.user)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
#        context['title'] = 'List of responses'
        context['filterset'] = self.filterset
        page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(
            page.number, on_each_side=1, on_ends=1)
        return context



@login_required
def accept_response(request, pk):   # нужно
    response = Response.objects.get(id=pk)
    # response.accepted = True
    response.status_on()
    response.save()
    messages.success(request, "The accept response was updated successfully, the status was changed")
    return redirect('response_detail', pk)    # private_response


#
# @login_required
# def subscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(user)
#     return redirect('advert_cat_list', pk)