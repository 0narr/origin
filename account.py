import mysql.connector
import random


def is_fullage(value):
    """
    Sprawdza wiek podany przez użytkownika
    :param value: age
    """
    if int(value) >= 18:
        return True
    else:
        print('Niepełnoletni nie mogą tworzyć konta!')
        return False


def is_card_exist(database: mysql.connector, cardnumber, pin=None):
    """
    Sprawdzenie czy podana karta występuje w bazie danych
    :param database: baza danych
    :param cardnumber: numer karty
    :param pin: pin karty
    """
    cursor = database.cursor()

    if pin is None:  # Kiedy pin nie podany
        sql = ('SELECT card FROM accounts WHERE card=%s')
        values = (cardnumber,)
    else:  # Kiedy podano pin
        sql = ('SELECT card FROM accounts WHERE card=%s AND pin=%s')
        values = (cardnumber, pin)

    cursor.execute(sql, values)
    result = cursor.fetchone()
    cursor.close()

    if result is not None:
        return True  # Kiedy istnieje
    else:
        return False  # Kiedy nie istnieje


def log_into_account(database):
    """
    Funkcja logowania do konta
    """
    cardnumber = input('Podaj numer karty >> ')
    pin = input('Podaj pin >> ')
    print('Sprawdzam...')
    if is_card_exist(database, cardnumber, pin):
        account = get_account_from_database(database, cardnumber)
        print('Pomyślnie zalogowano!')  # Logowanie udane
        return account
    else:
        print('Logowanie nieudane!')  # Logowanie nieudane
        return None


def create_account(database):
    """
    Funkcja tworzenia konta
    """
    # Imie
    firstname = input('Podaj imię >> ')
    # Nazwisko
    lastname = input('Podaj nazwisko >> ')
    # Numer karty
    while True:
        card_no = random.randint(1000, 9999)
        if not is_card_exist(database, card_no):
            break
    print('Twoj numer karty >>', card_no)
    # Pin
    pin = input('Ustaw pin >> ')
    # Balans
    balance = 0
    acc = Account(firstname, lastname, card_no, pin, balance)
    acc.add_account_to_database(database)
    acc.print_information()


def get_account_from_database(database, cardnumber):
    """
    Zwraca obiekt Account z bazy danych
    """
    try:
        cursor = database.cursor()

        sql = f'SELECT firstname, lastname, card, pin, balance FROM accounts WHERE card={cardnumber}'
        cursor.execute(sql)

        result = cursor.fetchone()
        if result:
            account = Account(
                result[0],
                result[1],
                result[2],
                result[3],
                result[4]
            )
            cursor.close()

            return account

    except mysql.connector.Error as err:
        print(err)
        return None


class Account:

    def __init__(self, firstname, lastname, cardnumber, pin, balance):
        self.firstname = firstname
        self.lastname = lastname
        self.cardnumber = cardnumber
        self.pin = pin
        self.balance = balance

    def set_firstname(self, value):
        self.firstname = value

    def set_lastname(self, value):
        self.lastname = value

    def set_cardnumber(self, value):
        self.cardnumber = value

    def set_pin(self, value):
        self.pin = value

    def set_balance(self, value):
        self.balance = value

    def print_details(self):
        print(f'\n------ Twoj wyciąg ------\n'
              + f'Właściciel: {self.firstname} {self.lastname}\n'
              + f'Nr.Karty: {self.cardnumber}\n'
              + f'Balans: {self.balance}\n')

    def print_information(self):
        print('\n------ Twoja karta ------\n'
              + 'Posiadacz: ' + self.firstname + ' ' + self.lastname + '\n'
              + 'Numer: ' + str(self.cardnumber) + '\n'
              + 'Pin: ' + str(self.pin) + '\n')

    def add_account_to_database(self, database):
        """
        Wykonywanie zapytania do bazy danych o dodanie nowego rekordu (nowe konto)
        """
        cursor = database.cursor()

        sql = ('INSERT INTO accounts (firstname, lastname, card, pin, balance) '
               'VALUES (%s, %s, %s, %s, %s)')
        values = (self.firstname, self.lastname, self.cardnumber, self.pin, self.balance)

        cursor.execute(sql, values)
        database.commit()
        cursor.close()

    def deposit(self, database):
        amount = input('Podaj kwote do wpłaty: ')
        cursor = database.cursor()

        sql = ('INSERT INTO deposits (firstname, lastname, amount) '
               'VALUES (%s, %s, %s)')
        values = (self.firstname, self.lastname, amount)

        cursor.execute(sql, values)
        database.commit()
        cursor.close()
