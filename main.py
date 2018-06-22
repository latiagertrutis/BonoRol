# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mrodrigu <mrodrigu@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/06/12 00:13:38 by mrodrigu          #+#    #+#              #
#    Updated: 2018/06/22 17:30:09 by mrodrigu         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time
import random
from bonoRol import *
from dataBase import *

db = DBHelper();

def build_keyboard(items):
	keyboard = [[item] for item in items]
	reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
	return json.dumps(reply_markup)

def handle_updates(updates):
	for update in updates["result"]:
		print(update)
		text = update["message"]["text"]
		chat = update["message"]["chat"]["id"]
		print(text)

def main():
    db.setup();
    last_update_id = 532
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
