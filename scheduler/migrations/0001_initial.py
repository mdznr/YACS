# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Schedule'
        db.create_table('scheduler_schedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crns', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(unique=True, max_length=200)),
            ('course_ids', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=200, db_index=True)),
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedules', to=orm['courses.Semester'])),
        ))
        db.send_create_signal('scheduler', ['Schedule'])

        # Adding unique constraint on 'Schedule', fields ['crns', 'semester']
        db.create_unique('scheduler_schedule', ['crns', 'semester_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Schedule', fields ['crns', 'semester']
        db.delete_unique('scheduler_schedule', ['crns', 'semester_id'])

        # Deleting model 'Schedule'
        db.delete_table('scheduler_schedule')


    models = {
        'courses.semester': {
            'Meta': {'unique_together': "(('year', 'month'),)", 'object_name': 'Semester'},
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ref': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'scheduler.schedule': {
            'Meta': {'unique_together': "(('crns', 'semester'),)", 'object_name': 'Schedule'},
            'course_ids': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '200', 'db_index': 'True'}),
            'crns': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedules'", 'to': "orm['courses.Semester']"})
        }
    }

    complete_apps = ['scheduler']
