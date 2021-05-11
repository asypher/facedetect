from django.conf.urls import url

from main.views import ImageFaceDetect, LiveVideoFaceDetect
app_name = 'main'

urlpatterns = [
    url(r'^face-detect/image/$', ImageFaceDetect.as_view(), name='image'),
    url(r'^face-detect/video/$', LiveVideoFaceDetect.as_view(), name='live_video'),
]
