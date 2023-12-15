from address_book import AddressBook, Record, Phone, Name, Birthday

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Wrong number of arguments"
        except ValueError as ve:
            return str(ve)
        except Exception as e:
            return f"An unexpected error occurred: {e}"
    return inner


@input_error
def hello_command(args, book):
    return "How can I help you?"


@input_error
def add_command(args, book):
    name, phone = args
    if book.find(name) != "Record not found":
        return f"Record with name {name} already exists."
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Record added"


@input_error
def change_command(args, book):
    name, new_phone = args
    record = book.find(name)
    if record == "Record not found":
        return record
    record.phones = [Phone(new_phone)] 
    return "Phone number changed"


@input_error
def remove_command(args, book):
    return book.delete(args[0])


@input_error
def phone_command(args, book):
    name = args[0]
    record = book.find(name)
    if record == "Record not found":
        return record
    return "; ".join([phone.value for phone in record.phones])


@input_error
def all_command(args, book):
    return "\n".join([str(record) for record in book.data.values()])


@input_error
def add_birthday_command(args, book):
    name, date = args
    record = book.find(name)
    if record == "Record not found":
        return "Record not found"
    record.add_birthday(date)
    return "Birthday added"


@input_error
def show_birthday_command(args, book):
    name = args[0]
    record = book.find(name)
    if record == "Record not found":
        return "Record not found"
    if record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    else:
        return "Birthday not set"


@input_error
def birthdays_command(args, book):
    return ", ".join(book.get_birthdays_per_week())


command_functions = {
    "hello": hello_command,
    "add": add_command,
    "change": change_command,
    "remove": remove_command,
    "phone": phone_command,
    "all": all_command,
    "add-birthday": add_birthday_command,
    "show-birthday": show_birthday_command,
    "birthdays": birthdays_command,
}


def main():
    book = AddressBook()
    book.load_from_file()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command in command_functions:
            response = command_functions[command](args, book)
            print(response)
        else:
            print("Invalid command.")

        book.save_to_file() 


if __name__ == "__main__":
    main()