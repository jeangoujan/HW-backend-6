from attrs import define

@define
class User:
    id: int = None
    email: str = ""
    username: str = ""
    password: str = ""


class UserRepository:
    def __init__(self):
        self.users = [
            User(id=1, email="DAMIR", username= "123", password= "123"),
            User(id=2, email="Rimad", username= "321", password= "321"),
        ]

    def save_user(self, user: User):
        user.id = len(self.users) + 1
        self.users.append(user)

    def get_by_username(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def get_by_id(self, id: int) -> User:
        for user in self.users:
            if user.id == id:
                return user
        return None
    

@define
class Flower:
    id: int = None
    flower_name: str = ""
    quantity: int = 0
    price: int = 0

class FlowersRepository:
    def __init__(self):
        self.flowers = [
            Flower(id=1, flower_name="Розы", quantity= 10, price= 200),
            Flower(id=2, flower_name="Пионы", quantity= 20, price= 1000),
        ]

    def save_flower(self, flower: Flower):
        flower.id = len(self.flowers) + 1
        self.flowers.append(flower)

    def get_by_flower_name(self, flower_name: str) -> Flower:
        for flower in self.flowers:
            if flower.flower_name == flower_name:
                return flower
        return None
    
    def get_by_id(self, flower_id: int) -> Flower:
        for flower in self.flowers:
            if flower.id == flower_id:
                return flower
        return None