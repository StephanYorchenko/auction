import vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

import auction as au


class Server:
	keyboards = {0: ['keyboards/keyboard_home.json', 'Вы находитесь в главном меню!'],
				 1: ['keyboards/keyboard_info.json', 'О боте'],
				 2: ['keyboards/keyboard_type.json', 'Выберите задание:'],
				 3: ['keyboards/keyboard_start.json', 'Нажмите, чтобы начать'],
				 }
	users = au.HelpfulDict()
	rooms = au.HelpfulDict()

	back_button = {2: 0}

	def __init__(self, token, group_id):
		self.vk = vk_api.VkApi(token=token)
		self.long_poll = VkBotLongPoll(self.vk, group_id)
		self.vk_api = self.vk.get_api()
		self.random_id = 0

	def send_msg(self, send_id, message=False, keyboard_index=0, start=False):

		"""Распределение типов сообщений по методам"""

		if self.users[send_id][0] in {4, 5}:
			self.game_messages(send_id, message, start)
		else:
			self.standard_message(send_id, keyboard_index, message)
		self.random_id += 1

	def game_message(self):




