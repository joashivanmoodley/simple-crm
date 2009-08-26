# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


COMMUNICATION_TYPE = (
    ('phone', u'телефон'),
    ('email', u'электропочта')
)

INTERACTION_TYPE = (
    ('note','заметка'),
    ('task','задача'),
)

class Party(models.Model):
    background_info = models.TextField(u'background info', null=True, blank=True)
    party_type = models.CharField(max_length='20', blank=True)
    
    def __unicode__(self):
        if self.party_type == 'company':
            return self.company.__unicode__()
        elif self.party_type == 'person':
            return self.person.__unicode__()
#class Party

class Company(Party):
    name = models.CharField(u'company name', max_length=100)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.party_type = 'company'
        super(Company, self).save()
    
#class Company

class Person(Party):
    """ Персона """
    fname = models.CharField(u'Имя', max_length=100)
    lname = models.CharField(u'Фамилия', max_length=100)
    mname = models.CharField(u'Отчество', max_length=100, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    
    def __unicode__(self):
        return "%s %s" % (self.lname, self.fname)
        
    def save(self, *args, **kwargs):
        self.party_type = 'person'
        super(Person, self).save()        

#class Person

#-------------------------------------------------------------------------------
#class Communication(models.Model):
#    """ Средства связи """
#    party = models.ForeignKey(Party)
#    type = models.CharField(max_length=20, choices=COMMUNICATION_TYPE)
#    communication = models.CharField(max_length=80)
    
#class Communication

#class Interaction(models.Model):
#    party = models.ForeignKey(Party)
#    task = models.CharField(max_length=250)
#    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE)
#    created_by = models.ForeignKey(User)
#    created_date = models.DateField(auto_now_add=True)
#    interaction_date = models.DateField()
#    note = models.TextField()
#    
#    def __unicode__(self):
#        return "%s %s %s" % (self.interaction_type, self.created_date,  self.party)
#    
#    class Meta:
#        ordering = ['-interaction_date']
##class Interaction
#-------------------------------------------------------------------------------


class Interaction(models.Model):
    party = models.ForeignKey(Party)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE)
    created_date = models.DateField(auto_now_add=True)    
    created_by = models.ForeignKey(User)
    interaction_date = models.DateField()
    
    class Meta:
        ordering = ['-interaction_date']
        
    def __unicode__(self):
        if self.interaction_type == 'note':
            return self.note.__unicode__()
        elif self.interaction_type == 'task':
            return self.task.__unicode__()

#class Interaction

class Note(Interaction):
    note_text = models.TextField()
    
    def __unicode__(self):
        return "%s %s" % (self.interaction_type, self.interaction_date)
    
    def save(self, *args, **kwargs):
        self.interaction_type = 'note'
        super(Note, self).save()    

#class Note

class Task(Interaction):
    title = models.CharField(max_length=250)
    note_text = models.TextField(null=True, blank=True)
    status = models.IntegerField(default=1)

    def __unicode__(self):
        return "%s %s" % (self.interaction_date, self.task_name)
    
    def save(self, *args, **kwargs):
        self.interaction_type = 'task'
        super(Task, self).save()


#-------------------------------------------------------------------------------
#class Comment(models.Model):
#    """Абстрактный класс для комментариев """
#    created_by = models.ForeignKey(User)
#    created_date = models.DateField(auto_now_add=True)
#    comment = models.TextField(u'комментарий')
#    
#    class Meta:
#        abstract=True
#        
#class Comment
#
#class InteractionComment(Comment):
#    interaction = models.ForeignKey(Interaction)

#class InteractionComment      


