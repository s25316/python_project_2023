import sqlite3
import os
from datetime import datetime

path_to_file = os.getcwd()+"\\Report"

yes = "tak"
no = "nie"

id_ = "id"
name_ = "name"
description_ = "description"
price_ = "price"
amount_ = "amount"



# ERRORS
error_uncorrect = "Wprowadzono niekorektne dane: "

uncorrect_id = "id"
uncorrect_price = "cena/y"
uncorrect_type = "cena/y"
uncorrect_amount = "ilość/i"

error_type = " typ/u "
error_price_val = " powinno być \"00.00\" "
error_lower_0 = " powinno być >= 0 "

#Staitments
staitment_database_created = "Baza danych z podną nazwą została utwożona: "

staitment_0_products_in_databse = "Brak produkt/ów w bbazie danyych"

staitment_product_id_exist = "Produkt/y pod podanym id insnieje/ą, id:"
staitment_product_id_not_exist = "Produkt/y pod podanym id nie insnieje/ą, id:"
staitment_product_name_not_exist = "Produkt/y z nazwą o wartości nie insnieje/ą, wartość:"


staitment_product_added = "Produkt dodany pod numerem id: "
staitment_product_not_added = "Produkt nie dodany pod numerem id: "


staitment_deleted_success = "Wartość z podanym id zosała usunięta, id: "
staitment_deleted_unsuccess = "Wartość z podanym id nie zosała usunięta, id: "

staitment_operaton_realizated = "Operacja wykonana"
staitment_operaton_denied = "Operacja przerwana"


#Questions
question_for_delete = "Czy na pewno chesz usunąc dany produkt ? Tak wpisz \""+yes+"\", Nie wpisz dowolną wartość \n"
question_for_update = "Czy na pewno chesz aktualizować dane danego produktu? Tak wpisz \""+yes+"\", Nie wpisz dowolną wartość \n"
question_for_update_id = "Czy chesz aktualizować dane "+id_+" danego produktu? Tak wpisz \""+yes+"\", Nie wpisz dowolną wartość \n"
question_for_update_name =  "Czy chesz aktualizować dane "+name_+" danego produktu? Tak wpisz \""+yes+"\", Nie wpisz dowolną wartość \n"
question_for_update_description =  "Czy chesz aktualizować dane "+description_+" danego produktu? Tak wpisz \""+yes+"\", Nie wpisz dowolną wartość \n"
question_for_update_price =  "Czy chesz aktualizować dane "+price_+" danego produktu? Tak wpisz \""+yes+"\", Nie wpisz dowolną wartość \n"
question_for_update_amount =  "Czy chesz aktualizować dane "+amount_+" danego produktu? Tak wpisz \""+yes+"\", Nie wpisz dowolną wartość \n"

command_set_id = "Wpisz nowe"+id_+":\n"
command_set_name = "Wpisz nowe"+name_+":\n"
command_set_description = "Wpisz nowe"+description_+":\n"
command_set_price = "Wpisz nowe"+price_+":\n"
command_set_amount = "Wpisz nowe"+amount_+":\n"


#Classes
#=====================================================================     
#=====================================================================     

class Pair :
    def __init__ (self, first , hand ):
        try :
            self.first = bool (first)
        except ValueError:
            print ("Uncorrect information should be bool")
        self.hand = hand

    def get_first (self):
        return self.first

    def get_hand (self):
        return self.hand

    def set_hand (self, hand2):
        self.hand = hand2 
    
#=====================================================================     
class DataBase :

    def is_correct_id ( self, indeteficator ):
        is_correct = True
        error_information = error_uncorrect + uncorrect_id + " - "
        try:
            x = int (indeteficator)
        except ValueError:
            is_correct = False
            error_information = error_information + error_type 
        return Pair ( is_correct, error_information + " (" + str (indeteficator) + ")")

    def is_correct_price ( self, price ):
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
        self.database.close()
    
    def create_base (self):
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
        print (staitment_database_created + self.database_name )

    
    #=====================================================================

    def is_exist_id (self, indeteficator):
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
            information = staitment_product_not_added + str (indeteficator) + "\n\n"
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
        amount_of_records = self.cur.execute(""" SELECT COUNT (1) FROM warehouse""").fetchall() [0][0]
        max_id = 0
        if amount_of_records != 0:
            max_id = self.cur.execute(""" SELECT MAX (id) FROM warehouse""").fetchall() [0][0]
            max_id = max_id + 1
        is_added = self. add_product_with_id ( max_id , name, description, price, amount)
        return Pair ( is_added.get_first() , is_added. get_hand())
    
    #=====================================================================
    def table_to_string (self, table):
        text = ""
        text += id_+"\t|\t"+name_ +"\t|\t"+ description_+"\t|\t"+price_+"\t|\t"+amount_ +"\n"
        for line in table:
            for value in line:
                text += str (value) + "\t|\t"
            text += "\n"
        return  text
    
    def select_by_id (self, indeteficator):
        is_exist_values = True
        information = ""
        is_exist_id = self. is_exist_id ( indeteficator )
        if is_exist_id. get_first() == True :
            table = self. cur.execute(""" SELECT * FROM warehouse WHERE ID = ?""", (int (indeteficator),)).fetchall()
            return Pair ( True ,  self. table_to_string (table))
        
        else :
            return Pair ( False , is_exist_id. get_hand() )

    def select_by_name (self, value):
        amount_of_records = self. cur.execute(""" SELECT * FROM warehouse
                                        WHERE name LIKE ? or
                                        name LIKE ? or
                                        name LIKE ? """, (value+'%','%'+value+'%','%'+value)).fetchall() [0][0]
    
        if amount_of_records > 0 :
            table = self. cur.execute(""" SELECT * FROM warehouse
                                        WHERE name LIKE ? or
                                        name LIKE ? or
                                        name LIKE ? """, (value+'%','%'+value+'%','%'+value)).fetchall() 
            return Pair ( True ,  self. table_to_string (table))
        else :
            return Pair ( False ,  staitment_product_name_not_exist +  str (value) )

    def select_all (self):
        amount_of_records = self. cur.execute(""" SELECT COUNT (1) FROM warehouse """).fetchall() [0][0]
    
        if amount_of_records > 0 :
            table = self. cur.execute(""" SELECT * FROM warehouse """).fetchall() 
            return Pair ( True ,  self. table_to_string (table))
        else :
            return Pair ( False ,  staitment_0_products_in_databse )

    def select (self, value = "a" , by_what = "a" ):
        # dopracować
        if by_what.upper() == id_.upper() :
            return self. select_by_id ( value)
        elif by_what.upper()  == name_.upper() :
            return self. select_by_name ( value)
        else :
            return self. select_all ()
        
    #=====================================================================
    def delete (self, indeteficator):
        is_exist_id = self. is_exist_id ( indeteficator )  
    
        if is_exist_id. get_first () == True :
            self . cur.execute(""" DELETE FROM warehouse WHERE id=?""" ,  (indeteficator,))
            self . database.commit()
            
            return Pair ( True ,  staitment_deleted_success + str (indeteficator) )
        else :
            return Pair ( False ,  staitment_deleted_unsuccess + str (indeteficator) + "\n" + is_exist_id. get_hand() )
    #=====================================================================
    
a = DataBase ("magazyn")
a.create_base ()
x = a. select ()
print (x.get_first()," ",x.get_hand() )
x = a. add_product_with_id (0,"Ogórek szklarniowy", "Polska", 4.55, 100)
print (x.get_first()," ",x.get_hand() )
x = a. add_product_with_id (0,"Ogórek szklarniowy", "Polska", -4.545, -100)
print (x.get_first()," ",x.get_hand() )
x = a. add_product_without_id ("Pomidory na gałązce", "Polska", 4.99, 250)
print (x.get_first()," ",x.get_hand() )

x = a. select (12, id_)
print (x.get_first()," ",x.get_hand() )
x = a. select ()
print (x.get_first()," ",x.get_hand() )
x = a. delete  (12)
print (x.get_first()," ",x.get_hand() )
x = a. delete  (1)
print (x.get_first()," ",x.get_hand() )
a.close_connection ()
