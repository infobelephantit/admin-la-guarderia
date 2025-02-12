from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from core.models.Child import Child
from core.models.Family import Family
from core.models.Parent import Parent
from core.models.Professor import Professor
from core.models.Event import Event
from core.models.Bill import Bill
from core.models.Alert import Alert
from core.models.ReportChild import ReportChild
from core.models.ClassGroup import ClassGroup
from core.models.Activity import Activity
from core.models.User import UserApp
from core.models.Gallery import Gallery
from core.models.AssistanceDaily import AssistanceDaily
from django.core.exceptions import NON_FIELD_ERRORS

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control mayusculas'
            field.widget.attrs['autocomplete'] = 'off'

class ChildForm(forms.ModelForm):
    health_requirements = forms.CharField(required=False)
    food_requirements = forms.CharField(required=False)
    periodic_medications = forms.CharField(required=False)
    observations = forms.CharField(required=False)
    class Meta:
        model = Child
        exclude = ('exp','active','mother','father','date_down')
        error_messages = {
            NON_FIELD_ERRORS: {
                'primary_key': "El campo %(field_labels)s no se puede repetir.",
            }
        }


class FamilyForm(forms.ModelForm):
    age = forms.IntegerField(required=False)
    ic = forms.CharField(required=False)
    relationship = forms.CharField(required=False)
    type = forms.CharField(required=False)
    status = forms.CharField(required=False)
    class Meta:
        model = Family
        exclude = ('active',)

class RelationshipForm(forms.ModelForm):
    age = forms.IntegerField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    relationship = forms.CharField(required=False)
    class Meta:
        model = Family
        exclude = ('ic', 'type','active', 'status')

class ApprovedForm(forms.ModelForm):
    ic = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    relationship = forms.CharField(required=False)
    status = forms.CharField(required=False)
    class Meta:
        model = Family
        exclude = ('age', 'type','active')

class ParentForm(forms.ModelForm):
    illnesses = forms.CharField(required=False)
    alcoholism = forms.BooleanField(required=False)
    smoking = forms.BooleanField(required=False)
    class Meta:
        model = Parent
        exclude = ('user','active')

class ProfessorForm(forms.ModelForm):
    is_supervisor = forms.BooleanField(required=False)    
    class Meta:
        model = Professor
        exclude = ('user','active')

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserForm(UserCreationForm):
    class Meta:
        model = UserApp
        fields = ['username', 'rol', 'nip', 'mother']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserApp
        fields = ['username', 'rol', 'is_active', 'nip', 'mother']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('user',)

class ReportChildForm(forms.ModelForm):
    class Meta:
        model = ReportChild
        exclude = ('child',)

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        exclude = ('user','active')
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Los campos %(field_labels)s no se pueden repetir en una nueva factura.",
            }
        }

class ClassGroupForm(forms.ModelForm):
    class Meta:
        model = ClassGroup
        fields = ('name',)

class ClassGroupAssignForm(forms.ModelForm):
    class Meta:
        model = ClassGroup
        exclude = ('childs','name','professor','user')

class AlertForm(forms.ModelForm):
    active = forms.BooleanField(required=False)
    class Meta:
        model = Alert
        exclude = ('user','created')
        
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('name',)

class ActivityAssignForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = ('childs','name','professor','user')
        
class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('image',)
        
class AssistanceDailyForm(forms.ModelForm):
    class Meta:
        model = AssistanceDaily
        exclude = ('child','professor')