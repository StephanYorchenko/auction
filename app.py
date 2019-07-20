import vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from config import token, group_id

import auction as au


class Server:
    keyboards = {0: ['keyboards/home.json', 'Вы находитесь в главном меню!'],
                 1: ['keyboards/task.json', 'Выберите задание:'],
                 2: ['keyboards/start.json', 'Нажмите, чтобы начать'],
                 3: ['keyboards/none.json', '']
                 5: ['keyboards/keyboard_start.json', 'Нажмите, чтобы начать'],
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

        if self.users[send_id] in {3, 4}:
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
                                  message='рад Вас видеть',
                                  random_id=self.random_id,
                                  keyboard=open(self.keyboards[5][0], "r", encoding="UTF-8").read())

    def standard_message(self, send_id, keyboard_index=3, message=0):

        """Отправка стандартых сообщений (меню и прочее)"""
        print('@')
        self.vk_api.messages.send(peer_id=send_id,
                                  message=self.keyboards[keyboard_index][1] if not message else message,
                                  keyboard=open(self.keyboards[keyboard_index][0], "r", encoding="UTF-8").read(),
                                  random_id=self.random_id)

    def start(self):
        print('@home')
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                print(self.users, event.type, event.object.text, sep='     ')
                peer = event.object.peer_id
                if self.users[peer] not in {3, 4}:
                    if event.object.text == 'Аукцион' and self.users[peer] == 0:
                        self.users[peer] = 1
                        print('@@')
                    elif event.object.text == 'Открыть пошаговый аукцион' and self.users[peer] == 1:
                        self.users[peer] = 3
                        self.send_msg(peer, start=True)
                        continue
                    elif event.object.text == 'Назад' and self.users[peer] == 1:
                        self.users[peer] = 0
                elif self.users[peer] == 3:
                    self.create_room(peer)

                self.send_msg(peer, keyboard_index=self.users[peer])

    def create_room(self, peer):
        for x in self.rooms.array.keys():
            if x.get_number_players() < 3:
                x.array[x.array.get_len()] = au.User(self.get_user_name(peer), peer)
                return [self.standard_message(t.id,
                                              message=f'{self.get_user_name(peer)} присоединился к игре') for t in
                        x.array.values()]

        self.rooms[self.rooms.array.get_len()] = au.Room(au.PlayerChain(au.User(self.get_user_name(peer), peer)),
                                                         id=self.rooms.array.get_len())

    def get_user_name(self, user_id):

        """ Получаем имя пользователя"""

        return self.vk_api.users.get(user_id=user_id)[0]['first_name']


if __name__ == '__main__':
    server1 = Server(token, group_id)

    server1.start()
