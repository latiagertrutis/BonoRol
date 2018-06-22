# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    rola.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mrodrigu <mrodrigu@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/06/12 19:05:47 by mrodrigu          #+#    #+#              #
#    Updated: 2018/06/22 18:19:04 by mrodrigu         ###   ########.fr        #
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

def dados(text, chat, user):
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
		if (cuant <= 0 or cuant > 100 or dice <= 0 or dice > 1000):
				send_message("*Formato de dado incorrecto*", chat)
				return
		res = ""
		for i in range(0, cuant):
				res = res + "\n*D" + str(dice) + ":* " + str(random.randint(1, dice))
		send_message("*" + user + "*" + res, chat)

def handle_updates(updates):
		for update in updates["result"]:
				for mess in update:
						if "message" in mess:
								if "text" not in update[mess]:
									return
								text = update[mess]["text"]
								chat = update[mess]["chat"]["id"]
								user = update[mess]["from"]["first_name"]
								if (text and chat and '/' in text and 'D' in text):
										dados(text, chat, user)

def main():
		db.setup()
		last_update_id = None
		while True:
				updates = get_updates(last_update_id)
				if len(updates["result"]) > 0:
						last_update_id = get_last_update_id(updates) + 1
						handle_updates(updates)
				time.sleep(0.5)

if __name__ == '__main__':
		main()
