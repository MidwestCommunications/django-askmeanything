
from south.db import db
from django.db import models
from askmeanything.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Response'
        db.create_table('askmeanything_response', (
            ('id', orm['askmeanything.response:id']),
            ('poll', orm['askmeanything.response:poll']),
            ('answer', orm['askmeanything.response:answer']),
            ('votes', orm['askmeanything.response:votes']),
        ))
        db.send_create_signal('askmeanything', ['Response'])
        
        # Deleting model 'responsechoice'
        db.delete_table('askmeanything_responsechoice')
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Response'
        db.delete_table('askmeanything_response')
        
        # Adding model 'responsechoice'
        db.create_table('askmeanything_responsechoice', (
            ('votes', orm['askmeanything.response:votes']),
            ('poll', orm['askmeanything.response:poll']),
            ('id', orm['askmeanything.response:id']),
            ('choice', orm['askmeanything.response:choice']),
        ))
        db.send_create_signal('askmeanything', ['responsechoice'])
        
    
    
    models = {
        'askmeanything.poll': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'owner_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
