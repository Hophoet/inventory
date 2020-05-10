#coding:utf-8
import sqlite3
import time

#data base manager creation
class DataBase:
    """database class manager"""
    def __init__(self, name):
        """ database constructor """
        try:
            #connection with the database
            self.connection = sqlite3.connect(f'database/{name}.db')
            #database cursor
            self.cursor = self.connection.cursor()
        except Exception as error:
            print('DATABASE ERROR:', error)

    def close(self):
        """ database closer """
        #close of the database
        self.connection.close()

    def get_total_buy_price(self):
        """ total buy price getter """
        try:
            #get of the total_buy_price
            self.cursor.execute('SELECT SUM(buy_price*quantity) FROM product')
            total_buy_price = self.cursor.fetchall()
            #return of the total_buy_price
            return total_buy_price
        except Exception as error:
            print('DATABASE ERROR:', error)
            self.connection.rollback()
    #method to get total sell price of all products
    def get_total_sell_price(self):
        """ total sell price getter """
        try:
            #get of the get_total_sell_price
            self.cursor.execute('SELECT SUM(sell_price*quantity) FROM product')
            total_sell_price = self.cursor.fetchall()
            #return of the get_total_sell_price
            return total_sell_price
        except Exception as error:
            print('DATABASE ERROR:', error)
            self.connection.rollback()

    #method to get the total price oe the sell products
    def get_sell_products_total_price(self):
        """ getter the total price oe the sell products """
        try:
            #get the total price oe the sell products
            self.cursor.execute('SELECT SUM(sell_price*sell_quantity) FROM product WHERE sell_quantity>0')
            sell_products_total_sell_price = self.cursor.fetchall()
            #return of the sell_products_total_sell_price
            return sell_products_total_sell_price
        except Exception as error:
            print('DATABASE ERROR:', error)

    #method to get total expense price
    def get_total_expense_price(self):
        """ total expense price getter """
        try:
            #get of the total expense
            self.cursor.execute('SELECT SUM(price) FROM expense')
            total_expense_price = self.cursor.fetchall()
            #return of the total_expense_price
            return total_expense_price
        except Exception as error:
            print('DATABASE ERROR:', error)
            self.connection.rollback()

    #method to get all the sell products
    def get_all_sell_products(self):
        """ method to get all the sell products """
        try:
            #get of the sell products, => is at less sell if the sell_quantity >0
            self.cursor.execute('SELECT * FROM product WHERE sell_quantity>0')
            sell_products = self.cursor.fetchall()
            #return of the sell products
            return sell_products
        except Exception as error:
            print('DATABASE ERROR:', error)
            self.connection.rollback()

    def get_all_products(self):
        """ all products getter """
        try:
            #get of the products
            self.cursor.execute('SELECT * FROM product')
            products = self.cursor.fetchall()
            #return of the products
            return products
        except Exception as error:
            print('DATABASE ERROR:', error)
            self.connection.rollback()




    #product getter
    def get_product_by_id(self, id):
        """ product getter by his id(auto increment) """
        try:
            #get request
            self.cursor.execute('SELECT * FROM product WHERE id=?', (id,))
            #get of the product
            product = self.cursor.fetchone()
            return product
        except Exception as error:
            print('DATABASE ERROR:', error)
            self.connection.rollback()

    #customer visits
    def get_all_expenses(self):
        """ all expenses getter """
        try:
            #get of the expenses
            self.cursor.execute('SELECT * FROM expense')
            expenses = self.cursor.fetchall()
            #return of the expenses
            return expenses
        except Exception as error:
            print('DATABASE ERROR:', error)
            self.connection.rollback()

    #visit setter
    def set_expense(self, price, description, moment=time.time()):
        """ expense setter """
        #try execution
        try:
            self.cursor.execute("""
                    INSERT INTO expense(price, description, moment)
                    VALUES(?, ?, ?)""", (price, description, moment))
            self.connection.commit()
        except Exception as error:
            print('DATBASE ERROR:', error)
            self.connection.rollback()

    def set_product(self, name, buy_price, sell_price, quantity, code, moment=time.time()):
        """ product setter """
        #try execution
        try:
            #check existence of the product
            self.cursor.execute('SELECT * FROM product WHERE code=?', (code,))
            #get the customer
            product = self.cursor.fetchone()
            if product:
                print('product exists alrady')
            else:
                self.cursor.execute("""
                    INSERT INTO product(name, buy_price, sell_price, quantity, code, moment)
                    VALUES(?, ?, ?, ?, ?, ?)""", (name, buy_price, sell_price, quantity, code, moment))
                self.connection.commit()
        except Exception as error:
            print('DATBASE ERROR:', error)
            self.connection.rollback()

    #product quantity increser
    def update_product_quantity(self, id, increment=1):
        """increment product qunatity by his id"""
        try:
            #request for the update
            if increment < 0:
                self.cursor.execute("""
                    UPDATE product
                    SET quantity=quantity+?,sell_quantity=sell_quantity-?
                    WHERE id=? """, (increment, increment, id))
                self.connection.commit()
            elif increment > 0:
                self.cursor.execute("""
                    UPDATE product
                    SET quantity=quantity+?
                    WHERE id=? """, (increment, id))
                self.connection.commit()
        except Exception as error:
            print('DATABASE ERROR:', error)
            self.connection.rollback()

    #delete of a product
    def delete_product(self, id):
        """ product deleter """
        try:
            #request for the delete
            self.cursor.execute("""
                DELETE FROM product
                WHERE id=? """, (id,))
            #commiting
            self.connection.commit()
        except Exception as error:
            print('DATABASE ERROR:', error)
            self.connection.rollback()



if __name__ == '__main__':
    database = DataBase('dbase')
    #database.set_data('GL', 'Renseignement', 98764598)
    #database.set_data('kea', 'Renseignement', 99797640)
    #database.set_data('jso', 'Renseignement', 98768593)
    #database.set_expense(2500, 'description', time.time())
    # database.set_product('BOOK XT', 300, 460, 12, time.time())
    # print('seon')
    # for expense in database.get_all_expenses():
    #     print(expense)
    s = database.get_total_expense_price()
    print(s)
