from django.urls import path
from .views import gallery, upload_image_api, image_gallery_api, image_upload
urlpatterns = [

path("",gallery),
path("gallery-list/",image_gallery_api),
path("upload-page/",image_upload,name='image_upload'),
path("upload-image",upload_image_api,name='Upload_image_api')

]