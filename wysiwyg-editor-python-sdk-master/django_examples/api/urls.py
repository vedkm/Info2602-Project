from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload_file$', views.upload_file, name='upload_file'),
    url(r'^upload_file_validation', views.upload_file_validation, name='upload_file_validation'),
    url(r'^upload_image$', views.upload_image, name='upload_image'),
    url(r'^upload_image_validation', views.upload_image_validation, name='upload_image_validation'),
    url(r'^upload_video$', views.upload_video, name='upload_video'),
    url(r'^upload_video_validation', views.upload_video_validation, name='upload_video_validation'),
    url(r'^upload_image_resize', views.upload_image_resize, name='upload_image_resize'),
    url(r'^delete_file', views.delete_file, name='delete_file'),
    url(r'^delete_image', views.delete_image, name='delete_image'),
    url(r'^delete_video', views.delete_video, name='delete_video'),
    url(r'^load_images', views.load_images, name='load_images'),
    url(r'^amazon_hash', views.amazon_hash, name='amazon_hash'),
]