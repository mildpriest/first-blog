import json, requests, random
from pprint import pprint

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse

from .models import ChatLog
from bs4 import BeautifulSoup

import logging

logger = logging.getLogger(__name__)

ACCESS_TOKEN = "EAAaBkR9jOPUBAAZBuBPO61JzxC0h8d4fuSYLjZBXoGI5jV3To9tqvL1GZCZBkhJpGqasPWnwb4hYJ3Yih8mrNo5I7ZCZC8b1BJ5MCP94nVCVCeZCYRStrYdOmLaKgUzZBTBliArfbIOTOawlINSVJs17AuERZBWftTFy5WEekhf1mmQZDZD"
VERIFY_TOKEN = "1357924680"

msg_text = "몰라"
fbid = "1282792875171205"


def post_fb_message(fb_id, rec_msg):
    # joke_text = requests.get("http://api.icndb.com/jokes/random/").json()['value']['joke']
    post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token=%s"%ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fb_id}, "message":{"text":rec_msg}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


class fb_chatbotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse("Error, invalid token!")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incomming_msg = json.loads(self.request.body.decode('utf-8'))

        no = random.randint(1, 5)

        if no == 1:
            msg_text = "응"
        elif no == 2:
            msg_text = "아니"
        elif no == 3:
            msg_text = "멍청이"
        elif no == 4:
            msg_text = "바보"
        elif no == 5:
            msg_text = "천재 ^^"
        else:
            msg_text = "망"

        for entry in incomming_msg['entry']:
            for msg in entry['messaging']:
                if 'message' in msg:
                    pprint(msg)
                    post_fb_message(msg['sender']['id'], msg_text)
        return HttpResponse()


def chat_room(request):
    if request.is_ajax():
        post_type = request.POST.get('type')
        post_text = request.POST.get('the_post')
        response_data = {}

        if post_type == "q":
            result_text = post_text

        elif post_type == "a":
            url = 'http://search.daum.net/search?w=tot&q=%s'%post_text
            req = requests.get(url)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            objects = soup.findAll('a', attrs={'class': 'f_link_b'})

            length = len(objects)

            if length > 0:
                no = random.randint(1, length)
                result_text = objects[no].text
            else:
                result_text = "어지럽다......"

        else:
            result_text = "error"

        post = ChatLog(text=result_text, type=post_type)
        post.save()

        response_data['chat'] = result_text

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        ChatLog.objects.all().delete()
        return render(request, 'fb_chat/chat_room.html')