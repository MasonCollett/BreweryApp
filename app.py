from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_table import Table, Col
from wtforms import Form, StringField, DecimalField, SubmitField, widgets, SelectMultipleField
import mysql.connector
from db_connector.db_connector import connect_to_database, execute_query
# from db_connector.db_connector import connect_to_database, execute_query

# mysql -u cs340_highlanb -p -h classmysql.engr.oregonstate.edu cs340_highlanb

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
html_top = "<!DOCTYPE html><html>"
css = "<head><title>It'll Get You Drunk</title><link rel='stylesheet' href='static/CSS/flask_stylesheet.css'/></head><body>"
links = "<header> <div class='container'> <h1 class='logo'>It'll Get You Drunk Brewpub</h1><nav><u1 class='menu'>"
links += '<li><a href="http://flip3.engr.oregonstate.edu:36963/ingredients.html">View/Add Ingredients</a></li>'
links += '<li><a href="http://flip3.engr.oregonstate.edu:36963/customers.html">View/Add Customers</a></li>'
links += '<li><a href="http://flip3.engr.oregonstate.edu:36963/promotions.html">View/Add Promotions</a></li>'
links += '<li><a href="http://flip3.engr.oregonstate.edu:36963/browse_drinks.html">View/Add Drinks</a></li>'
links += '<li><a href="http://flip3.engr.oregonstate.edu:36963/promotions_drinks">Active Promotions</a></li>'
links += '<li><a href="http://flip3.engr.oregonstate.edu:36963/drink_search">Search Drinks</a></li></ul>'


# Connector information found at https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
# def connect_database(database_location, user, password, db_name):
#     try:
#         db_connect = mysql.connector.connect(
#             user=user, password=password,
#             database=db_name, host=database_location)
#         return db_connect
#     except:
#         print("Connection failed\n")


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class IngredientTable(Table):
    ingredient_id = Col('id')
    ingredient_name = Col('Ingredient Name')
    supplier = Col('Supplier')
    cost = Col('Cost')


class IngredientItem(object):
    def __init__(self, ingredient_id, ingredient_name, supplier, cost):
        self.ingredient_id = ingredient_id
        self.ingredient_name = ingredient_name
        self.supplier = supplier
        self.cost = cost


class CustomerTable(Table):
    customer_id = Col('id')
    customer_name = Col('Customer Name')
    email = Col('Email Address')
    phone_number = Col('Phone Number')
    favorite_drink = Col('Favorite Drink')
    promo_applied = Col('Current Promotion Applied')


class CustomerItem(object):
    def __init__(self, customer_id, customer_name, email, phone_number, favorite_drink, promo_applied):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.email = email
        self.phone_number = phone_number
        self.favorite_drink = favorite_drink
        self.promo_applied = promo_applied


class PromotionTable(Table):
    promotion_id = Col('id')
    discount = Col('Discount %')
    promotion_name = Col('Promotion Name')
    # applicable_drink = Col('Applicable Drink')


class PromotionItem(object):
    def __init__(self, promotion_id, discount, promotion_name): # , applicable_drink):
        self.promotion_id = promotion_id
        self.discount = discount
        self.promotion_name = promotion_name
        # self.applicable_drink = applicable_drink


class IngredientEntryForm(Form):
    ingredient_name = StringField(u'Ingredient Name')
    supplier = StringField(u'Supplier')
    cost = DecimalField(u'Cost $/lb', places=2)
    submit = SubmitField(u'Add Ingredient')


class SpecialPromotionsEntryForm(Form):
    sql_connection = connect_to_database()
    cursor = sql_connection.cursor()
    query = "SELECT id, name FROM customerss"
    cursor.execute(query)
    results = []
    for customer in cursor:
        results += [customer]
    promo_name = StringField(u'Promotion Name')
    discount_percentage = DecimalField(u'Discount Percentage', places=1)
    # drink_on_special = StringField(u'Applicable Drinks')
    # drinks = MultiCheckboxField('Drinks', choices=results)
    submit = SubmitField(u'Add Promotion')


class CustomersEntryForm(Form):
    name = StringField(u'Name')
    email = StringField(u'Email Address')
    phone = StringField(u'Phone Number')
    favorite_drink = StringField(u'Favorite Drink')
    promo_applied = StringField(u'Current Promotion Applied')
    submit = SubmitField(u'Add Customer')


@app.route('/index.html')
def index():
    return css + links + "</html>"

@app.route('/ingredients.html', methods=['POST', 'GET'])
def ingredients():
    sql_connection = connect_to_database()
    cursor = sql_connection.cursor()
    form = IngredientEntryForm()
    if request.method == 'POST':
        ing_name = request.form['ingredient_name']
        ing_supplier = request.form['supplier']
        ing_cost = request.form['cost']
        if ing_name == "" or ing_supplier == "" or ing_cost == "" or not ing_cost.isnumeric():
            return redirect("/ingredients.html")
        query = "INSERT INTO ingredients (ingredient_name, supplier, cost) VALUES ('%s', '%s', '%s');"
        cursor.execute(query%(ing_name, ing_supplier, ing_cost))
        sql_connection.commit()
        cursor.close()
        sql_connection.close()
        return redirect("/ingredients.html")
    elif request.method == 'GET':
        query = "SELECT * FROM ingredients"
        cursor.execute(query)
        results = []
        for ingredient in cursor:
            results += [ingredient]
        tables = []
        for ingredients in results:
            tables += [IngredientItem(ingredients[0], ingredients[1], ingredients[2], ingredients[3])]

        ingredient_table = IngredientTable(tables, border=1)
        cursor.close()
        sql_connection.close()
        return html_top + css + links + "<body>" + render_template('addingredients.html', form=form) + "<h1>Ingredient Information</h1>" + ingredient_table.__html__() + "</body></html>"

@app.route('/customers.html', methods=['POST', 'GET'])
def customers():
    sql_connection = connect_to_database()
    cursor = sql_connection.cursor()
    form = CustomersEntryForm()
    if request.method == 'POST':
        cust_name = request.form['name']
        cust_email = request.form['email']
        cust_phone = request.form['phone']
        cust_fav_drink = request.form['favorite_drink']
        cust_special_promo = request.form['promo_applied']
        if cust_name == "":
            return redirect("/customers.html")
        query = "INSERT INTO customerss (name, email, phone, favorite_drink, promo_applied) VALUES ('%s', '%s', '%s', '%s', '%s');"
        cursor.execute(query%(cust_name, cust_email, cust_phone, cust_fav_drink, cust_special_promo))
        sql_connection.commit()
        return redirect("/customers.html")

    elif request.method == 'GET':
        query = "SELECT id, name, email, phone, favorite_drink, promo_applied FROM customerss"
        cursor.execute(query)
        results = []
        for customer in cursor:
            results += [customer]
        tables = []
        for customer in results:
            tables += [CustomerItem(customer[0], customer[1], customer[2], customer[3], customer[4], customer[5])]

        customer_table = CustomerTable(tables, border=1)

        return html_top + css + links + "<body>" + render_template('addcustomers.html', form=form) + "<h1>Customer Information</h1>" + customer_table.__html__() + "</body></html>"


@app.route('/promotions.html', methods=['POST', 'GET'])
def promotions():
    sql_connection = connect_to_database()
    cursor = sql_connection.cursor()
    form = SpecialPromotionsEntryForm()

    if request.method == 'POST':
        # return "<html><body>" + str(request.form) + "</body></html>"

        promo_name = request.form['promotion_name']
        discount = request.form['discount']
        cust_special_promo = request.form['promo_applied']
        if promo_name == "" or discount == "" or cust_special_promo == "":
            return redirect("/promotions.html")
        query = "INSERT INTO special_promotions (promo_name, discount_percentage) VALUES ('%s', '%s');"
        cursor.execute(query%(promo_name, discount))
        sql_connection.commit()
        return redirect("/promotions.html")
    elif request.method == 'GET':
        query = "SELECT * FROM special_promotions"
        cursor.execute(query)
        results = []
        for promotion in cursor:
            results += [promotion]
        tables = []
        for promotions in results:
            tables += [PromotionItem(promotions[0], promotions[1], promotions[2])]

        promotion_table = PromotionTable(tables, border=1)
        return html_top + css + links + "<body>" + render_template("addpromotions.html", form=form) + "<h1>Available Promotions:</h1>" + promotion_table.__html__() + "</body></html>"

@app.route('/browse_drinks.html', methods=['POST', 'GET'])
def browse_drinks():
    db_connection = connect_to_database()

    # Adding a new drink from form
    if request.method == 'POST':
        print("Add new drink!")
        price = request.form['price']
        name = request.form['name']
        inventory = request.form['inventory']
        secret_ingredient = request.form['sec_ing']
        if(price != '' and inventory != '' and name != ''):
            query = 'INSERT INTO drinks (price, inventory, secret_ingredient, name) VALUES (%s,%s,%s, %s)'
            data = (price, inventory, secret_ingredient, name)
            execute_query(db_connection, query, data)
            print("drink added!")

    # Getting current drinks
    print("Fetching and rendering drinks web page")
    query = "SELECT drinks.id, price, inventory, ingredients.ingredient_name as 'Secret Ingredient', drinks.name from drinks JOIN ingredients ON drinks.secret_ingredient = ingredients.id;"
    drink_result = execute_query(db_connection, query).fetchall()

    # Getting ingredients for add new drink dropdown
    query = 'SELECT id, ingredient_name FROM ingredients'
    ing_result = execute_query(db_connection, query).fetchall()

    return render_template('browse_drinks.html', rows=drink_result, ingredients=ing_result, links=links)

# deleting a drink
@app.route('/delete_drink/<int:id>')
def delete_drink(id):
    # remove from drinks table
    db_connection = connect_to_database()
    query = "DELETE FROM promotions_drinks WHERE drink_id = %s"
    data = (id,)
    result = execute_query(db_connection, query, data)
    query = "DELETE FROM drinks WHERE id = %s"
    data = (id,)
    result = execute_query(db_connection, query, data)

    return redirect(url_for('browse_drinks'))

#display update form and process any updates, using the same function
@app.route('/update_drink/<int:id>', methods=['POST', 'GET'])
def update_drink(id):
    db_connection = connect_to_database()
    
    #display existing data
    if request.method == 'GET':
        print('The GET request')
        drink_query = 'SELECT id, price, inventory, secret_ingredient, name from drinks WHERE id = %s'  % (id)
        drink_result = execute_query(db_connection, drink_query).fetchone()

        if drink_result == None:
            return "No such drink found!"

        query = 'SELECT id, ingredient_name FROM ingredients'
        ing_result = execute_query(db_connection, query).fetchall()
        return render_template('drink_update.html', drink=drink_result, ingredients=ing_result)

    # update drink
    elif request.method == 'POST':
        print('The POST request')
        id = request.form['drink_id']
        price = request.form['price']
        inventory = request.form['inventory']
        name = request.form['name']
        secret_ingredient = request.form['sec_ing']

        query = "UPDATE drinks SET price = %s, inventory = %s, secret_ingredient = %s, name = %s WHERE id = %s"
        data = (price, inventory, secret_ingredient, name, id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated")

        return redirect('/browse_drinks.html')

@app.route('/drink_search', methods=['GET', 'POST'])
def drink_search():
    drink = ["", "", "", ""]
    if request.method == "POST":
        db_connection = connect_to_database()
        drink_id = request.form['drink']
        drink_query = 'SELECT id, price, inventory, secret_ingredient, name from drinks WHERE id = %s' % (drink_id)
        drink_result = execute_query(db_connection, drink_query).fetchall()
        return render_template('drink_search.html', drink=drink_result, links=links)

    return render_template('drink_search.html', links=links)

@app.route('/promotions_drinks', methods=['POST', 'GET'])
def promotions_drinks():
    db_connection = connect_to_database()

    # Adding a new relationship from form
    if request.method == 'POST':
        print("Add new m:m relationship!")
        drink_id = request.form['drink_id']
        promo_id = request.form['promo_id']
        query = 'INSERT IGNORE INTO promotions_drinks (drink_id, promotion_id) VALUES (%s,%s)'
        data = (drink_id, promo_id)
        execute_query(db_connection, query, data)
        print("relationship added!")

    # Getting table to display relationships
    print("Fetching and rendering promotions_drinks")
    query = "SELECT drink_id, promotion_id, special_promotions.promo_name AS 'Promo Name', drinks.name from promotions_drinks JOIN special_promotions ON promotions_drinks.promotion_id = special_promotions.id JOIN drinks ON promotions_drinks.drink_id = drinks.id;"
    result = execute_query(db_connection, query).fetchall()

    # Getting drink_ids for add new relationship dropdown 
    query = 'SELECT id FROM drinks'
    drink_ids = execute_query(db_connection, query).fetchall()
    drink_ids = list(drink_ids)
    drink_ids = [str(i) for i in drink_ids]
    drink_ids = [i.strip('(),') for i in drink_ids]
    drink_ids = [int(i) for i in drink_ids]
    print("DRINK IDS:", drink_ids)

    # Getting promo_ids for add new relationship dropdown 
    query = 'SELECT id FROM special_promotions'
    promo_ids = execute_query(db_connection, query).fetchall()
    promo_ids = list(promo_ids)
    promo_ids = [str(i) for i in promo_ids]
    promo_ids = [i.strip('(),') for i in promo_ids]
    promo_ids = [int(i) for i in promo_ids]
    print("PROMO IDS:", promo_ids)

    return render_template('promotions_drinks.html', rows=result, drink_ids=drink_ids, promo_ids=promo_ids,links=links)

# deleting a drink
@app.route('/delete_promo_drink/<row>')
def delete_promo_drink(row):
    print("Deleting from promo_drink")
    # remove from m:m table
    db_connection = connect_to_database()
    print(row)
    row = row.strip('(')
    row = row.strip(')')
    ids = row.split(',')
    drink_id = int(ids[0].strip(' '))
    promo_id = int(ids[1].strip(' '))
    query = "DELETE FROM promotions_drinks WHERE drink_id = %s AND promotion_id = %s"
    data = (drink_id, promo_id)
    result = execute_query(db_connection, query, data)

    return redirect(url_for('promotions_drinks'))


