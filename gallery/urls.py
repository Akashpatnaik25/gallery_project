from django.urls import path
from .views import gallery, upload_image_api, image_gallery_api, image_upload

urlpatterns = [

path("",gallery,name="gallery_listing"),
path("gallery-list/",image_gallery_api,name="gallery_listing_api"),
path("upload-page/",image_upload,name='image_upload'),
path("upload-image",upload_image_api,name='Upload_image_api')

]