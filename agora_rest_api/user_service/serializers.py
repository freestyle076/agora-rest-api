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
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')