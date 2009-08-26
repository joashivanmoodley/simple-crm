# -*- encoding: utf-8 -*-
from django.contrib import admin
from crm.models import Company, Person

from crm.models import Interaction, Note, Task

admin.site.register(Company)
admin.site.register(Person)
admin.site.register(Interaction)
admin.site.register(Note)
admin.site.register(Task)



