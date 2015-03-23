from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse
from agora_rest_api import settings
from agora_rest_api.post_service.models import BookPost, DateLocationPost, ItemPost, RideSharePost, PostReport

import ast
import json

@api_view(['POST'])
def get_image(request):
    json_data = {}
    try:
        request_data = ast.literal_eval(request.body)
        print request_data
        category = request_data['category'] #switch on category
        post_id = int(request_data['post_id'])
        picture_id = int(request_data['picture_id'])
        #print "Fetching Image " + picture_id + " For Post " + post_id + " Category = " + category
        if category in settings.item_categories:
            post_info = ItemPost.objects.get(id=post_id)    
        elif category in settings.book_categories:
            post_info = BookPost.objects.get(id=post_id)
        elif category in settings.datelocation_categories:
            post_info = DateLocationPost.objects.get(id=post_id)
        elif category in settings.rideshare_categories:
            post_info = RideSharePost.objects.get(id=post_id)
        else:
            json_data['message'] =  'Error in viewing post: Invalid category'

        json_data['category'] = post_info.category
        json_data['post_id'] = str(post_info.id)

        if picture_id == 0:
            image_name = post_info.image1
        elif picture_id == 1:
            image_name = post_info.image2
        else:
            image_name = post_info.image3
            
        if image_name != '':
            image_url = settings.IMAGES_ROOT + image_name
            image_data = open(image_url,"r").read()
            response = form_multipart_response(json_data,image_data,image_name)
            return response
        else:
            response = HttpResponse(status=status.HTTP_204_NO_CONTENT,content_type="image/png")
            return response
            
        
    except Exception,e:
        print str(e)
        response = HttpResponse(status=status.HTTP_400_BAD_REQUEST,content_type='image/png')
        return response
    
def form_multipart_response(json_data,image_data,image_name):    
    BOUNDARY = "$AGORA_boundary$"
    CRLF = "\r\n"
    _content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    
    response = HttpResponse(status=status.HTTP_200_OK,content_type=_content_type)
    response.write('--' + BOUNDARY + CRLF)
    response.write('Content-Disposition: form-data; name="json"' + CRLF)
    response.write('' + CRLF)
    response.write(json.dumps(json_data) + CRLF)
    response.write('--' + BOUNDARY + CRLF)
    response.write('Content-Disposition: form-data; name="image"; filename="%s"\r\n' % image_name)
    response.write('Content-Type: image/png' + CRLF)
    #response.write('Content-Transfer-Encoding: binary' + CRLF)
    response.write('' + CRLF)
    response.write(image_data + CRLF)
    response.write('--' + BOUNDARY + '--' + CRLF)
    response.write('' + CRLF)
    return response
    
    
    '''
    L = []
    L.append('--' + BOUNDARY)
    L.append('Content-Disposition: form-data; name="json"')
    L.append('')
    L.append(json.dumps(json_data))
    L.append('--' + BOUNDARY)
    L.append('Content-Disposition: form-data; name="image"; filename="%s"' % image_name)
    L.append('Content-Type: image/png')
    L.append('')
    L.append(image_data)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    '''
    
    #return content_type, body
        
    
    
