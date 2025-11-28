from datetime import datetime
from typing import List
from abc import ABC, abstractmethod


class BankingError(Exception):
    pass


class InsufficientFundsError(BankingError):
    pass


class InvalidAmountError(BankingError):
    pass


class InvalidBranchError(BankingError):
    pass


class Bank:
    def __init__(self, name: str, cnpj: str, location: str, phone: str):
        self._name = name
        self._cnpj = cnpj
        self._location = location
        self._phone = phone
        self._branch: List["Branch"] = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def cnpj(self):
        return self._cnpj

    @cnpj.setter
    def cnpj(self, value):
        self._cnpj = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    def add_branch(self, branch: "Branch"):
        if not isinstance(branch, Branch):
            raise InvalidBranchError(
                f"Expected Branch object, got {type(branch).__name__}"
            )
        self._branch.append(branch)

    def show_branches(self):
        for branch in self._branch:
            print(f"Branch: {branch.name}")


class Branch:
    def __init__(self, number: str, name: str, location: str, phone: str):
        self._number = number
        self._name = name
        self._location = location
        self._phone = phone
        self._accounts: List["Account"] = []

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value


class Client:
    def __init__(self, name, age):
        self._name = name
        self._age = age
        self._accounts: List["Account"] = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = value


class Transaction:
    def __init__(self, type: str, value: float, account: "Account"):
        self._type = type
        self._value = value
        self._account = account
        self._date = datetime.now()

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, value):
        self._account = value

    @property
    def date(self):
        return self._date

    def get_receipt(self):
        print(f"Date: {self.date}")


class Authenticate(ABC):
    @abstractmethod
    def authenticate(self, password: str) -> bool:
        pass


class Tax(ABC):
    @abstractmethod
    def get_tax_value(self) -> float:
        pass


class Earning(ABC):
    @abstractmethod
    def get_earning(self) -> float:
        pass


class Account(Authenticate, ABC):
    def __init__(self, number: str, client: str, balance: float, password: str):
        self._number = number
        self._client = client
        self._balance = balance
        self._password = password
        self._transactions: List["Transaction"] = []

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @abstractmethod
    def withdraw(self, value: float):
        pass

    @abstractmethod
    def deposit(self, value: float):
        pass

    def authenticate(self, password: str) -> bool:
        return self._password == password

    def total(self):
        pass

    def print_total(self):
        pass


class Current_account(Account, Tax):
    def __init__(
        self, number: str, client: str, balance: float, password: str, limit: float
    ):
        super().__init__(number, client, balance, password)
        self._limit = limit
        self._tax = 10.0
        self._transactions: List["Transaction"] = []

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value):
        self._limit = value

    @property
    def tax(self):
        return self._tax

    @tax.setter
    def tax(self, value):
        self._tax = value

    def withdraw(self, value: float):
        if value <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive.")

        total_withdrawal = value + self._tax
        available_funds = self._balance + self._limit

        if total_withdrawal > available_funds:
            raise InsufficientFundsError(
                f"Insufficient funds. Available: {available_funds}, Required: {total_withdrawal}"
            )

        self._balance -= total_withdrawal
        print(f"Remaining balance: {self._balance}")

        transaction = Transaction("current", value, self)
        self._transactions.append(transaction)

    def deposit(self, value: float):
        if value <= 0:
            raise InvalidAmountError("Deposit amount must be positive.")
        self._balance += value

    def get_tax_value(self):
        return self._balance * 0.07


class Savings_account(Account, Earning):
    def __init__(
        self, number: str, titular: str, balance: float, password: str, earnings: float
    ):
        super().__init__(number, titular, balance, password)
        self._earnings = earnings
        self._date = datetime.now().day

    def get_earning(self):
        pass
