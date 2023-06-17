from DataBaseClass import *

# Update -> choce
# Select -> choce

def print_pair(pair: Pair):
    print(pair.get_first(), pair.get_hand(), sep='\n')

def choice():
    print("""
    Wybierz opcje:

    1. Dodaj rekord z podaniem id
    2. Dodaj rekord bez podania id
    3. Usuń rekord
    4. Wyszukaj rekord (Select)
    5. Generuj raport
    6. Aktualizuj rekord
    7. Wyjdż z programu
    """)

    try:
        option = int(input())
        return option
    except ValueError:
        print("Wprowadzono niekorektne id")
        return choice()

#1. Add product with id
def add_product_with_id ():
    get_id = input("Wprowadż id produktu: \n")
    get_name = input("Wprowadż nazwę produktu: \n")
    get_descriprion = input("Wprowadż opis produktu: \n")
    get_price = input("Wprowadż cenę produktu: \n")
    get_amount = input("Wprowadż liczbę produktu: \n")

    x = a.add_product_with_id (get_id,get_name, get_descriprion,get_price, get_amount )
    print_pair(x)
    
#2. Add product without id
def add_product_without_id ():
    get_name = input("Wprowadż nazwę produktu: \n")
    get_descriprion = input("Wprowadż opis produktu: \n")
    get_price = input("Wprowadż cenę produktu: \n")
    get_amount = input("Wprowadż liczbę produktu: \n")
    
    x = a.add_product_without_id (get_name, get_descriprion,get_price, get_amount )

    print_pair(x)

#3. Delete
def delete ():
    pair = a.select_all()
    print_pair(pair=pair)
    get_id = input("Wprowadż id produktu: \n")

    x = a.delete (get_id)
    
    print_pair(x)
    
#4.1 Select all
def select_all():
    print("""
    Wybierz za jaką wrtością będzie sortowanie (domyślny = id):

    1. Id
    2. Nazwa
    3. Cena
    4. Liczba
    """)
    try:
        option = int(input())
        order_by = OrderBy.by_id
        if option == 2:
            order_by = OrderBy.by_name
        elif option == 3:
            order_by = OrderBy.by_price
        elif option == 4: 
            order_by = OrderBy.by_amount
        pair = a.select_all(order=order_by)
        print_pair(pair=pair)
    except ValueError:
        print("Niepoprawana wrtość")
        return select_all()

#4.2 Select by id
def select_by_id():
    try:
        id = int(input("Wpisz id: "))
        pair = a.select_by_id(id)
        print_pair(pair=pair)
    except ValueError:
        print("Niepoprawana wrtość")
        return select_by_id()
    
#4.3 Select by name
def select_by_name():
    name = input("Wpisz nazwę: ")
    pair = a.select_by_name(name)
    print_pair(pair=pair)

#4. Select
def select():
    print("""
    Wybierz opcje:

    1. Wyszukaj wszystkie rekordy
    2. Wyszukaj wszystkie rekordy za id
    3. Wyszukaj wszystkie rekordy za nazwą
    """)
    
    try:
        option = int(input())
        if option == 1:
            select_all()
        elif option == 2:
            select_by_id()
        elif option == 3:
            select_by_name()
        else:
            print('Podana opcja nie istnieje')
    except ValueError:
        print("Wprowadzono niekorektne id")

#5. Report
def report ():
    try :
        by_what = int (input ("""
        Wyberz za jakim parametrem będzie sortowany raport :\n 
        1. Za 'id' \n 
        2. Za 'nazwą' \n
        3. Za 'ceną' \n
        4. Za liczbą \n
        Wpisz wartość z powyższych: \n'"""))
        orderBy_local = OrderBy.by_id
        
        if by_what == 2 :
            orderBy_local = OrderBy.by_name
        elif by_what == 3 :
            orderBy_local = OrderBy.by_price
        elif by_what == 4 :
            orderBy_local = OrderBy.by_amount

        x = a.make_report (orderBy_local)
        print_pair (x)
    except ValueError:
        print ("Wprowadzono niepoprwaną wartość")

#Id selection for update methods
def select_id_for_update():
    pair = a.select_all()
    print_pair(pair=pair)
    try:
        id = int(input('Wpisz id: '))
        return id
    except ValueError:
        print("Niepoprawana wartość ") 
        return int(select_id_for_update())

#6.1 Update name
def update_name():
    id = select_id_for_update()
    name = input('Wprowadż nową nazwę: ')
    pair = a.update_name(id, name)
    print_pair(pair=pair)

#6.2 Update description
def update_description():
    id = select_id_for_update
    description = input('Wprowadż nowy opis: ')
    pair = a.update_description(id, description)
    print_pair(pair=pair)

#6.3 Update price
def update_price():
    id = select_id_for_update()
    try:
        price = float(input('Wprowadż nową cenę: '))
        pair = a.update_price(id, price)
        print_pair(pair=pair)
    except ValueError:
        print("Niepoprawana wartość ") 
        return update_price()

#6.4 Update amount    
def update_amount():
    id = select_id_for_update()
    try:
        amount = int(input('Wprowadż nową liczbę produktów: '))
        pair = a.update_amount(id, amount)
        print_pair(pair=pair)
    except ValueError:
        print("Niepoprawana wartość ") 
        return update_amount()

#6. Update
def update():
    print("""
    Co aktualizujemy:

    1. Nazwę
    2. Opis
    3. Cenę
    4. Liczbę produktów
    """)

    try:
        option = int(input())
        if option == 1:
            update_name()
        elif option == 2:
            update_description()
        elif option == 3:
            update_price()
        elif option == 4:
            update_amount()
        else:
            print("Podana opcja nie istnieje")
            return update()
    except ValueError:
        print("Niepoprawana wartość ")
        return update()

#7. Exit
def exit_program():
    pair = a.close_connection()
    print_pair(pair=pair)
    exit()

#Program begin
if __name__ == '__main__':
    a = DataBase ("magazyn")
    a.create_base ()

    while True:
        option = choice()
        if option == 1:
            add_product_with_id()
        elif option == 2:
            add_product_without_id()
        elif option == 3:
            delete()
        elif option == 4:
            select()
        elif option == 5:
            report()
        elif option == 6:
            update()
        elif option == 7:
            exit_program()
        else:
            print("Podana opcja nie istnieje wybeirz opcje z podanych ")