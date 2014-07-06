# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table('album_users', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('friends', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('followers', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('album', ['User'])

        # Adding model 'Tweet'
        db.create_table('album_tweets', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('retweets', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['album.User'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('long', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=3, null=True)),
        ))
        db.send_create_signal('album', ['Tweet'])

        # Adding model 'Media'
        db.create_table('album_medias', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('media_url_http', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('media_url_https', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('album', ['Media'])

        # Adding M2M table for field tweets on 'Media'
        m2m_table_name = db.shorten_name('album_medias_tweets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('media', models.ForeignKey(orm['album.media'], null=False)),
            ('tweet', models.ForeignKey(orm['album.tweet'], null=False))
        ))
        db.create_unique(m2m_table_name, ['media_id', 'tweet_id'])

        # Adding model 'Administration'
        db.create_table('album_administration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('max_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('album', ['Administration'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table('album_users')

        # Deleting model 'Tweet'
        db.delete_table('album_tweets')

        # Deleting model 'Media'
        db.delete_table('album_medias')

        # Removing M2M table for field tweets on 'Media'
        db.delete_table(db.shorten_name('album_medias_tweets'))

        # Deleting model 'Administration'
        db.delete_table('album_administration')


    models = {
        'album.administration': {
            'Meta': {'object_name': 'Administration'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_id': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'album.media': {
            'Meta': {'object_name': 'Media', 'db_table': "'album_medias'"},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'media_url_http': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'media_url_https': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tweets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['album.Tweet']", 'symmetrical': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'album.tweet': {
            'Meta': {'object_name': 'Tweet', 'db_table': "'album_tweets'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'long': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'retweets': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.User']"})
        },
        'album.user': {
            'Meta': {'object_name': 'User', 'db_table': "'album_users'"},
            'followers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'friends': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['album']