import sqlite3
import os
from datetime import datetime
from PairClass import Pair
from Order import OrderBy
from tabulate import tabulate

path_to_file = os.getcwd()+"\\Report"

# ERRORS
error_uncorrect = "Wprowadzono niekorektne dane: "

uncorrect_id = "id"
uncorrect_price = "cena/y"
uncorrect_type = "typ/y"
uncorrect_amount = "ilość/i"

error_type = " typ/u "
error_price_val = " powinno być \"00.00\" "
error_lower_0 = " powinno być >= 0 "

#Staitments
staitment_database_created = "Baza danych z podną nazwą została utwożona: "
staitment_database_closed = "Połczenie z Baza danych z podną nazwą zostało przerwane: "

staitment_0_products_in_databse = "Brak produkt/ów w bbazie danyych"

staitment_product_id_exist = "Produkt/y pod podanym id insnieje/ą, id:"
staitment_product_id_not_exist = "Produkt/y pod podanym id nie insnieje/ą, id:"
staitment_product_name_not_exist = "Produkt/y z nazwą o wartości nie insnieje/ą, wartość:"


staitment_product_added = "Produkt dodany pod numerem id: "
staitment_product_not_added = "Produkt nie dodany pod numerem id: "


staitment_deleted_success = "Wartość z podanym id zosała usunięta, id: "
staitment_deleted_unsuccess = "Wartość z podanym id nie zosała usunięta, id: "

staitment_report_generated = "Raport został wygenrowany i znajduje się pod scieżką: "

staitment_updated_success = "Wartość z podanym id zosała odświeżona w bazie danych, id: "
staitment_updated_unsuccess = "Wartość z podanym id nie zosała odświeżona w bazie danych, id: "


#=====================================================================     

#=====================================================================     

class DataBase :

    def is_correct_id ( self, indeteficator ):
        '''Weryfikacja czy id jest wartością INT'''
        is_correct = True
        error_information = error_uncorrect + uncorrect_id + " - "
        try:
            x = int (indeteficator)
        except ValueError:
            is_correct = False
            error_information = error_information + error_type 
        return Pair ( is_correct, error_information + " (" + str (indeteficator) + ")")

    def is_correct_price ( self, price ):
        '''Weryfikacja czy price jest wartością FLOAT z maksymalną liczbą do 2 po przecinku'''
        is_correct = True
        error_information = error_uncorrect + uncorrect_price  + " - "
        try:
            x = float (price)
            if x < float (0) :
                is_correct = False
                error_information = error_information + error_lower_0

            x = (x * 1000) % 10                
            if x > 0 :
                is_correct = False
                error_information = error_information + error_price_val            

        except ValueError:
            is_correct = False
            error_information = error_information + error_type
        return Pair ( is_correct, error_information + " (" + str ( price ) + ")" )

    def is_correct_amount ( self, amount ):
        '''Weryfikacja czy amount jest wartością INT powyżej zera'''
        is_correct = True
        error_information = error_uncorrect + uncorrect_amount  + " - "
        #vereficaton amount correct data and >= 0
        try:
            x = int (amount)
            if x < 0 :
                error_information = error_information + error_lower_0
                is_correct = False
        except ValueError:
            error_information = error_information + error_type
            is_correct = False
        return Pair (is_correct, error_information + " (" + str (amount) + ")" )

    #=====================================================================
    def __init__ (self, database_name):
        self.database_name = database_name
        self.database = sqlite3.connect(database_name)
        #self.database.row_factory = sqlite3.Row
        self.cur = self.database.cursor()

    def close_connection (self):
        '''Zamknięcie połaczenia z bazą danych'''
        self.database.close()
        staitment_database_closed
        return Pair (True , staitment_database_closed + self.database_name )
    
    def create_base (self):
        '''Stworzenie nowej bazy lub uzunięcie wszystkich wartości'''
        self.cur.executescript("""
                        DROP TABLE IF EXISTS warehouse;
                        CREATE TABLE IF NOT EXISTS warehouse (
                            id INTEGER PRIMARY KEY ASC,
                            name varchar(250) NOT NULL,
                            description varchar(1000),
                            price MONEY NOT NULL,
                            amount INTEGER NOT NULL
                        );
                        """)
        self.database.commit()
        return Pair (True , staitment_database_created + self.database_name )
    
    #=====================================================================

    def is_exist_id (self, indeteficator):
        '''Weryfikacja czy za podanym id istnieje rekord w bazie danych'''
        is_exist = True
        information = ""
        is_correct = self.is_correct_id (indeteficator)
        if is_correct. get_first() == True :
            amount_of_records = self.cur.execute(""" SELECT COUNT (1) FROM warehouse WHERE ID = ?""", (int (indeteficator),)).fetchall() [0][0]
    
            if amount_of_records > 0 :
                is_exist = True
                information = staitment_product_id_exist + str (indeteficator) 
            else :
                is_exist = False
                information = staitment_product_id_not_exist +  str (indeteficator) 
        else :
            is_exist = False
            information = is_correct. get_hand ()
        return Pair (is_exist , information )

    
    #=====================================================================
        
    def add_product_with_id (self, indeteficator , name, description, price, amount):
        '''Dodanie produktu do bazy danych z podanym przez urzytkownika id '''
        is_inserted = True
        information = ""
        is_correct_id = self. is_correct_id ( indeteficator )
        is_exist_id = self. is_exist_id ( indeteficator )
        is_correct_price = self . is_correct_price ( price )
        is_correct_amount = self . is_correct_amount ( amount )

        if is_correct_id. get_first() == True and is_exist_id. get_first() == False and is_correct_price. get_first() == True and is_correct_amount. get_first() == True :
            
    
            self.cur.execute('INSERT INTO warehouse VALUES(?, ?, ?, ?, ?);', (indeteficator , name.upper(), description.upper(), price, amount))
            self.database.commit()
            information = staitment_product_added + str (indeteficator)        
        else :
            is_inserted = False
            information = staitment_product_not_added + str (indeteficator) + "\n"
            if is_correct_id. get_first() != True:
                information = information + is_correct_id. get_hand() + "\n"
            if is_correct_id. get_first() == True and is_exist_id. get_first() != False :
                information = information + is_exist_id. get_hand() + "\n"
            if is_correct_price. get_first() != True :
                information = information + is_correct_price. get_hand() + "\n"
            if is_correct_amount. get_first() != True :
                information = information + is_correct_amount. get_hand() + "\n"
            
        return Pair (is_inserted, information)

    def add_product_without_id(self, name, description, price, amount):
        '''Dodanie produktu do bazy danych bez podanego przez urzytkownika id'''
        amount_of_records = self.cur.execute(""" SELECT COUNT (1) FROM warehouse""").fetchall() [0][0]
        max_id = 0
        if amount_of_records != 0:
            max_id = self.cur.execute(""" SELECT MAX (id) FROM warehouse""").fetchall() [0][0]
            max_id = max_id + 1
        is_added = self. add_product_with_id ( max_id , name, description, price, amount)
        return Pair ( is_added.get_first() , is_added. get_hand())
    
    #=====================================================================
    def delete (self, indeteficator):
        '''Usunięcie rekordu zbazy danych za podanym przez urzydkownika id '''
        is_exist_id = self. is_exist_id ( indeteficator )  
    
        if is_exist_id. get_first () == True :
            self . cur.execute(""" DELETE FROM warehouse WHERE id=?""" ,  (indeteficator,))
            self . database.commit()
            
            return Pair ( True ,  staitment_deleted_success + str (indeteficator) )
        else :
            return Pair ( False ,  staitment_deleted_unsuccess + str (indeteficator) + "\n" + is_exist_id. get_hand() )
        
    #=====================================================================
    def table_to_string (self, table):
        console_table = [["ID", "NAZWA", "OPIS", "CENA", "ILOŚĆ"],]

        for row in table :
            values = []
            for value in row :
                values.append(str(value))
            console_table.append(values)
        return tabulate(console_table, headers='firstrow', tablefmt='fancy_grid')
    
    def select_all(self, order: OrderBy = OrderBy.by_id):
        records = self.cur.execute(f"""
        SELECT * FROM warehouse
        ORDER BY {order.value}
        """).fetchall()
        if len(records) > 0:
            return Pair(True, self.table_to_string (records)) 
        else:
            return Pair ( False ,  staitment_0_products_in_databse )


    def select_by_id (self, indeteficator):
        is_exist_id = self. is_exist_id ( indeteficator )
        if is_exist_id. get_first() == True :
            table = self. cur.execute(""" SELECT * FROM warehouse WHERE ID = ?""", (int (indeteficator),)).fetchall()
            return Pair ( True ,  self. table_to_string (table))
        
        else :
            return Pair ( False , is_exist_id. get_hand() )

    def select_by_name (self, name, order: OrderBy = OrderBy.by_id):     
        records = self. cur.execute(f""" SELECT * FROM warehouse
                                        WHERE name LIKE ? or
                                        name LIKE ? or
                                        name LIKE ? 
                                        ORDER BY {order.value}""", (name+'%','%'+name+'%','%'+name,)).fetchall()
        if len(records) > 0 :
            return Pair ( True ,  self. table_to_string (records))
        else :
            return Pair ( False ,  staitment_product_name_not_exist +  str (name) )
  
    #=====================================================================
    def make_report (self, order: OrderBy = OrderBy. by_id):

        records = self.cur.execute(f"""
        SELECT * FROM warehouse
        ORDER BY {order.value}
        """).fetchall()

        text = ''
        for row in records:
            text = text + str(row) + '\n'

        now = datetime.now()
        now = str (now)
        now = now.replace (":","_")
    
        path_file = path_to_file + now +".txt"
        with open(path_file, 'w') as f:
            f.write(str(text.encode('utf8')))
        f.close()
        return Pair ( True ,  staitment_report_generated + path_file )
    #=====================================================================
    def update_name (self, indeteficator, new_name):
        is_exist_id = self. is_exist_id ( indeteficator )  
    
        if is_exist_id. get_first () == True :
            self . cur. execute("""UPDATE warehouse SET name=? WHERE id=?""", (new_name.upper(),indeteficator))
            self . database.commit()
            
            return Pair ( True ,  staitment_updated_success + str (indeteficator) )
        else :
            return Pair ( False ,  staitment_updated_unsuccess + str (indeteficator) + "\n" + is_exist_id. get_hand() )

    def update_description (self, indeteficator, new_description):
        is_exist_id = self. is_exist_id ( indeteficator )  
    
        if is_exist_id. get_first () == True :
            self . cur. execute("""UPDATE warehouse SET description=? WHERE id=?""", (new_description.upper(),indeteficator))
            self . database.commit()
            
            return Pair ( True ,  staitment_updated_success + str (indeteficator) )
        else :
            return Pair ( False ,  staitment_updated_unsuccess + str (indeteficator) + "\n" + is_exist_id. get_hand() )

    def update_price (self, indeteficator, new_price):
        is_exist_id = self. is_exist_id ( indeteficator )  
        is_correct_price = self . is_correct_price ( new_price )
        
        
        if is_exist_id. get_first () == True and is_correct_price . get_first () == True :
            self . cur. execute("""UPDATE warehouse SET price=? WHERE id=?""", (new_price ,indeteficator))
            self . database.commit()
            
            return Pair ( True ,  staitment_updated_success + str (indeteficator) )
        else :
            information = staitment_updated_unsuccess + str (indeteficator)+ "\n" 
            if is_exist_id. get_first () != True :
                information = information  + is_exist_id. get_hand() + "\n"
            if is_correct_price. get_first () != True :
                information = information  + is_correct_price. get_hand() + "\n"

            return Pair ( False , information )
        
    def update_amount (self, indeteficator, new_amount):
        is_exist_id = self. is_exist_id ( indeteficator )  
        is_correct_amount = self . is_correct_amount ( new_amount )
        
        if is_exist_id. get_first () == True and is_correct_amount . get_first () == True :
            self . cur. execute("""UPDATE warehouse SET amount=? WHERE id=?""", (new_amount ,indeteficator))
            self . database.commit()
            
            return Pair ( True ,  staitment_updated_success + str (indeteficator) )
        else :
            information = staitment_updated_unsuccess + str (indeteficator)+ "\n" 
            if is_exist_id. get_first () != True :
                information = information  + is_exist_id. get_hand() + "\n"
            if is_correct_amount. get_first () != True :
                information = information  + is_correct_amount. get_hand() + "\n"

            return Pair ( False , information )