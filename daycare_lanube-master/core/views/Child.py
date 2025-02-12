from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView, FormView, TemplateView
from core.models.Child import Child
from core.models.Family import Family
from core.models.Parent import Parent
from core.models.ClassGroup import ClassGroup
from core.models.ReportChild import ReportChild
from core.models.User import UserApp
from core.forms import ChildForm, RelationshipForm, ApprovedForm, ParentForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

class ChildStepOneCreateView(LoginRequiredMixin, CreateView):
    model = Child
    form_class = ChildForm
    template_name = "core/child_form_one.html"

    def get_success_url(self):
        pk = self.object.pk
        return reverse("core:child-add-two", kwargs={'pk': pk})

    def form_invalid(self, form):
        print('ERROR',form.errors)
        return super(ChildStepOneCreateView, self).form_invalid(form)

    def form_valid(self, form):
        if Child.objects.filter(nip = form.instance.nip, active = False).exists():
            messages.add_message(self.request, messages.SUCCESS, "Este niño se encuentra en el histórico. Debe eliminarlo definitivamente y agregarlo nuevamente.")
            return super(ChildStepOneCreateView, self).form_invalid(form)
        
        if Child.objects.filter(nip = form.instance.nip, active = True).exists():
            messages.add_message(self.request, messages.SUCCESS, "Ya existe un niño con este NIP.")
            return super(ChildStepOneCreateView, self).form_invalid(form)
        
        last_exp = Child.objects.all().order_by('-id').first()
        if last_exp is not None:
            exp = last_exp.exp + 1
        else:
            exp = 1
        form.instance.exp = exp
        form.instance.created_by = self.request.user
        return super(ChildStepOneCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChildStepOneCreateView, self).get_context_data(**kwargs)
        context["title_page"] = "Niños"
        return context
    
class ChildStepTwoCreateView(LoginRequiredMixin, CreateView):
    model = Parent
    form_class = ParentForm
    template_name = "core/child_form_two.html"

    def get_success_url(self):
        return reverse("core:child-add-three")

    def form_invalid(self, form):
        print('ERROR',form.errors)
        return super(ChildStepTwoCreateView, self).form_invalid(form)

    def form_valid(self, form):
        form.instance.is_mother = True
        form.instance.created_by = self.request.user
        
        if not Parent.objects.filter(nip = form.instance.nip, mother = False).exists():
            obj = super(ChildStepTwoCreateView, self).form_valid(form)
            id_parent = form.instance.id
        else:
            parent = Parent.objects.get(nip = form.instance.nip, mother = False)
            id_parent = parent.id
            parent.first_name = form.instance.first_name
            parent.last_name = form.instance.last_name
            parent.date_birth = form.instance.date_birth
            parent.address = form.instance.address
            parent.phone = form.instance.phone
            parent.school_level = form.instance.school_level
            parent.work_center = form.instance.work_center
            parent.position = form.instance.position
            parent.illnesses = form.instance.illnesses
            parent.alcoholism = form.instance.alcoholism
            parent.smoking = form.instance.smoking
            parent.is_mother = True
            parent.save()
        child = Child.objects.get(id = self.request.POST['child'])
        child.mother_id = id_parent
        child.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super(ChildStepTwoCreateView, self).get_context_data(**kwargs)
        context["title_page"] = "Niños"
        context["pk"] = self.kwargs.get('pk')
        context["parent"] = Parent.objects.get(user_id = self.request.user.id, mother = True) if Parent.objects.filter(user_id = self.request.user.id, mother = True).exists() else None
        return context
    
class ChildStepThreeCreateView(LoginRequiredMixin, CreateView):
    model = Parent
    form_class = ParentForm
    template_name = "core/child_form_three.html"

    def get_success_url(self):
        return reverse("core:child-add-four")

    def form_invalid(self, form):
        print('ERROR',form.errors)
        return super(ChildStepThreeCreateView, self).form_invalid(form)

    def form_valid(self, form):
        form.instance.is_mother = False
        form.instance.created_by = self.request.user
        
        if not Parent.objects.filter(nip = form.instance.nip, mother = False).exists():
            obj = super(ChildStepThreeCreateView, self).form_valid(form)
            id_parent = form.instance.id
        else:
            parent = Parent.objects.get(nip = form.instance.nip, mother = False)
            id_parent = parent.id
            parent.first_name = form.instance.first_name
            parent.last_name = form.instance.last_name
            parent.date_birth = form.instance.date_birth
            parent.address = form.instance.address
            parent.phone = form.instance.phone
            parent.school_level = form.instance.school_level
            parent.work_center = form.instance.work_center
            parent.position = form.instance.position
            parent.illnesses = form.instance.illnesses
            parent.alcoholism = form.instance.alcoholism
            parent.smoking = form.instance.smoking
            parent.is_mother = False
            parent.save()
        child = Child.objects.get(id = self.request.POST['child'])
        child.father_id = id_parent
        child.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super(ChildStepThreeCreateView, self).get_context_data(**kwargs)
        context["title_page"] = "Niños"
        context["pk"] = self.kwargs.get('pk')
        context["parent"] = Parent.objects.get(user_id = self.request.user.id, mother = False) if Parent.objects.filter(user_id = self.request.user.id, mother = False).exists() else None
        return context
    
class ChildStepFourCreateView(LoginRequiredMixin, CreateView):
    model = Child
    form_class = RelationshipForm
    template_name = "core/child_form_four.html"

    def get_success_url(self, *args, **kwargs):
        return reverse("core:child-add-five")

    def form_invalid(self, form):
        print('ERROR',form.errors)
        return super(ChildStepFourCreateView, self).form_invalid(form)

    def form_valid(self, form, *args, **kwargs):
        if form.instance.first_name == '' and form.instance.last_name == '' and form.instance.age is None:
            return HttpResponseRedirect(reverse('core:child-add-five'))
        form.instance.created_by = self.request.user
        form.instance.child_id = self.request.POST["child"]
        form.instance.type = "Relationship"
        form.instance.status = None
        return super(ChildStepFourCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChildStepFourCreateView, self).get_context_data(**kwargs)
        context["title_page"] = "Niños"
        context["pk"] = self.kwargs.get('pk')
        return context
    
class ChildStepFiveCreateView(LoginRequiredMixin, CreateView):
    model = Family
    form_class = ApprovedForm
    template_name = "core/child_form_five.html"

    def get_success_url(self):
        return reverse("core:child-list")

    def form_invalid(self, form):
        print('ERROR',form.errors)
        return super(ChildStepFiveCreateView, self).form_invalid(form)

    def form_valid(self, form, *args, **kwargs): 
        if form.instance.first_name == '' and form.instance.last_name == '' and form.instance.ic is None:
            return HttpResponseRedirect(reverse('core:child-list'))      
        form.instance.created_by = self.request.user
        form.instance.child_id = self.request.POST["child"]
        form.instance.type = "Approved"
        form.instance.status = "Aprobado"
        return super(ChildStepFiveCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChildStepFiveCreateView, self).get_context_data(**kwargs)
        context["title_page"] = "Niños"
        context["pk"] = self.kwargs.get('pk')
        return context
    

@csrf_exempt
@require_http_methods(['POST'])
def save_relationship(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    age = request.POST.get('age')
    relationship = request.POST.get('relationship')
    child = request.POST.get('child')

    # save the relationship to the database
    # assuming you have a model called Relationship
    relationship_obj = Family.objects.create(
        type="Relationship",        
        relationship=relationship,
        first_name=first_name,
        last_name=last_name,
        age=age,
        child_id = child
    )
    return JsonResponse({'message': 'Relationship saved successfully'})

@csrf_exempt
@require_http_methods(['POST'])
def save_approved(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    ic = request.POST.get('ic')
    relationship = request.POST.get('relationship')
    child = request.POST.get('child')

    # save the relationship to the database
    # assuming you have a model called Relationship
    relationship_obj = Family.objects.create(
        type="Approved",        
        status="Aprobado",
        relationship=relationship,
        first_name=first_name,
        last_name=last_name,
        ic=ic, 
        child_id = child
    )
    return JsonResponse({'message': 'Approved saved successfully'})
    
class ChildDetailView(LoginRequiredMixin, DetailView):
    model = Child
    template_name = 'core/child_details.html'

    def get_context_data(self, **kwargs):
        context = super(ChildDetailView, self).get_context_data(**kwargs)
        context["title_page"] = "Perfil Infantil"
        context["mother"] = Child.objects.get(id = self.object.id).mother
        context["classgroup"] = ClassGroup.objects.filter(childs = self.object)
        context["father"] = Child.objects.get(id = self.object.id).father
        context["family_approved"] = Family.objects.filter(child = self.object.id, type="Approved")
        context["familys"] = Family.objects.filter(child = self.object.id)
        context["last_report"] = ReportChild.objects.filter(child = self.object.id).order_by('-date').first()
        return context 

class ChildListView(LoginRequiredMixin, ListView):
    model = Child
    template_name = 'core/child_list.html'
    paginate_by = 12

    def get_queryset(self):
        if self.request.user.groups.filter(name = "Progenitor").exists():
            parent = Parent.objects.get(user_id = self.request.user.id)
            if parent.is_mother:
                return Child.objects.filter(active=True,mother = parent)
            else:
                return Child.objects.filter(active=True,father = parent)
        else:
            return Child.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(ChildListView, self).get_context_data(**kwargs)
        context["title_page"] = "Niños"
        return context

class ChildEditView(LoginRequiredMixin, UpdateView):
    model = Child
    form_class = ChildForm
    template_name = "core/child_form_edit.html"

    def get_success_url(self):
        return reverse("core:child-list")

    def form_invalid(self, form):
        print('ERROR',form.errors)
        return super(ChildEditView, self).form_invalid(form)

    def form_valid(self, form):
        # form.instance.father_id = self.request.POST['father']        
        # form.instance.mother_id = self.request.POST['mother']
        form.instance.created_by = self.request.user
        return super(ChildEditView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChildEditView, self).get_context_data(**kwargs)
        context["title_page"] = "Niños"
        # context["fathers"] = Parent.objects.filter(active = True, is_mother = False)
        # context["mothers"] = Parent.objects.filter(active = True, is_mother = True)
        return context
    
class ChildDeleteView(LoginRequiredMixin, DeleteView):
    model = Child

    def get_context_data(self, **kwargs):
        context = super(ChildDeleteView, self).get_context_data(**kwargs)
        context["title_page"] = "Niños"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        p = Child.objects.get(pk=int(kwargs['pk']))
        if p.active:             
            p.active = False
            p.date_down = datetime.now()
            p.save() 
            # Delete families
            families = Family.objects.filter(child = p)
            for family in families:
                family.delete()
            # Delete parents
            if p.father:
                if not Child.objects.filter(father = p.father, active = True).exists():
                    p.father.active = False
                    p.father.save()
            if p.mother:
                if not Child.objects.filter(mother = p.mother, active = True).exists():
                    p.mother.active = False
                    p.mother.save()  
            success_url = reverse_lazy('core:child-list')              
            messages.add_message(request, messages.SUCCESS, "Se ha desmatriculado de manera satisfactoria.")
        else:
            if p.father:
                if not Child.objects.filter(father = p.father, active = True).exists():
                    p.father.delete()
            if p.mother:
                if not Child.objects.filter(mother = p.mother, active = True).exists():
                    p.mother.delete()  
            p.delete()            
            success_url = reverse_lazy('core:child-history')   
            messages.add_message(request, messages.SUCCESS, "Se ha eliminado de manera satisfactoria.")
        return HttpResponseRedirect(success_url)
    
class ChildListHistoryView(LoginRequiredMixin, ListView):
    model = Child
    template_name = 'core/child_history.html'
    paginate_by = 12

    def get_queryset(self):
        return Child.objects.filter(active=False)

    def get_context_data(self, **kwargs):
        context = super(ChildListHistoryView, self).get_context_data(**kwargs)
        context["title_page"] = "Niños Históricos"
        return context