import vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from config import token, group_id

import auction as au


class Server:
    keyboards = {0: ['keyboards/home.json', 'Вы находитесь в главном меню!'],
                 1: ['keyboards/type.json', 'Выберите задание:'],
                 2: ['keyboards/start.json', 'Нажмите, чтобы начать'],
                 }
    users = au.HelpfulDict()
    rooms = au.HelpfulDict()

    back_button = {1: 0}

    def __init__(self, token, group_id):
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        self.random_id = 0

    def send_msg(self, send_id, message=False, keyboard_index=0, start=False):

        """Распределение типов сообщений по методам"""

        if self.users[send_id] in {4, 5}:
            self.game_messages(send_id, message, start)
        else:
            self.standard_message(send_id, keyboard_index, message)
        self.random_id += 1

    def game_messages(self, send_id, message, start):

        """Отправка сообщений во время прохождения тестирования"""

        if not start:
            self.vk_api.messages.send(peer_id=send_id,
                                      message=message,
                                      random_id=self.random_id,
                                      keyboard=open(f'keyboards/{send_id}.json', 'r',
                                                    encoding='UTF-8').read())
        else:
            self.start_test_message(send_id)

    def start_test_message(self, send_id):

        """Отправка стартового сообщения при запуске теста"""

        self.vk_api.messages.send(peer_id=send_id,
                                  message=self.keyboards[5][1],
                                  random_id=self.random_id,
                                  keyboard=open(self.keyboards[5][0], "r", encoding="UTF-8").read())

    def standard_message(self, send_id, keyboard_index, message):

        """Отправка стандартых сообщений (меню и прочее)"""

        self.vk_api.messages.send(peer_id=send_id,
                                  message=self.keyboards[keyboard_index][1] if not message else message,
                                  random_id=self.random_id,
                                  keyboard=open(self.keyboards[keyboard_index][0], "r", encoding="UTF-8").read())

    def start(self):
        print('@home')
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                print(self.users, event.type, event.object.text, sep='     ')
                peer = event.object.peer_id
                if event.object.text == 'Аукцион' and self.users[peer] == 0:
                    self.users[peer] = 1

                self.send_msg(peer, keyboard_index=self.users[peer])


if __name__ == '__main__':
    server1 = Server(token, group_id)

    server1.start()
