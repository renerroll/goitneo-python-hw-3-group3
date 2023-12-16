import json
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)
        if not self.validate(phone):
            raise ValueError("Invalid phone number format")

    @staticmethod
    def validate(phone):
        return len(phone) == 10 and phone.isdigit()


class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(birthday)
        if not self.validate(birthday):
            raise ValueError("Invalid date format")

    @staticmethod
    def validate(birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones] if phones else []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return "Phone removed"
        return "Phone not found"

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                return "Phone updated"
        return "Phone not found"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name}, Phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, "Record not found")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return "Record deleted"
        return "Record not found"

    def get_birthdays_per_week(self):
        now = datetime.now()
        start, end = self.__get_start_date(now)
        birthdays_storage = {}
        days = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }

        for record in self.data.values():
            if record.birthday:
                birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                birthday = birthday.replace(year=now.year)
                if start <= birthday <= end:
                    weekday = birthday.weekday()
                    if 0 <= weekday <= 4:  
                        birthdays_storage.setdefault(days[weekday], []).append(record.name.value)

        biggest_day_name = max((len(day) for day in days.values()), default=0)
        upcoming_birthday_messages = []
        for i in range(5): 
            day_name = days[i]
            birthdays = birthdays_storage.get(day_name, [])
            if birthdays:
                upcoming_birthday_messages.append(f'{day_name:<{biggest_day_name}}: {", ".join(birthdays)}')
        return upcoming_birthday_messages

    def __get_start_date(self, current_date):
        current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_diff = 6 - current_date.weekday()
        start = current_date + timedelta(days=day_diff - 1)
        end = start + timedelta(days=7, microseconds=-1)
        return start, end

    def save_to_file(self, filename="address_book.json"):
        with open(filename, "w") as file:
            json.dump(self.data, file, default=lambda obj: obj.__dict__, ensure_ascii=False, indent=4)

    def load_from_file(self, filename="address_book.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            for name, record in data.items():
                name_obj = Name(record['name']['value'])
                phones_obj = [Phone(phone['value']) for phone in record['phones']]
                birthday_obj = Birthday(record['birthday']['value']) if record['birthday'] else None
                new_record = Record(name_obj.value, [phone.value for phone in phones_obj], birthday_obj.value if birthday_obj else None)
                self.data[new_record.name.value] = new_record
        except FileNotFoundError:
            pass