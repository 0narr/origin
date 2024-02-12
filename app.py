import mysql.connector

import account


def connect_to_database():
    """
    Baza danych aplikacji
    """
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='python-atm-system'
        )
        return mydb
    except mysql.connector.Error as err:
        print(f'Połączenie do bazy danych nieudane! {err}')
        return None


def login_panel(database):
    option = None
    while option != 'exit':
        option = input('Wybierz opcje: login, create, exit: ')
        if option == 'login':  # Logowanie
            print('\n------ Logowanie ------')
            logged_user = account.log_into_account(database)
            if logged_user is not None:
                atm_panel(database, logged_user)
        elif option == 'create':  # Tworzenie konta
            print('\n------ Tworzenie konta ------')
            account.create_account(database)
        else:  # Niepoprawna operacja!
            print('Operacja nieprawidłowa!\n')

    print('Żegnaj!')


def atm_panel(database, user):
    print(f'\nWitaj {user.firstname}!')
    option = None
    while option != 'logout':
        option = input('Wybierz operację\n'
                       + '-withdrawal\n'
                       + '-deposit\n'
                       + '-transfer\n'
                       + '-pinchange\n'
                       + '-printdetails\n'
                       + '-logout\n'
                       + '>>')
        if option == 'withdrawal':  # Wpłata na konto
            pass
        elif option == 'deposit':  # Wypłata
            pass
        elif option == 'transfer':  # Transfer miedzy kontam
            pass
        elif option == 'pinchange':  # Zmiana pinu
            pass
        elif option == 'printdetails':  # Wydrukowanie detali konta (wyciąg z konta)
            user.print_details()
            pass
        elif option == 'logout':
            pass
        else:
            print('Niepoprawna opcja!')  # Niepoprawna operacja!


def run():
    database = connect_to_database()
    if database is not None:
        print('atm-system')
        login_panel(database)


run()
