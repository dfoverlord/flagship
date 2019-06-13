from django.urls import path

from .views import ImageView, ImageList, PhotoBookView, PhotoBookList, ImageCreate

app_name = 'gallery'
urlpatterns = [
    path('', PhotoBookList.as_view(), name='photobooks_list'),
    path('images/', ImageList.as_view(), name='images_list'),
    path('image/<int:pk>/<slug>', ImageView.as_view(), name='image_detail'),
    path('upload/', ImageCreate.as_view(), name='image_upload'),
    path('photobook/<int:pk>/<slug>/', PhotoBookView.as_view(), name='photobook_detail'),
    path('photobook/<int:apk>/<int:pk>/<slug>', ImageView.as_view(), name='photobook_image_detail')
]