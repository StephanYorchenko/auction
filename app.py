import vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from config import token, group_id

import auction as au


class Server:
    keyboards = {0: ['keyboards/home.json', 'Вы находитесь в главном меню!'],
                 1: ['keyboards/task.json', 'Выберите задание:'],
                 5: ['keyboards/keyboard_start.json', 'Нажмите, чтобы начать'],
                 3: ['keyboards/none.json', ''],
                 }
    users = au.UserDict()
    rooms = au.RoomDict()

    back_button = {1: 0}

    def __init__(self, token, group_id):
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()
        self.random_id = 0

    def send_msg(self, send_id, message=False, keyboard_index=0, start=False):

        """Распределение типов сообщений по методам"""

        if self.users[send_id][0] in {3, 4}:
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
                                      keyboard=open(f'keyboards/keyboard_start.json', 'r',
                                                    encoding='UTF-8').read())
        else:
            self.start_test_message(send_id)

    def start_test_message(self, send_id):

        """Отправка стартового сообщения при запуске теста"""

        self.vk_api.messages.send(peer_id=send_id,
                                  message='Нажмите начать',
                                  random_id=self.random_id,
                                  keyboard=open(f'keyboards/keyboard_start', "r", encoding="UTF-8").read())

    def standard_message(self, send_id, keyboard_index=3, message=0):

        """Отправка стандартых сообщений (меню и прочее)"""
        self.vk_api.messages.send(peer_id=send_id,
                                  message=self.keyboards[keyboard_index][1] if not message else message,
                                  keyboard=open(self.keyboards[keyboard_index][0], "r", encoding="UTF-8").read(),
                                  random_id=self.random_id)

    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                print(self.users, event.type, event.object.text, sep='     ')
                print(self.rooms)
                peer = event.object.peer_id
                print(self.users[peer][0])
                if self.users[peer][0] not in {2, 3, 4, 5}:
                    if event.object.text == 'Аукцион' and self.users[peer][0] == 0:
                        self.users[peer][0] = 1
                    elif event.object.text == 'Открытый пошаговый аукцион' and self.users[peer][0] == 1:
                        self.users[peer][0] = 5
                        self.send_msg(peer, start=True)
                        continue
                    elif event.object.text == 'Назад' and self.users[peer][0] == 1:
                        self.users[peer][0] = 0
                    self.send_msg(peer, keyboard_index=self.users[peer][0])
                elif self.users[peer][0] == 5:
                    print('&&')
                    self.create_room(peer)
                elif self.users[peer][0] == 4:
                    self.send_msg(peer, start=True)
                    if self.rooms.array[self.users[peer][1]].get_number_players() == 3:
                        for t in self.users:
                            if t[1] == self.users[peer][1]:
                                t[0] = 6
                                self.send_msg(peer, start=True)

                elif self.users[peer] == 6:
                    self.rooms.array[self.users[peer][1]].next_step()

    def create_room(self, peer):
        print('creating')
        for x in self.rooms.array.keys():
            print('   @@@')
            if self.rooms.array[x].get_number_players() < 3:
                print(self.rooms)
                self.rooms.array[x].users_array.add(self.get_user_name(peer), peer)
                for t in self.rooms.array[x].users_array:
                    print('---')
                    self.standard_message(t.id,
                                          message=f'{self.get_user_name(peer)} присоединился к игре',
                                          keyboard_index=3)
                    self.users[peer][1] = x
                    self.users[peer][0] = 4
                return 0

        self.rooms[len(self.rooms.array.keys())] = au.Room(au.PlayerChain([au.User(self.get_user_name(peer), peer)]),
                                                           id=len(self.rooms.array.keys()))
        print(len(self.rooms.array))

    def get_user_name(self, user_id):

        """ Получаем имя пользователя"""

        return self.vk_api.users.get(user_id=user_id)[0]['first_name']


if __name__ == '__main__':
    server1 = Server(token, group_id)

    server1.start()
