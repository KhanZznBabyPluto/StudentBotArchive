import random

class User:
    def __init__(self):
        self.orders = 4
    
    def update_name(self, name, id):
        self.name = name
        self.id = id

    def update_surname(self, surname):
        self.surname = surname
    
    def update_university(self, univ):
        self.univ = univ

    def update_faculty(self, fac):
        self.fac = fac

    def update_group(self, gr):
        self.group = gr

    def update_phone(self, phone):
        self.phone = phone

    def update_group_id(self, id):
        self.group_id = id

    def print(self):
        print(f'User: {self.name} {self.surname} {self.room} {self.id}')
    # def update_phone_number(self, phone):
    #     self.phone = phone


class Group:
    def __init__(self):
        self.flag = 0

    def init_new(self, univ, fac):
        self.univ = univ
        self.fac = fac
        self.id = random.randint(1000000, 9999999)
        self.flag =1