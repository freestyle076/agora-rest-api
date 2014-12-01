from models import User
from rest_framework import serializers

'''
Serializer classes for data models. Serializers hold model class meta-data
to allow for proper serialization format.
'''

class UserSerializer(serializers.HyperlinkedModelSerializer):
    '''
    User model serializer
    '''
    class Meta:
        model = User
        fields = ('username', 'first_name','pref_email', 'gonzaga_email', 'last_name', 'phone')