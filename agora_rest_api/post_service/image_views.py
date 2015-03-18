from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse
from agora_rest_api import settings
from agora_rest_api.post_service.models import BookPost, DateLocationPost, ItemPost, RideSharePost, PostReport

import ast

@api_view(['POST'])
def get_image(request):
    json_data = {}
    try:
        request_data = ast.literal_eval(request.body)
        category = request_data['category'] #switch on category
        post_id = int(request_data['post_id'])
        picture_id = int(request_data['picture_id'])
        print "Fetching Image " + picture_id + " For Post " + post_id + " Category = " + category
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


        if picture_id == 0:
            image_name = post_info.image1
        elif picture_id == 1:
            image_name = post_info.image2
        else:
            image_name = post_info.image3
            
        if image_name != '':    
            image_url = settings.IMAGES_ROOT + image_name
            image_data = open(image_url).read()
            response = HttpResponse(image_data,status=status.HTTP_200_OK,content_type="image/png")
        else:
            response = HttpResponse(status=status.HTTP_204_NO_CONTENT,content_type="image/png")
            
        
    except Exception,e:
        print str(e)
        response = HttpResponse(image_data,status=status.HTTP_400_BAD_REQUEST,content_type='image/png')
        return response
    
