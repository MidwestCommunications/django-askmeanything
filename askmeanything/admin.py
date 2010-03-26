from django.contrib import admin
from models import Poll, Response, PublishedPoll

class AnswerInline(admin.TabularInline):
    model = Response
    extra = 5

class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'creator', 'created', 'open')
    inlines = [AnswerInline]

class PublishedPollAdmin(admin.ModelAdmin):
    list_display = ('poll', 'publication',)# 'published')
    fields = ('poll', 'publication_type', 'publication_id')

admin.site.register(Poll, PollAdmin)
admin.site.register(PublishedPoll, PublishedPollAdmin)