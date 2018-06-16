# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    bonoRol.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mrodrigu <mrodrigu@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/06/11 23:21:51 by mrodrigu          #+#    #+#              #
#    Updated: 2018/06/12 19:26:50 by mrodrigu         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import json
import requests
import urllib

TOKEN = "611255056:AAHjMHIhSztNCdmbmQSYXEXSNWw-Ro8MZSo"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset = None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
#    print(updates["result"][last_update]["message"]["from"]);
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = text.encode("utf-8")
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    get_url(url)
