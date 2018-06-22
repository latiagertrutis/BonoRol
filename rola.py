# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    rola.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mrodrigu <mrodrigu@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/06/12 19:05:47 by mrodrigu          #+#    #+#              #
#    Updated: 2018/06/22 12:48:04 by mrodrigu         ###   ########.fr        #
#   git clone https://github.com/syl20bnr/spacemacs ~/.emacs.d                                                                           #
# **************************************************************************** #

import json
import requests
import time
import random
import urllib
from dataBase import *

TOKEN = "585152603:AAGS-XKYqZp4QxjqwmmLGQ31o_pHxMFF204"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

db = DBHelper();

def send_message(text, chat_id):
#	text = urllib.parse.quote_plus(text)
	url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
	get_url(url)

def get_url(url):
	response = requests.get(url)
	content = response.content.decode("utf8")
	return (content)

def get_json_from_url(url):
	content = get_url(url)
	js = json.loads(content)
	return (js)

def get_updates(offset = None):
	url = URL + "getUpdates?timeout=100"
	if offset:
		url += "&offset={}".format(offset)
	js = get_json_from_url(url)
	return (js)

def get_last_update_id(updates):
    update_id = None
    for update in updates["result"]:
        update_id = int(update["update_id"])
    return (update_id)

def dados(update, text, chat):
	user = None
	try:
		user = update[0]["edited_message"]["from"]["first_name"]
	except:
		try:
			user = update[0]["message"]["from"]["first_name"]
		except:
			return
	pos = text.find('D')
	if (pos == 1):
		cuant = 1
	elif (text[1:pos].isdigit()):
		cuant = int(text[1:pos])
	else:
		send_message("*Formato de dado incorrecto*", chat)
		return
	if (text[(pos + 1):].isdigit()):
		dice = int(text[(pos + 1):])
	else:
		send_message("*Formato de dado incorrecto*", chat)
		return
	print("pos: " + str(pos) + "\ndice: " + str(dice))
	if (cuant <= 0 or cuant > 100 or dice <= 0 or dice > 1000):
		send_message("*Formato de dado incorrecto*", chat)
		return
	for i in range(0, cuant):
			send_message("*" + user + "\nD" + str(dice) + ":* " + str(random.randint(1, dice)), chat)

def handle_updates(updates):
#	cosa = updates["result"]
#	print(cosa)
#	print("\n\n")
#	print(cosa[0]["message"])
	update = updates["result"]
	print(update[0]["message"])
	text = None
	chat = None
	try:
		text = update[0]["edited_message"]["text"]
		chat = update[0]["edited_message"]["chat"]["id"]
	except:
		try:
			text = update[0]["message"]["text"]
			chat = update[0]["message"]["chat"]["id"]
		except:
			pass

	if (text and chat and '/' in text and 'D' in text):
		dados(update, text, chat)

def main():
    db.setup();
    last_update_id = None
    while True:
	    updates = get_updates(last_update_id)
	    if len(updates["result"]) > 0:
		    last_update_id = get_last_update_id(updates) + 1
		    handle_updates(updates)
	    time.sleep(0.5)

if __name__ == '__main__':
    main()
