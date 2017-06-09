from django.conf.urls import include, url
from .views import fb_chatbotView
from . import views

urlpatterns = [
    url(r'^fb_chatbot/1234567890$', fb_chatbotView.as_view()),
    url(r'^fb_chatbot/chat_room$', views.chat_room, name='chat_room'),
]