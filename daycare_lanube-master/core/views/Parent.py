from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView, FormView
from core.models.Parent import Parent
from core.models.Child import Child
from core.forms import ParentForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.contrib.auth.models import User, Group

class ParentCreateView(LoginRequiredMixin, CreateView):
    model = Parent
    form_class = ParentForm
    template_name = "core/parent_form.html"

    def get_success_url(self):
        return reverse("core:parent-list")

    def form_invalid(self, form):
        print('ERROR',form.errors)
        return super(ParentCreateView, self).form_invalid(form)

    def form_valid(self, form):
        child = Child.objects.get(id = self.request.POST['child'])
        if "mother" in self.request.POST:   
            form.instance.is_mother = 1
        else:
            form.instance.is_mother = 0
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
        user.groups.add(Group.objects.get(name="Progenitor"))
        form.instance.user = user
        form.instance.created_by = self.request.user        
        form.instance.save()
        if "mother" in self.request.POST:
            child.mother = form.instance
            child.save()
        else:
            child.father = form.instance
            child.save()
        return super(ParentCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ParentCreateView, self).get_context_data(**kwargs)
        context["title_page"] = "Padres"
        context["childs"] = Child.objects.filter(active=True)
        return context

class ParentListView(LoginRequiredMixin, ListView):
    model = Parent
    template_name = 'core/parent_list.html'

    def get_queryset(self):
        return Parent.objects.filter(active = True)

    def get_context_data(self, **kwargs):
        context = super(ParentListView, self).get_context_data(**kwargs)
        context["title_page"] = "Padres"
        return context

class ParentEditView(LoginRequiredMixin, UpdateView):
    model = Parent
    form_class = ParentForm
    template_name = 'core/parent_form.html'
    success_url = reverse_lazy('core:parent-list')

    def form_invalid(self, form):
        print('ERRORS',form.errors)
        return super(ParentEditView, self).form_invalid(form)
    
    def form_valid(self, form):        
        child = Child.objects.get(id = self.request.POST['child'])
        if "mother" in self.request.POST:   
            form.instance.is_mother = 1
        else:
            form.instance.is_mother = 0
        user = self.object.user
        if user:
            user.first_name = self.request.POST["first_name"]
            user.last_name = self.request.POST["last_name"]
            user.save()        
        if "mother" in self.request.POST:
            child.mother = form.instance
            child.save()
        else:
            child.father = form.instance
            child.save()
        form.instance.created_by = self.request.user
        return super(ParentEditView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ParentEditView, self).get_context_data(**kwargs)
        context["title_page"] = "Padres"        
        context["first_name"] = self.object.first_name        
        context["last_name"] = self.object.last_name
        if Child.objects.filter(father = self.kwargs['pk']).exists():
            context["childs"] = Child.objects.filter(father = self.kwargs['pk'], active=True)               
            context["child"] = Child.objects.filter(father = self.kwargs['pk'], active=True)  
        if Child.objects.filter(mother = self.kwargs['pk']).exists():
            context["childs"] = Child.objects.filter(mother = self.kwargs['pk'], active=True)              
            context["child"] = Child.objects.filter(mother = self.kwargs['pk'], active=True)  
        if not Child.objects.filter(father = self.kwargs['pk']).exists() and not Child.objects.filter(mother = self.kwargs['pk']).exists():            
            context["childs"] = Child.objects.filter(active=True) 
        return context

class ParentDeleteView(LoginRequiredMixin, DeleteView):
    model = Parent
        
    def get_context_data(self, **kwargs):
        context = super(ParentDeleteView, self).get_context_data(**kwargs)
        context["title_page"] = "Padres"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        p = Parent.objects.get(pk=int(kwargs['pk']))
        if p.active:
            p.active = False
            p.save()
            success_url = reverse_lazy('core:parent-list')
            messages.add_message(request, messages.SUCCESS, "El padre ha sido eliminado.")
        else:
            p.delete()            
            success_url = reverse_lazy('core:parent-history')
            messages.add_message(request, messages.SUCCESS, "El padre ha sido eliminado definitivamente.")
        return HttpResponseRedirect(success_url)
    
class ParentDetailView(LoginRequiredMixin, DetailView):
    model = Parent
    template_name = 'core/parent_details.html'    

    def get_context_data(self, **kwargs):
        context = super(ParentDetailView, self).get_context_data(**kwargs)
        context["title_page"] = "Mi Perfil"
        return context 
    
class ParentDetailUserView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'core/parent_details.html'    

    def get_context_data(self, **kwargs):
        context = super(ParentDetailUserView, self).get_context_data(**kwargs)
        context["title_page"] = "Mi Perfil"
        return context 
    
def profile_parent(request, pk):
    parent = Parent.objects.get(user_id = pk)
    context = {}
    context["title_page"] = "Mi Perfil"
    context["object"] = parent
    template = loader.get_template('core/parent_details.html')
    return HttpResponse(template.render(context, request))

class ParentListHistoryView(LoginRequiredMixin, ListView):
    model = Parent
    template_name = 'core/parent_history.html'

    def get_queryset(self):
        return Parent.objects.filter(active = False)

    def get_context_data(self, **kwargs):
        context = super(ParentListHistoryView, self).get_context_data(**kwargs)
        context["title_page"] = "Padres Históricos"
        return context
    