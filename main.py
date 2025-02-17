from collections import UserDict
from datetime import datetime, timedelta
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Phone should have exactly 10 digits')
        self.value = value
        
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone_to_remove: Phone):
        for phone in self.phones:
            if phone.value == phone_to_remove.value:
                self.phones.remove(phone)
                return True
        return False
        

    def edit_phone(self, old: str, new: str):
        old_phone_obj = Phone(old)
        new_phone_obj = Phone(new)

        if old_phone_obj in self.phones:
            self.remove_phone(old_phone_obj)
            self.add_phone(new_phone_obj)
        else:
            comment = 'we dont have such number, try another'
            raise ValueError(comment)

    def find_phone(self, phone):
        if phone in self.phones:
            return phone
        else:
            return None
    
    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def get_bd(self):
        return self.birthday.value.strftime('%d.%m.%Y') if self.birthday else None
    
    def get_name(self):
        return self.name.value
    
    def get_phone(self):
        return [phone.value for phone in self.phones]
            

    def __str__(self):
        phones_str = '; '.join(phone.value for phone in self.phones)
        bd_str = self.get_bd() if self.birthday else 'no birthday to show'
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {bd_str}"

#birthday block

def string_to_date(date_string):
    return datetime.strptime(date_string, "%Y.%m.%d").date()


def date_to_string(date):
    return date.strftime("%Y.%m.%d")


def prepare_user_list(user_data):
    prepared_list = []
    for user in user_data:
        prepared_list.append({"name": user["name"], "birthday": string_to_date(user["birthday"])})
    return prepared_list


def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)


def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday    

class AddressBook(UserDict):

    def __init__(self):
        self.data = {}

    def add_record(self, Record):
        self.data[Record.name.value] = Record

    def find(self, name):
        if name in self.data:
            obj = self.data[name]
            return obj
        else:
            return None
        
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            return 'we dont have this number'
    
    def __str__(self):
        if not self.data:
            return "No contacts in the address book."

        result = '\n'.join(str(record) for record in self.data.values())
        return result
    
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = datetime.today()
        # print(type(today))

        for user in self.data.values():
            if user.birthday:
                bd = user.birthday.value
                birthday_this_year = bd.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = bd.replace(year=today.year + 1)

                if 0 <= (birthday_this_year - today).days <= days:
                    birthday_this_year = adjust_for_weekend(birthday_this_year)

                congratulation_date_str = birthday_this_year.strftime('%d.%m.%Y')
                upcoming_birthdays.append({
                    "name": user.get_name(),
                    "congratulation_date": congratulation_date_str
                })
        return upcoming_birthdays
    
# bot block

# decorators

def input_error_add(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter name and phone for the command"
        except KeyError:
            return "We don't have this name in the database, try another"
        except IndexError:
            return "Please try pattern 'add Bob 1234567890'"
    return inner

def input_error_change(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter name and phone for the command"
        except KeyError:
            return "We don't have this name in data base, try another"
        except IndexError:
            return "Please try pattern 'change Ross 123456789'"
    return inner

def input_error_phone(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter name for the command"
        except KeyError:
            return "We don't have this name in data base, try another"
        except IndexError:
            return "Please try pattern 'phone Dave'"
    return inner

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError, IndexError, KeyError) as e:
            return f"Error: {e}"
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split(' ')
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error_add
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
    
    record.add_phone(phone)
    return f"Contact {name} updated with phone {phone}."

@input_error_change
def change_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)

    if record and record.phones:
        phone_to_remove = record.phones[0]
        record.remove_phone(phone_to_remove)
        record.add_phone(phone)
        return f"Contact {name} updated with new phone {phone}."
    return "No phone number to update."

@input_error_phone
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        return f"{name}'s phone numbers: {', '.join(record.get_phone())}"
    else:
        print('we dont have this contact')

def show_all(args, book: AddressBook):
    return book

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(Birthday(birthday))
        return f"Birthday added for {name}."
    return "Contact not found."

# @input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        return record.get_bd()

# @input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    return upcoming_birthdays

# pickle block

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

#  add john 12345
#  add jane 987654
#  add-birthday john 01.01.2001
#  hello
#  show-birthday john
#  birthdays