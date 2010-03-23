
from south.db import db
from django.db import models
from askmeanything.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Poll'
        db.create_table('askmeanything_poll', (
            ('id', orm['askmeanything.Poll:id']),
            ('question', orm['askmeanything.Poll:question']),
            ('owner_type', orm['askmeanything.Poll:owner_type']),
            ('owner_id', orm['askmeanything.Poll:owner_id']),
            ('created', orm['askmeanything.Poll:created']),
        ))
        db.send_create_signal('askmeanything', ['Poll'])
        
        # Adding model 'ResponseChoice'
        db.create_table('askmeanything_responsechoice', (
            ('id', orm['askmeanything.ResponseChoice:id']),
            ('poll', orm['askmeanything.ResponseChoice:poll']),
            ('choice', orm['askmeanything.ResponseChoice:choice']),
            ('votes', orm['askmeanything.ResponseChoice:votes']),
        ))
        db.send_create_signal('askmeanything', ['ResponseChoice'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Poll'
        db.delete_table('askmeanything_poll')
        
        # Deleting model 'ResponseChoice'
        db.delete_table('askmeanything_responsechoice')
        
    
    
    models = {
        'askmeanything.poll': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'owner_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'askmeanything.responsechoice': {
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askmeanything.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {})
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
