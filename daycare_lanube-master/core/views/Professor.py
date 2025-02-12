from django.db.models.query import QuerySet
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView, FormView
from core.models.Professor import Professor
from core.forms import ProfessorForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from core.models.User import UserApp
from django.contrib.auth.models import User, Group
from django.template import loader

class ProfessorCreateView(LoginRequiredMixin, CreateView):
    model = Professor
    form_class = ProfessorForm
    template_name = "core/professor_form.html"

    def get_success_url(self):
        return reverse("core:professor-list")

    def form_invalid(self, form):
        print('ERROR',form.errors)
        return super(ProfessorCreateView, self).form_invalid(form)

    def form_valid(self, form):
        user = User()
        first_name = self.request.POST['first_name']
        last_name_array = self.request.POST['last_name'].split(' ')
        last_name = ''
        for item in last_name_array:
            last_name += item
        username = f"{first_name[:2].lower()}{last_name.lower()}"
        user.username = username
        user.first_name = first_name
        user.last_name = self.request.POST['last_name']
        user.set_password(username)
        user.save()
        user.groups.add(Group.objects.get(name="Profesor"))
        form.instance.user = user
        form.instance.created_by = self.request.user
        return super(ProfessorCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfessorCreateView, self).get_context_data(**kwargs)
        context["title_page"] = "Educadoras"
        return context

class ProfessorListView(LoginRequiredMixin, ListView):
    model = Professor
    template_name = 'core/professor_list.html'

    def get_queryset(self):
        return Professor.objects.filter(active=True).exclude(user__is_staff = True)

    def get_context_data(self, **kwargs):
        context = super(ProfessorListView, self).get_context_data(**kwargs)
        context["title_page"] = "Educadoras"
        return context

class ProfessorEditView(LoginRequiredMixin, UpdateView):
    model = Professor
    form_class = ProfessorForm
    template_name = 'core/professor_form.html'
    success_url = reverse_lazy('core:professor-list')

    def form_invalid(self, form):
        print('ERRORS',form.errors)
        return super(ProfessorEditView, self).form_invalid(form)
    
    def form_valid(self, form):
        user = self.object.user
        user.first_name = self.request.POST["first_name"]
        user.last_name = self.request.POST["last_name"]
        user.save()
        form.instance.created_by = self.request.user
        return super(ProfessorEditView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfessorEditView, self).get_context_data(**kwargs)
        context["title_page"] = "Educadoras"        
        context["first_name"] = self.object.user.first_name        
        context["last_name"] = self.object.user.last_name
        return context

class ProfessorDeleteView(LoginRequiredMixin, DeleteView):
    model = Professor
    success_url = reverse_lazy('core:professor-list')

    def get_context_data(self, **kwargs):
        context = super(ProfessorDeleteView, self).get_context_data(**kwargs)
        context["title_page"] = "Educadoras"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        p = Professor.objects.get(pk=int(kwargs['pk']))
        p.active = False
        p.save()
        success_url = self.get_success_url()
        messages.add_message(request, messages.SUCCESS, "El profesor ha sido eliminado.")
        return HttpResponseRedirect(success_url)
    
class ProfessorDetailView(LoginRequiredMixin, DetailView):
    model = Professor
    template_name = 'core/professor_details.html' 

    def get_context_data(self, **kwargs):
        context = super(ProfessorDetailView, self).get_context_data(**kwargs)
        context["title_page"] = "Mi Perfil"
        return context 
    
def profile_professor(request, pk):
    professor = Professor.objects.get(user_id = pk)
    context = {}
    context["title_page"] = "Mi Perfil"
    context["object"] = professor
    template = loader.get_template('core/professor_details.html')
    return HttpResponse(template.render(context, request))

class ProfessorListHistoryView(LoginRequiredMixin, ListView):
    model = Professor
    template_name = 'core/professor_history.html'

    def get_queryset(self):
        return Professor.objects.filter(active=False).exclude(user__is_staff = True)

    def get_context_data(self, **kwargs):
        context = super(ProfessorListHistoryView, self).get_context_data(**kwargs)
        context["title_page"] = "Educadoras Histórico"
        return context