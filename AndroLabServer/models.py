from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))

    def __init__(self, username=None, password=None, first_name=None, last_name=None):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"<User {self.username!r}>"

    @property
    def values(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    account_number = Column(Integer, unique=True)
    account_type = Column(String(50))   # renamed from `type`
    balance = Column(Integer)
    user_id = Column(Integer)
    user = Column(String(50))

    def __init__(self, account_number=None, account_type=None, balance=None, user=None):
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.user = user

    def __repr__(self):
        return f"<Account {self.account_number!r}>"

    @property
    def values(self):
        return {
            "account_number": self.account_number,
            "type": self.account_type,
            "balance": self.balance,
        }
