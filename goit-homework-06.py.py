from collections import UserDict
from datetime import datetime, timedelta

def input_error(func):
    def inner(phones, birthday):
        try:
            func(phones, birthday)
        except IndexError:
            print("Please enter norm number")
        except KeyError:
            print("Enter user name")
        except ValueError:
            print("plese, press norm number or date birthday")
    return inner

class AdressBook(UserDict):

    def __init__(self):
        super().__init__()
        self.max_value = 1
        self.current_value = 0
        self.page = 1
        self.page_size = 1
    
    def record_in_file(self):
        with open('test.bin', 'wb') as fh:
            pickle.dump(self.data, fh)

    def load_in_file(self):
        with open('test.bin', 'rb') as fh:
            unpack = pickle.load(fh)
            return unpack
    
    def find(self, find_val):
        res = []
        for k, v in self.data.items():
            if find_val in str(k):
                res.append(self.data[k])
            else:
                for phone in v.get_phones():
                    if find_val.lower() in phone.lower():
                        result.append(self.data[k])
                        break
        return result

    @input_error    
    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        self.page = 1
        return self

    def __next__(self):
        start = (self.page - 1) * self.page_size
        end = start + self.page_size
        records = list(self.data.values())[start:end]
        if not records:
            raise StopIteration
        self.page += 1
        for reco in records:
            print(reco.name.value, reco.phones)
        return self

class Record:
    def __init__(self, name, *phones, birthday=None):
        self.name = name
        self.phones = list(phones)
        self.birthday = birthday
        if phone:
            self.phones.append(phone)

    @input_error
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        
    @input_error
    def days_to_birthday(self): 
        date_now = datetime.now()
        self.birthday = datetime.strptime(self.birthday, '%d-%m-%Y')
        self.birthday = self.birthday.replace(year=date_now.year)
        date_days = self.birthday - datetime.now()
        return date_days.days

    @input_error
    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    @input_error
    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = Phone(new_phone)
    
    @input_error
    def get_phones(self):
        return [phone.get_value() for phone in self.phones]

# здесь логика добавления/удаления/редактирования необязательных полей и хранения обязательного поля Name.
    

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
    
# который будет родительским для всех полей, в нем потом реализуем логику общую для всех полей.

class Name(Field):
    pass

class Phone(Field):
    @Field.value.setter
    def value(self, value: str):
        if isinstance(value, str) and value.startswith('+') and len(value) == 13:
            self.__value = value
        else:
            raise ValueError('The name must contain only numbers')

class Birthday(Field):

    @Field.value.setter
    def value(self, value: str):
        try:
            datetime.strptime(value, '%d %B %Y')
            self.__value = value
        except ValueError:
            print('Invalid birthday format')

if __name__ == "__main__":
    name = Name('bob')
    phone = Phone('+123456789000')
    rec = Record(name, phone)
    ab = AdressBook()
    ab.add_record(rec)
    assert isinstance(ab['bob'], Record)
    assert isinstance(ab['bob'].name, Name)
    assert isinstance(ab['bob'].phones, list)
    assert isinstance(ab['bob'].phones[0], Phone)
    # assert ab['bob'].phones[0].value == '+123456789000'
    print('All Ok)')