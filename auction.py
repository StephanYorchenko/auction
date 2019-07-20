class Room:
    def __init__(self, array_users, id, auc_step=100, min_cost=500):
        """
        Initialisation of room
        :param array_users: PlayerChain()
        :param auc_step: minimal value of bet
        :param min_cost: starting cost of lot
        """
        self.id = id
        self.users_array = array_users
        self.auc_step = auc_step
        self.current_cost = min_cost

    def get_number_players(self):
        return self.users_array.get_len()

    def next_step(self):
        boolean, cost = self.users_array[0].step(self.current_cost, self.auc_step)
        self.current_cost = cost if boolean else self.current_cost
        self.player_bet(boolean)

    def player_bet(self, boolean_var):
        if boolean_var:
            self.users_array.append()
        else:
            self.users_array.pop()
        if self.users_array.get_len() == 1:
            return self.end_game()
        else:
            self.next_step()

    def end_game(self):
        return self.users_array.get_winner()


class User:
    def __init__(self, name, id, money=1000):
        self.id = id
        self.name = name
        self.money = money
        self.min_value = 10

    def step(self, current_cost, min_step):
        value = self.get_bet(current_cost)
        c = self.check_bet(current_cost, min_step, value)
        return c, c * value

    @staticmethod
    def check_bet(current_cost, min_step, value):
        return value >= current_cost + min_step

    def get_bet(self, cc):
        # TODO: get value by input
        # thi is kostyl for testing
        return int(input(f'bet {self.name} current {cc} '))

    def set_min_value(self, value):
        self.min_value = value


class PlayerChain:
    def __init__(self, array_users):
        """
        Data-structure for looking for users
        :param array_users: list with len == 4 of User()
        """
        self.array = array_users

    def append(self):
        self.array.append(self.array.pop(0))

    def pop(self):
        return self.array.pop(0)

    def get_len(self):
        return len(self.array)

    def get_winner(self):
        return self.array[0]

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, key, value):
        self.array[key] = value

    def add(self, name, id):
        self.array.append(User(name, id))


class HelpfulDict:

    def __init__(self):
        self.array = {}

    def __getitem__(self, peer_id):
        if peer_id not in self.array.keys():
            self.array[peer_id] = 0
        # self.update(peer_id)
        return self.array[peer_id]

    def __setitem__(self, key, value):
        self.array[key] = value

    def __str__(self):
        return f'<------ {len(self.array.keys())} records---->'


if __name__ == '__main__':
    pc = PlayerChain([User('name1', '12345'),
                      User('name2', '23456'),
                      User('name3', '34567'),
                      User('name4', '45678')])
    room = Room(pc)
    room.next_step()
