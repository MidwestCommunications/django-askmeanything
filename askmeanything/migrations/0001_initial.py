
from south.db import db
from django.db import models
from askmeanything.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Poll'
        db.create_table('askmeanything_poll', (
            ('id', orm['askmeanything.Poll:id']),
            ('question', orm['askmeanything.Poll:question']),
            ('created', orm['askmeanything.Poll:created']),
            ('open', orm['askmeanything.Poll:open']),
        ))
        db.send_create_signal('askmeanything', ['Poll'])
        
        # Adding model 'Response'
        db.create_table('askmeanything_response', (
            ('id', orm['askmeanything.Response:id']),
            ('poll', orm['askmeanything.Response:poll']),
            ('answer', orm['askmeanything.Response:answer']),
            ('votes', orm['askmeanything.Response:votes']),
        ))
        db.send_create_signal('askmeanything', ['Response'])
        
        # Adding model 'PublishedPoll'
        db.create_table('askmeanything_publishedpoll', (
            ('id', orm['askmeanything.PublishedPoll:id']),
            ('poll', orm['askmeanything.PublishedPoll:poll']),
            ('publication_type', orm['askmeanything.PublishedPoll:publication_type']),
            ('publication_id', orm['askmeanything.PublishedPoll:publication_id']),
            ('published', orm['askmeanything.PublishedPoll:published']),
        ))
        db.send_create_signal('askmeanything', ['PublishedPoll'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Poll'
        db.delete_table('askmeanything_poll')
        
        # Deleting model 'Response'
        db.delete_table('askmeanything_response')
        
        # Deleting model 'PublishedPoll'
        db.delete_table('askmeanything_publishedpoll')
        
    
    
    models = {
        'askmeanything.poll': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'askmeanything.publishedpoll': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askmeanything.Poll']"}),
            'publication_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'publication_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'published': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'askmeanything.response': {
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askmeanything.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['askmeanything']
