from flask import Flask, render_template, request, redirect, url_for, flash, session, escape
import sqlite3
import csv

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/home', methods=['POST'])
def home():
    return render_template('index.html')


@app.route('/')
def login():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return render_template('login.html')


@app.route('/log', methods=['POST'])
def log():
    try:
        username_form = request.form['username']
        password_form = request.form['password']
        if username_form == "" and password_form == "":
            flash('Please fill out the fields!')
        else:

            if request.method == 'POST':
                mydb = sqlite3.connect('inventory.db')
                mycursor = mydb.cursor()

                if 'username' in session:
                    return redirect(url_for('index'))
                if request.method == 'POST':
                    mycursor.execute("SELECT UserName FROM logincredentials WHERE UserName = '%s'" % username_form)
                    if mycursor.fetchone()[0]:
                        print("SELECT Password FROM logincredentials WHERE Password = '%s'" % password_form)
                        mycursor.execute("SELECT Password FROM logincredentials WHERE Password = '%s'" % password_form)
                        for row in mycursor.fetchall():
                            if password_form == row[0]:
                                session['username'] = request.form['username']
                                mydb.commit()
                                mycursor.close()
                                flash('Login Successful')
                                return render_template('index.html')
                            else:
                                flash('Incorrect Username/Password')
                                return redirect(url_for('login'))
                        else:
                            flash('Incorrect Username/Password')
                            return redirect(url_for('login'))
                    else:
                        flash('Incorrect Username/Password')
                        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return render_template('login.html')


@app.route('/insert', methods=['POST'])
def insert():
    try:
        id = request.form['newProductID']
        name = request.form['newProductName']
        price = request.form['newProductPrice']
        quantity = request.form['newProductQty']

        if name == "":
            return render_template('index.html')
        elif price == "":
            return render_template('index.html')
        elif quantity == "":
            return render_template('index.html')
        else:

            if request.method == 'POST':
                mydb = sqlite3.connect('inventory.db')
                mycursor = mydb.cursor()
                if request.method == 'POST':
                    mycursor.execute("SELECT COUNT(1) FROM inventoryDetails WHERE ProductID = '%s'" % id)
                    if mycursor.fetchone()[0]:
                        flash(
                            'Product ID:' + id + 'is already present. Click on Update to change the name/price/quantity')
                        return render_template('index.html')
                    else:
                        mycursor.execute("INSERT INTO inventoryDetails values (?,?,?,?);", (id, name, price, quantity,))
                        mydb.commit()
                        mycursor.close()
                        mydb.close()
                        flash(name + ', ' + price + ', ' + quantity + ', Saved!')
                        return render_template('index.html')
                else:
                    return render_template('index.html')
    except Exception as e:
        flash(e)
        return render_template('index.html')


@app.route('/update', methods=['POST'])
def update():
    try:
        id = request.form['prodIDtoUpdate']
        name_prod = request.form['namess']
        pricee = request.form['pricee']
        quantt = request.form['quantityy']
        if name_prod == "":
            return render_template('index.html')
        elif pricee == "":
            return render_template('index.html')
        elif quantt == "":
            return render_template('index.html')
        else:
            if request.method == 'POST':
                mydb = sqlite3.connect('inventory.db')
                mycursor = mydb.cursor()
                if request.method == 'POST':
                    mycursor.execute("SELECT COUNT(1) FROM inventoryDetails WHERE ProductID = '%s';" % id)
                    if mycursor.fetchone()[0]:
                        mycursor.execute("SELECT * FROM inventoryDetails WHERE ProductID = '%s';" % id)
                        produ = mycursor.fetchall()
                        flash(id + ' Found!')
                        for row in produ:
                            b = row[3]
                            if int(b) + int(quantt) < 0:
                                flash('Insufficient quantity')
                                return render_template('index.html')
                            else:
                                sum = int(b) + int(quantt)
                                mycursor.execute("UPDATE inventoryDetails SET Price='" + pricee + "' , Qty='" + str(
                                    sum) + "', ProductName='" + name_prod + "' WHERE ProductID='" + id + "'")
                                mydb.commit()
                                mycursor.close()
                                mydb.close()
                                flash('successfully updated')
                                return render_template('index.html')
                    else:
                        flash('There no such product with ID:  ' + id)
                    return render_template('index.html')
    except Exception as e:
        flash(e)
        return render_template('index.html')


@app.route('/delete', methods=['POST'])
def delete():
    try:
        prodToDelete = request.form['prodToDelete']
        if prodToDelete == "":
            return render_template('index.html')
        else:
            if request.method == 'POST':
                mydb = sqlite3.connect('inventory.db')
                mycursor = mydb.cursor()
                if request.method == 'POST':
                    mycursor.execute("SELECT COUNT(1) FROM inventoryDetails WHERE ProductID = '%s'" % prodToDelete)
                    if mycursor.fetchone()[0]:
                        mycursor.execute("DELETE FROM inventoryDetails WHERE ProductID = '%s'" % prodToDelete)
                        mydb.commit()
                        mycursor.close()
                        mydb.close()
                        flash('Deleted!')
                        return render_template('index.html')
                    else:
                        flash('Product ' + request.form['prodToDelete'] + '  not available')
        return render_template('index.html')
    except Exception as e:
        flash(e)
        return render_template('index.html')


@app.route('/showall', methods=['POST'])
def showall():
    try:
        if request.method == 'POST':
            mydb = sqlite3.connect('inventory.db')
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM inventoryDetails")
            data = mycursor.fetchall()
            return render_template('index.html', products=data)
    except Exception as e:
        flash(e)
        return render_template('index.html')

@app.route('/exportDatatoCSV', methods=['POST'])
def exportDatatoCSV():
    try:
        mydb = sqlite3.connect('inventory.db', isolation_level=None,
                               detect_types=sqlite3.PARSE_COLNAMES)
        mycursor = mydb.cursor()
        productData = mycursor.execute('SELECT * from inventoryDetails')
        with open('inventoryTable.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Product ID', 'Product Name','Price(in USD)','Quantity'])
            writer.writerows(productData)
        flash('Product details have been downloaded into inventoryTable.csv file')
    except Exception as e:
        flash(e)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
