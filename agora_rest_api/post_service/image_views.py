from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse
from agora_rest_api import settings
from agora_rest_api.post_service.models import BookPost, DateLocationPost, ItemPost, RideSharePost

import ast
import json

@api_view(['POST'])
def get_image(request):
    '''
    POST method for retrieving an image 
    Request body must contain the following data in JSON format:
        category: Category filter, member of collection of lowest level categories
        post_id: id of the post
        picture_id: numerical picture_id (0, 1 or 2) relative to post
    route: /getimage/
    '''
    json_data = {}
    try:
        #parse data
        request_data = ast.literal_eval(request.body)

        #gather picture ID info
        category = request_data['category']
        post_id = int(request_data['post_id'])
        picture_id = int(request_data['picture_id'])
        
        #switch on category
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

        #return values to associate picture w/ post
        json_data['category'] = post_info.category
        json_data['post_id'] = str(post_info.id)

        #get correct picture url from post object depending on positional picture_id
        if picture_id == 0:
            image_name = post_info.image1
        elif picture_id == 1:
            image_name = post_info.image2
        else:
            image_name = post_info.image3
            
        #if the url is NOT an empty string then gather image and return
        if image_name != '':
            json_data["image"] = True
            image_url = settings.IMAGES_ROOT + image_name
            image_data = open(image_url,"r").read()
            response = form_multipart_response(json_data,image_data,image_name)
            return response
        #else there is no image
        else:
            json_data["image"] = False
            response = form_multipart_response(json_data,None,image_name)
            return response
            
    #general exception handling
    except Exception,e:
        print str(e)
        response = HttpResponse(status=status.HTTP_400_BAD_REQUEST,content_type='image/png')
        return response
    
def form_multipart_response(json_data,image_data,image_name):
    '''
    Forms a multipart http response body with components json_data and image_data
    '''
    
    #set header constants
    BOUNDARY = "$AGORA_boundary$"
    CRLF = "\r\n"
    _content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        
    #create response object with 200 status code
    response = HttpResponse(status=status.HTTP_200_OK,content_type=_content_type)
    
    #start boundary
    response.write('--' + BOUNDARY + CRLF)
    response.write('Content-Disposition: form-data; name="json"' + CRLF)
    
    #json data
    response.write('' + CRLF)
    response.write(json.dumps(json_data) + CRLF)

    if image_data:
        #image boundary
        response.write('--' + BOUNDARY + CRLF)
        response.write('Content-Disposition: form-data; name="image"; filename="%s"\r\n' % image_name)
        response.write('Content-Type: image/png' + CRLF)

        #image data
        response.write('' + CRLF)
        response.write(image_data + CRLF)
        
    #final boundary
    response.write('--' + BOUNDARY + '--' + CRLF)
    response.write('' + CRLF)
    
    return response
    
        
    
    
