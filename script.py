""" app script """
#coding: utf-8

#the importations
from kivy.app import App
from kivy.uix.label import Label
import time
from kivy.factory import Factory
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import Screen , ScreenManager
from kivy.properties import ObjectProperty
from kivymd.uix.list import TwoLineIconListItem,IconLeftWidget, ILeftBodyTouch, OneLineIconListItem
from kivymd.uix.bottomsheet import (
    MDGridBottomSheet,
    MDListBottomSheet,
)
#import of the database manager
from datamanager import DataBase
from kivy.lang import Builder

Builder.load_file('script.kv')

class Login(Screen):
    def __init__(self, *args, **kwargs):
        Screen.__init__(self, *args, **kwargs)

    def navigate(self, screen_name):
        self.manager.transition.direction = 'left'
        self.manager.current = screen_name.strip().lower()
        #print(help(self.manager))
        self.ids.password.text = ''

class DetailScreen(Screen):
    """The detail screen of the customer """
    #redefined of the constructor
    def __init__(self, *args, **kwargs):
        """constructor of the detail screen """
        Screen.__init__(self, *args, **kwargs)
        self.database = DataBase('dbase')

    def on_enter(self, *args, **kwargs):
        """redefinition of the enter method of the detail screen """
        #get of the product buy the database with the product id
        self.product = self.database.get_product_by_id(self.manager.screen_tree.product_id)
        #set the product name as the title of the detail screen title
        self.ids.detail_toolbar.title = self.product[1]
        #set of the product informations in the detail screen(name, sell price, buy price, quantity, )
        self.ids.product_name.text = self.product[1]
        self.ids.product_quantity.text =str(self.product[4])
        self.ids.product_buy_price.text ='[b]'+ str(self.product[2]) +'[/b]'
        self.ids.product_sell_price.text ='[b]'+ str(self.product[3]) +'[/b]'

    def back(self, *args, **kwargs):
        """method use for navigation back to the main screen"""
        self.manager.current = 'main'
        #self.ids.box.clear_widgets()
        self.manager.transition.direction = 'left'
    def add_quantity(self, inc):
        # print(dir(self.ids.product_quantity))
        self.ids.add_quantity.text = str( int(self.ids.add_quantity.text) + inc )

    def update_product_quantity(self):
        """ method to update the product quantity """
        #get of the product
        product = self.database.get_product_by_id(id=self.product[0])
        #get of the quantity to add
        add_quantity = int(self.ids.add_quantity.text)
        #checking if the add quantity is less than the product quantity
        if ( product[4] + add_quantity >= 0):
            #update of the quantity in the database
            self.database.update_product_quantity(id=product[0], increment=add_quantity)
            #get of the current modified product
            product = self.database.get_product_by_id(id=self.product[0])
            #change of the product quantity with the new quantity on the screen (detail screen)
            self.ids.product_quantity.text = str(product[4])
            #reset of the add quantity
            self.ids.add_quantity.text = '0'
            print(product)

class Main(Screen):
    """ Main screen class """
    def __init__(self, *args, **kwargs):
        Screen.__init__(self, *args, **kwargs)
        self.display = True
        self.database = DataBase('dbase')

    def navigate(self, product_id, nav='detail'):
        """method use for navigation """
        self.manager.screen_tree.product_id = product_id
        self.manager.current = nav
        #self.ids.box.clear_widgets()
        self.manager.transition.direction = 'right'

    def logout(self, *args, **kwargs):
        """ logout  manager """
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'


    def remove_product(self, product):
        """ product deleter """
        #get of the product in the database
        prd = self.database.get_product_by_id(product.id)
        #check o if the product quantity is zero
        if prd[4] == 0:
            #removing the product in the database by his id
            self.database.delete_product(product.id)
            #removing of the product to the screen
            self.ids.product.remove_widget(product)
            #reload of the total prices on the screen
            self.display_total_prices()

    def show_example_bottom_sheet(self, product):
        """ method the show the bottom sheet after the click on the product """
        #get of the product in the database
        dbase_product = self.database.get_product_by_id(product.id)
        bs_menu = MDListBottomSheet()
        bs_menu.add_item(
            f'{dbase_product[4]}- [b]{dbase_product[1]}[/b] {dbase_product[2]}$ {dbase_product[3]}$',
            lambda x: print(x),
        )
        bs_menu.add_item(
            "view",
            lambda x:self.navigate(product_id=dbase_product[0]),
            icon="file-edit-outline",
        )
        bs_menu.add_item(
            "delete",
            lambda x: self.remove_product(product),
            icon="delete",
        )
        bs_menu.open()



    def save_product(self):
        #get of the production information (name, buy price, sell price, code, quantity)
        name = self.ids.product_name.text
        buy_price = self.ids.buy_price.text
        sell_price = self.ids.sell_price.text
        code = self.ids.code.text
        quantity = self.ids.quantity.text
        #reset of the textinputs
        self.ids.product_name.text = ''
        self.ids.buy_price.text = ''
        self.ids.sell_price.text = ''
        self.ids.code.text = ''
        self.ids.quantity.text = ''
        #save of the product into the database
        self.database.set_product(name=name, buy_price=buy_price, sell_price=sell_price, code=code, quantity=quantity)
        #add of the product in the widget (display in the app)
        self.ids.product.add_widget(
            TwoLineIconListItem(
                text=f'[b]{name}[/b] ',
                secondary_text=f'{buy_price}$\n    {sell_price}$',
                secondary_font_style='Subtitle2',
                on_press=self.show_example_bottom_sheet,

                )#.add_widget(IconLeftSampleWidget(icon='account-card-details'))
        )
        #reload of the total prices on the screen
        self.display_total_prices()

    def save_expense(self):
        #get of the expense price and his description
        price = self.ids.expense_name.text
        description = self.ids.expense_description.text
        #reset the textinput
        self.ids.expense_name.text = ''
        self.ids.expense_description.text = ''
        #saving of the expense into the database
        self.database.set_expense(price=price, description=description)
        #add of the expense in the widget
        self.ids.expense.add_widget(
            TwoLineIconListItem(
                text=f'[b]{price}$[/b] ',
                secondary_text=f'{description}',
                secondary_font_style='Subtitle2',


                )#.add_widget(IconLeftSampleWidget(icon='account-card-details'))
        )
        #reload of the total expense price
        self.display_total_expense_price()

    #method to dispay products
    def display_products(self, products):
        """method to add the current client as a widget in the view part"""

        #set of the remaining product list as a generator
        products = (product for product in products)
        for product in products:
            self.ids.product.add_widget(
                TwoLineIconListItem(
                    id=str(product[0]),
                    text=f'[b]{product[1]}[/b] ',
                    secondary_text=f'{product[2]}$\n    {product[3]}$',
                    secondary_font_style='Subtitle2',
                    on_press=self.show_example_bottom_sheet,

                    )
            )
    #method to dispay products
    def display_sell_products(self, products):
        """method to add the current sell products as a widget in the view part"""
        #display the sell products total price
        self.display_sell_products_total_price()
        #set of the sell products list as a generator
        self.ids.sell_products_scroll.clear_widgets()
        products = (product for product in products)
        for product in products:
            self.ids.sell_products_scroll.add_widget(
                TwoLineIconListItem(
                    id=str(product[0]),
                    text=f'{product[5]}- [b]{product[1]}[/b] ',
                    secondary_text=f'{product[2]}$\n    {product[3]}$',
                    secondary_font_style='Subtitle2',
                    )
            )


    #method to dispay expenses
    def display_expenses(self, expenses):
        """method to add the current expense as a widget in the view part"""

        #set of the expenses list as a generator
        expenses = (expense for expense in expenses)
        for expense in expenses:
            self.ids.expense.add_widget(
                TwoLineIconListItem(
                    text=f'[b]{expense[1]}$[/b] ',
                    secondary_text=f'{expense[2]}',
                    secondary_font_style='Subtitle2',

                    )#.add_widget(IconLeftSampleWidget(icon='account-card-details'))
            )

    #method to display the sell products total price
    def display_sell_products_total_price(self):
        """ method to display the sell products total price """
        self.ids.sell_product_total_price.text = f'[b]{self.database.get_sell_products_total_price()[0][0]}[color=#ffffff55]$[/color][/b]'

    #method to display the total expense price
    def display_total_expense_price(self):
        """method to display the total expense price"""
        self.ids.expense_price.text = f'[b]{self.database.get_total_expense_price()[0][0]}[color=#ffffff55]$[/color][/b]'

    #method to display the total buy and sell price
    def display_total_prices(self):
        """method to display the total buy and sell price"""
        self.ids.total_buy_price.text = f'[b]{self.database.get_total_buy_price()[0][0]}[color=#ffffff55]$[/color][/b]'
        self.ids.total_sell_price.text = f'[b]{self.database.get_total_sell_price()[0][0]}[color=#ffffff55]$[/color][/b]'

    def on_enter(self, *args, **kwargs):
        """redefined method """
        #display of the prices on the screen
        self.display_total_prices()
        self.display_total_expense_price()
        #display of all sell products
        self.display_sell_products(self.database.get_all_sell_products())
        if self.display:
            #display of the products and the expenses
            self.display_products(self.database.get_all_products())
            self.display_expenses(self.database.get_all_expenses())
            self.display = False
        #focus the add product textfield(textinput)
        self.ids.product_name.focus


class Manager(ScreenManager):
    login_screen = ObjectProperty()
    main_screen = ObjectProperty()
    #detail scree
    detail_screen = ObjectProperty()


class Inventor(App):
    """ app class """
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Blue'
    theme_cls.accent_palette = 'Blue'
    theme_cls.accent_palette = 'Gray'
    theme_cls.theme_style = 'Dark'
    #redifined of the application builder
    def build(self):
        return Manager()
