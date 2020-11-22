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
    
@webapp.route('/delete_drink/<int:id>')
def delete_people(id):
    '''deletes a drink with the given id'''
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

