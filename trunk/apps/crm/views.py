# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, resolve
from django.http import  Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext

from crm.models import Party, Company, Person, Interaction, Note, Task
from crm.forms import NoteForm, TaskForm, PersonForm, CompanyForm

@login_required
def main_page(request):    
    variables = RequestContext(request)
    return render_to_response('main_page.html', variables)

#def main_page

def parties_page(request):
    parties = Party.objects.all()
    variables = RequestContext(request,
                               {'parties':parties})
    return render_to_response('crm/parties_page.html', variables)

#def parties_page

def party_page(request, party_id):
    party = get_object_or_404(Party, id=party_id)
    
    if party.party_type == 'company':
        parties = [p.id for p in party.company.person_set.all()]
        parties.append(party.id)
        # Используем select_related() чтобы сократить количество запросов к базе
        # http://docs.djangoproject.com/en/dev/ref/models/querysets/#id4
        #interactions = Interaction.objects.select_related().filter(party__in=parties)
        tasks = Task.objects.select_related().filter(party__in=parties)
        notes = Note.objects.select_related().filter(party__in=parties)
    
    elif party.party_type == 'person':
        #interactions = Interaction.objects.select_related().filter(party=party)
        tasks = Task.objects.select_related().filter(party=party)
        notes = Note.objects.select_related().filter(party=party)
    
    variables = RequestContext(request,
                               {'party':party,
                                'tasks':tasks,
                                'notes':notes}
                               )
    return render_to_response('crm/party_page.html', variables)

#def party_page 

@login_required
def add_party(request, form_class, party_type):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            if party_type == 'person':
                party = Person.objects.create(
                    fname = form.cleaned_data['fname'],
                    lname = form.cleaned_data['lname'],
                    mname = form.cleaned_data['mname'],
                    background_info = form.cleaned_data['background_info']
                )
            elif party_type == 'company':
                party = Company.objects.create(
                    name = form.cleaned_data['name'],
                    background_info = form.cleaned_data['background_info']
                )
            party.save()
            return HttpResponseRedirect(reverse(parties_page))
            
    else:
        form = form_class()
    
    variables = RequestContext(request, {'form':form, 'party_type':party_type, 'add':True})
    return render_to_response ('crm/edit_party.html', variables)

#def add_party

@login_required
def edit_party(request, party_id):
    #Получаем объект
    party = get_object_or_404(Party, id=party_id)
    party = getattr(party, "%s" % party.party_type)
    
    if request.method == 'POST':
        
        #В зависимости от типа выбираем соответствующую форму
        if party.party_type == 'person':
            form = PersonForm(request.POST)
        elif party.party_type == 'company':
            form = CompanyForm(request.POST)
        
        if form.is_valid():
            if party.party_type == 'person':
                party.lname = form.cleaned_data['lname']
                party.fname = form.cleaned_data['fname']
                party.mname = form.cleaned_data['mname']
                party.background_info = form.cleaned_data['background_info']
                
            elif party.party_type == 'company':
                party.name = form.cleaned_data['name']
                party.background_info = form.cleaned_data['background_info']
            
            party.save()
            
            return HttpResponseRedirect(reverse(party_page, kwargs={'party_id':party.id}))
        
    else:
        if party.party_type == 'person':
            form = PersonForm({
                'lname':party.lname,
                'fname':party.fname,
                'mname':party.mname,
                'background_info':party.background_info,
                'company':party.company
            })
        elif party.party_type == 'company':
            form = CompanyForm({
                'name':party.name,
                'background_info':party.background_info
            })
    
    variables = RequestContext(request, {'form':form, 'party_type':party.party_type, 'party':party})
    return render_to_response ('crm/edit_party.html', variables)

#def edit_party

@login_required
def delete_party(request, party_id):
    #TODO реализовать удаление только пользователем имееющим доступ
    party = Party.objects.get(id=party_id)
    party.delete()
    return HttpResponseRedirect(reverse(parties_page))

#def delete_party

@login_required
def add_interaction(request, party_id, form_class, int_type):
    party = get_object_or_404(Party, id=party_id)
    if request.method == 'POST':
        form = form_class(request.POST, party)
        if form.is_valid():            
            if int_type == 'task':
                #TODO постараться вынести логику сохранения данных в форму
                interaction = Task.objects.create(
                                party = party,
                                created_by = request.user,
                                interaction_date = form.cleaned_data['interaction_date'],
                                title = form.cleaned_data['title'],
                                note_text = form.cleaned_data['note_text'])
                
            elif int_type == 'note':
                interaction = Note.objects.create(
                                party = party,
                                created_by = request.user,
                                interaction_date = form.cleaned_data['interaction_date'],
                                note_text = form.cleaned_data['note_text']
                                )            
            return HttpResponseRedirect(reverse('crm.views.party_page',
                                             kwargs={'party_id':int(party_id)}))
    else:
        form = form_class()
    
    variables = RequestContext(request,
                               {'form':form,
                                'party':party,
                                'int_type':int_type })
    
    #TODO реализовать поддержку ajax
    return render_to_response('crm/edit_interaction.html', variables)
    
#def add_interaction

@login_required
def edit_interaction(request, int_id, form_class):
    #TODO реализовать редактирование только пользователем имеющим доступ        
    i = get_object_or_404(Interaction, id=int_id)    
    #Получаем доступ к объекту-потомку Interaction, это или Note или Task
    # i.note, i.task
    i = getattr(i, "%s" % i.interaction_type)
    
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            if i.interaction_type == 'task':
                i.title = form.cleaned_data['title']
                i.note_text = form.cleaned_data['note_text']
                i.interaction_date = form.cleaned_data['interaction_date']
            elif i.interaction_type == 'note':
                i.note_text = form.cleaned_data['note_text']
                i.interaction_date = form.cleaned_data['interaction_date']
            i.save()
            return HttpResponseRedirect(reverse('crm.views.party_page',
                                             kwargs={'party_id':i.party.id}))        
    else:
        if i.interaction_type == 'task':
            form = form_class({
                'title':i.title,
                'note_text':i.note_text,
                'interaction_date':i.interaction_date
            })
        elif i.interaction_type == 'note':
            form = form_class({
                'note_text': i.note_text,
                'interaction_date': i.interaction_date                
            })
        
    variables = RequestContext(request,
          {'form':form, 'party':i.party, 'interaction':i,'int_type':i.interaction_type})
    
    return render_to_response('crm/edit_interaction.html', variables)


#def edit_interaction

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = 2
    task.save()
    
    return HttpResponseRedirect(reverse(party_page, kwargs={'party_id':task.party.id }))

#def complite_task

@login_required
def delete_interaction(request, int_id):
    #TODO реализовать удаление только пользователем имееющим доступ
    i = Interaction.objects.get(id=int_id)
    i.delete()    
    return HttpResponseRedirect(reverse('crm.views.party_page',
                                 kwargs={'party_id':i.party.id}))

#def delete_interaction