from django.contrib import admin
from models import Poll, Response

class AnswerInline(admin.TabularInline):
    model = Response
    extra = 5

class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'creator', 'created')
    inlines = [AnswerInline]

admin.site.register(Poll, PollAdmin)