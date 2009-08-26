# -*- encoding: utf-8 -*-
import os.path
from django.conf.urls.defaults import *
from django.conf import settings
from crm.forms import NoteForm, TaskForm, CompanyForm, PersonForm
from crm.views import *

from django.contrib import admin
admin.autodiscover()

site_media = os.path.join(settings.PROJECT_PATH, 'site-media')

urlpatterns = patterns('',
    
    url(r'^$', main_page, name='main_page'),                       

    url(r'^parties/$', parties_page, name='parties'),
    url(r'^parties/(?P<party_id>\d+)/$', party_page, name='party'),
    
    url(r'^parties/add-company/$', add_party, {'form_class':CompanyForm, 'party_type':'company'}, name='add_company'),
    url(r'^parties/add-person/$', add_party,  {'form_class':PersonForm, 'party_type':'person'}, name='add_person'),
    url(r'^parties/(?P<party_id>\d+)/edit/$', edit_party, name='edit_party'),
    url(r'^parties/(?P<party_id>\d+)/delete/$', delete_party, name='delete_party'),
    
    url(r'^parties/(?P<party_id>\d+)/note/add/$', add_interaction, {'form_class':NoteForm, 'int_type':'note'}, name='add_note',),
    url(r'^parties/(?P<party_id>\d+)/task/add/$', add_interaction, {'form_class':TaskForm, 'int_type':'task'}, name='add_task'),    
    url(r'^note/(?P<int_id>\d+)/edit/$', edit_interaction, {'form_class':NoteForm}, name='edit_note'),
    url(r'^task/(?P<int_id>\d+)/edit/$', edit_interaction, {'form_class':TaskForm}, name='edit_task'),    
    url(r'^note/(?P<int_id>\d+)/delete/$', delete_interaction, name='delete_note'),
    url(r'^task/(?P<int_id>\d+)/delete/$', delete_interaction, name='delete_task'),
    url(r'^task/(?P<task_id>\d+)/complete/$', complete_task, name='complete_task'),
    
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site-media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': site_media }),
    )
