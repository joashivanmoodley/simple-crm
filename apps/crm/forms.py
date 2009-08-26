# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
import datetime

from crm.models import Interaction, Company, Person, Note, Task

class CompanyForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    background_info = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'5'}))
    
#class CompanyForm

class PersonForm(forms.Form):
    lname = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    fname = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    mname = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':'50'}))    
    background_info = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'5'}))

#class PersonForm

class InteractionForm(forms.Form):
    class Media:
        css = { 'all': ('css/ui.datepicker.css',) }
        js = ('js/ui.datepicker.js',)

#class AddInteractionForm

class NoteForm(InteractionForm):
    note_text = forms.CharField(widget=forms.Textarea(attrs={'rows':'5'}))
    interaction_date = forms.DateField(initial=datetime.date.today())

#class AddNoteForm

class TaskForm(InteractionForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    note_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'5'}))
    interaction_date = forms.DateField()
    
#class AddTaskForm