from flask import Flask, render_template
from flask import request, redirect, url_for
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)
webapp.config['TEMPLATES_AUTO_RELOAD'] = True

@webapp.route('/browse_drinks', methods=['POST','GET'])
def browse_drinks():
    db_connection = connect_to_database()

    # Adding a new drink from form
    if request.method == 'POST':
        print("Add new drink!")
        price = request.form['price']
        inventory = request.form['inventory']
        secret_ingredient = request.form['sec_ing']
        query = 'INSERT INTO drinks (price, inventory, secret_ingredient) VALUES (%s,%s,%s)'
        data = (price, inventory, secret_ingredient)
        execute_query(db_connection, query, data)
        print("drink added!")
    
    # Getting current drinks 
    print("Fetching and rendering drinks web page")
    query = "SELECT id, price, inventory, secret_ingredient from drinks;"
    drink_result = execute_query(db_connection, query).fetchall()

    # Getting ingredients for add new drink dropdown 
    query = 'SELECT id, ingredient_name FROM ingredients'
    ing_result = execute_query(db_connection,query).fetchall()

    return render_template('browse_drinks.html', rows=drink_result, ingredients = ing_result)

# deleting a drink
@webapp.route('/delete_drink/<int:id>')
def delete_drink(id):
    # remove from drinks table
    db_connection = connect_to_database()
    query = "DELETE FROM drinks WHERE id = %s"
    data = (id,)
    result = execute_query(db_connection, query, data)

    return redirect(url_for('browse_drinks'))

#display update form and process any updates, using the same function
@webapp.route('/update_drink/<int:id>', methods=['POST','GET'])
def update_drink(id):
    db_connection = connect_to_database()
    
    #display existing data
    if request.method == 'GET':
        print('The GET request')
        drink_query = 'SELECT id, price, inventory, secret_ingredient from drinks WHERE id = %s'  % (id)
        drink_result = execute_query(db_connection, drink_query).fetchone()

        if drink_result == None:
            return "No such drink found!"

        query = 'SELECT id, ingredient_name FROM ingredients'
        ing_result = execute_query(db_connection,query).fetchall()
        return render_template('drink_update.html', drink = drink_result, ingredients = ing_result)

    # update drink
    elif request.method == 'POST':
        print('The POST request')
        id = request.form['drink_id']
        price = request.form['price']
        inventory = request.form['inventory']
        secret_ingredient = request.form['sec_ing']

        query = "UPDATE drinks SET price = %s, inventory = %s, secret_ingredient = %s WHERE id = %s"
        data = (price, inventory, secret_ingredient, id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated")

        return redirect('/browse_drinks')

@webapp.route('/drink_search', methods=['GET', 'POST'])
def drink_search():
    drink=["","","",""]
    if request.method == "POST":
        db_connection = connect_to_database()
        drink_id = request.form['drink']
        drink_query = 'SELECT id, price, inventory, secret_ingredient from drinks WHERE id = %s'  % (drink_id)
        drink_result = execute_query(db_connection, drink_query).fetchall()
        return render_template('drink_search.html', drink=drink_result)

    return render_template('drink_search.html')

@webapp.route('/promotions_drinks')
def promotions_drinks():
    db_connection = connect_to_database()
    print("Fetching and rendering promotions_drinks")
    query = "SELECT drink_id, promotion_id from promotions_drinks;"
    result = execute_query(db_connection, query).fetchall()
    return render_template('promotions_drinks.html', rows=result)

# deleting a drink
@webapp.route('/delete_promo_drink/<row>')
def delete_promo_drink(row):
    # remove from m:m table
    db_connection = connect_to_database()
    row = row.strip('(')
    row = row.strip(')')
    ids = row.split(',')
    drink_id = int(ids[0].strip(' '))
    promo_id = int(ids[1].strip(' '))
    query = "DELETE FROM promotions_drinks WHERE drink_id = %s AND promotion_id = %s"
    data = (drink_id,promo_id)
    result = execute_query(db_connection, query, data)

    return redirect(url_for('promotions_drinks'))


