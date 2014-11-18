from models import Post
from rest_framework import serializers

'''
Serializer classes for data models. Serializers hold model class meta-data
to allow for proper serialization format.
'''

class PostSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Post model serializer
    '''
    class Meta:
        model = Post
        fields = ('postid', 'username', 'title', 'category', 'description', 'gonzaga_email', 'pref_email', 'phone', 'price')
        
        
