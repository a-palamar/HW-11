from collections import UserDict
from datetime import datetime


class Birthday:
    def __init__(self, birthday):
        self._birthday = None
        self.value = birthday

    @property
    def value(self):
        return self._birthday

    @value.setter
    def value(self, birthday):
        if birthday is None:
            self._birthday = None
        else:
            try:
                datetime.strptime(birthday, '%Y-%m-%d')
                self._birthday = birthday
            except ValueError:
                raise ValueError(
                    "Birthday should be in the format 'YYYY-MM-DD'.")

    def __str__(self):
        return str(self._birthday)


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def name_check(self, value):
        if not self.value:
            return ValueError
        else:
            return self.value


class Phone(Field):
    def __init__(self, value) -> None:
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError("Phone number must be 10 digits long.")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday is not None else None

    def days_to_birthday(self):
        if self.birthday.birthday:
            today = datetime.today()
            next_birthday = datetime(
                today.year, self.birthday.birthday.month, self.birthday.birthday.day)
            if today > next_birthday:
                next_birthday = datetime(
                    today.year + 1, self.birthday.birthday.month, self.birthday.birthday.day)
            days_remaining = (next_birthday - today).days
            return days_remaining
        else:
            return "Birthday information is not available."

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError

    def edit_phone(self, exist_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == exist_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone number {exist_phone} not found!")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def __iter__(self):
        return self

    def __next__(self, n=1):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i + n]
        raise StopIteration

    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            for phone in record.phones:
                self.data[record.name.value].add_phone(str(phone))

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print(f"No record found for {name}")

    def find(self, name):
        return self.data.get(name)


# The error handling and command dictionary


def user_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Not enough params. Tip: Enter input in format {command space value}"
        except KeyError:
            return "Unknown rec_id. Try again. Tip: Enter input in format {command space value}"
        except ValueError:
            return "Value error. Tip: Enter input in format {command space value}"
    return inner


address_book = AddressBook()


@user_error
def add(name, phone):
    address_book.add_record(name, phone)
    return f"Add record {name=}, {phone=}"


@user_error
def change(name, phone):
    address_book.change(name, phone)
    return f"Change record {name=}, {phone=}"


@user_error
def greeting():
    return "How can I help you?"


@user_error
def phone(name):
    return f"Existing record {name=}, {address_book.phone(name)}"


@user_error
def show_all():
    return address_book.show_all()


@user_error
def exit_program():
    return "EXIT_PROGRAM"


def unknown():
    return "Unknown command. Try again."


COMMANDS = {
    add: ["add"],
    change: ["change"],
    greeting: ["hello"],
    phone: ["phone"],
    show_all: ["show all"],
    exit_program: ["good bye", "close", "exit"]
}


def parser(text: str):
    for func, kws in COMMANDS.items():
        for kw in kws:
            if text.startswith(kw):
                return func, text[len(kw):].strip().split()
    return unknown, []


def main():
    while True:
        user_input = input(">>>").lower()
        func, data = parser(user_input)
        result = func(*data)
        if result == "EXIT_PROGRAM":
            print("Good bye!")
            break
        else:
            print(result)


if __name__ == '__main__':
    main()
