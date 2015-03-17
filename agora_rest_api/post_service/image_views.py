from rest_framework import status
from rest_framework.decorators import api_view

from django.http import HttpResponse


from agora_rest_api import settings

import ldap
import json
import ast
import sys
import pytz
import datetime

@api_view(['POST'])
def get_image(request):
    print "inside!"
    json_data = {}
    try:
        request_data = ast.literal_eval(request.body)
        image_name = request_data['image_name']
        image_url = settings.IMAGES_ROOT + image_name
        image_data = open(image_url).read()
        response = HttpResponse(image_data,status=status.HTTP_200_OK,content_type="image/png")
        return response
    except Exception,e:
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response
    
