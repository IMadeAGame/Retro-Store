from flask import Flask,render_template,request,flash,session,redirect,url_for
from flask_login import current_user
import sqlite3
import datetime

#Regular expression from: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
import re
from itertools import groupby
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
pattern = re.compile(r'(?:\d{4}-){3}\d{4}|\d{16}')

#From: https://gist.github.com/JeffPaine/3083347
states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
months = ['01','02','03','04','05','06','07','08','09','10','11','12']

connection = sqlite3.connect('retro.db')
cursor = connection.cursor()

app = Flask(__name__)
app.secret_key = 'SECRET KEY'

#From: https://stackoverflow.com/questions/46079770/validate-card-numbers-using-regex-python
def count_consecutive(num):
    return max(len(list(g)) for _, g in groupby(num))

def checkCard(cc,sc):
    if not pattern.fullmatch(cc) or count_consecutive(cc.replace('-', '')) >= 4 or len(sc) != 3:
        return False
    for i in range(3):
        if not sc.isnumeric():
            return False
    return True

def checkEmail(email):
    if(re.fullmatch(regex, email)):
        return True

    else:
        return False

def checkZip(zipc):
    if len(zipc) != 5:
        return False
    for i in range(5):
        if not zipc.isnumeric():
            return False
    return True

#Code from: https://stackoverflow.com/questions/15258708/python-trying-to-check-for-a-valid-phone-number
def validNumber(phone_number):
    if len(phone_number) != 12 and  len(phone_number) != 14 and len(phone_number) != 10:
        return False
    for i in range(len(phone_number)):
        if i in [3,7] and len(phone_number) == 12:
            if phone_number[i] != '-' and phone_number[i] != ' ':
                return False
        elif i in [5,9] and len(phone_number) == 14:
            if phone_number[i] != '-':
                return False
        elif i in [0] and len(phone_number) == 14:
            if phone_number[i] != '(':
                return False
        elif i in [4] and len(phone_number) == 14:
            if phone_number[i] != ')':
                return False
        elif not phone_number[i].isnumeric():
            return False
    return True

def checkCart():
    connection = sqlite3.connect('retro.db')
    cursor = connection.cursor()
    titles = []
    publishers = []
    prices = []
    conds = []
    for i in session["CART"]:
        itemstock = cursor.execute("SELECT stock FROM condition WHERE conditionID = ?",[i])
        itemstock = itemstock.fetchone()[0]
        pid = cursor.execute("SELECT productID FROM condition WHERE conditionID = ?",[i])
        pid = pid.fetchone()[0]
        title = cursor.execute("SELECT title FROM product WHERE productID = ?",[pid])
        title = title.fetchone()[0]

        if session["CART"].count(i) > itemstock:
            flash("Item removed from cart: " + title)
            session["CART"].remove(i)
            session["CART"] = session["CART"]
        else:
            titles.append(title)
            publisher = cursor.execute("SELECT publisher FROM product WHERE productID = ?",[pid])
            publisher = publisher.fetchone()[0]
            publishers.append(publisher)
            publisher = cursor.execute("SELECT publisher FROM product WHERE productID = ?",[pid])
            publisher = publisher.fetchone()[0]
            publishers.append(publisher)
            price = cursor.execute("SELECT price FROM condition WHERE conditionID = ?",[i])
            price = price.fetchone()[0]
            prices.append(price)
            cond = cursor.execute("SELECT condition FROM condition WHERE conditionID = ?",[i])
            cond = cond.fetchone()[0]
            conds.append(cond)
    return titles, publishers, prices, conds

@app.route('/')
@app.route('/store')
def store():
    connection = sqlite3.connect('retro.db')
    cursor = connection.cursor()
    products = cursor.execute("SELECT * FROM product")
    products=products.fetchall()
    cond = cursor.execute("SELECT * FROM condition")
    cond=cond.fetchall()
    tot = 0
    stock = []
    imgs = []
    xspace = []
    yspace = []
    y = 9
    x = 15
    for i in range(len(products)):
        if i != 0 and i%3 == 0:
            y+=36
            x = 15
        else:
            x+= 19
        yspace.append(y)
        xspace.append(x)
        for k in range(7*i,7*i+7):
            tot += int(cond[k][3])
        imgs.append(products[i][1] + ".png")
        stock.append(tot)
        tot = 0
    return render_template('store.htm', length=len(products),products=products,cond=cond,stock=stock,imgs=imgs,xspace=xspace,yspace=yspace)

@app.route('/', methods=['GET', 'POST'])
@app.route('/store', methods=['GET', 'POST'])
def store_post():
    connection = sqlite3.connect('retro.db')
    cursor = connection.cursor()
    products = cursor.execute("SELECT * FROM product WHERE title = ?",[request.form['product']])
    pid=products.fetchone()[0]
    return redirect(url_for('product',pid=pid))

@app.route('/sell')
def sell():
    connection = sqlite3.connect('retro.db')
    cursor = connection.cursor()
    products = cursor.execute("SELECT * FROM product")
    products=products.fetchall()
    cond = cursor.execute("SELECT * FROM condition")
    cond=cond.fetchall()
    imgs = []
    xspace = []
    yspace = []
    y = 9
    x = 15
    for i in range(len(products)):
        if i != 0 and i%3 == 0:
            y+=36
            x = 15
        else:
            x+= 19
        yspace.append(y)
        xspace.append(x)
    return render_template('sell.htm', length=len(products),products=products,cond=cond,xspace=xspace,yspace=yspace)

@app.route('/sell', methods=['GET', 'POST'])
def sell_post():
    connection = sqlite3.connect('retro.db')
    cursor = connection.cursor()
    products = cursor.execute("SELECT * FROM product WHERE title = ?",[request.form['product']])
    pid=products.fetchone()[0]
    return redirect(url_for('sellproduct',pid=pid))

@app.route('/register')
def register():
    if "USERNAME" in session:
        return redirect(url_for('store'))
    else:
        return render_template('signup.htm')

@app.route('/register', methods=['GET', 'POST'])
def register_post():
    connection = sqlite3.connect('retro.db')
    cursor = connection.cursor()
    email = request.form['email']
    cemail = request.form['cemail']
    passw = request.form['pass']
    cpassw = request.form['cpass']
    if email == cemail and passw == cpassw:
        if checkEmail(email):
            cursor.execute("SELECT * FROM account WHERE email = ?", [email])
            if cursor.fetchone():
                flash("Email already in use")
                return render_template('signup.htm')
            else:
                cursor.execute('INSERT INTO account(email, password, credit) VALUES(?,?,?)', (email, passw, 0.00))
                connection.commit()
                return redirect(url_for('login'))
        else:
            flash("Invalid Email")
            return render_template('signup.htm')
    else:
        flash("Email or Password does not match")
        return render_template('signup.htm')

@app.route('/logout')
def logout():
    session.pop('USERNAME',None)
    return redirect(url_for('store'))

@app.route('/login')
def login():
    if "USERNAME" in session:
        return redirect(url_for('store'))
    else:
        return render_template('signin.htm')

@app.route('/login', methods=['GET', 'POST'])
def login_post():
    connection = sqlite3.connect('retro.db')
    cursor = connection.cursor()
    email = request.form['email']
    passw = request.form['pass']
    cursor.execute("SELECT * FROM account WHERE email = ?", [email])
    if cursor.fetchone() != None:
        cursor.execute("SELECT password FROM account WHERE email = ?", [email])
        if cursor.fetchone()[0] == passw:
            session["USERNAME"] = email
            session["CART"] = []
            return redirect(url_for('store'))
    flash("Incorrect email or password")
    return render_template('signin.htm')

@app.route('/account')
def account():
    if "USERNAME" in session:
        connection = sqlite3.connect('retro.db')
        cursor = connection.cursor()
        data = cursor.execute("SELECT credit FROM account WHERE email = ?", [session["USERNAME"]])
        credits = data.fetchone()[0]
        return render_template('account.htm',credits = "${:,.2f}".format(credits))
    else:
        return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
def account_post():
    connection = sqlite3.connect('retro.db')
    cursor = connection.cursor()
    return render_template('account.htm')

@app.route('/product/<pid>')
def product(pid):
    connection = sqlite3.connect('retro.db')
    cursor = connection.cursor()
    products = cursor.execute("SELECT * FROM product WHERE productID = ?",[pid])
    product=products.fetchone()
    conds = cursor.execute("SELECT * FROM condition WHERE productID = ?",[pid])
    conds=conds.fetchall()
    prices = []
    stocks = []
    conditions = []
    for i in range(7):
        stocks.append(conds[i][3])
        prices.append("${:,.2f}".format(conds[i][4]))
        conditions.append(conds[i][2])
    return render_template('product.htm',product=product,conds=conds,prices=prices,stocks=stocks,conditions=conditions)

@app.route('/product/<pid>', methods=['GET', 'POST'])
def product_post(pid):
    if "USERNAME" in session:
        connection = sqlite3.connect('retro.db')
        cursor = connection.cursor()
        select = request.form.get('conditions')
        stock = cursor.execute("SELECT stock FROM condition WHERE productID = ? AND condition = ?",[pid,select])
        stock=stock.fetchone()[0]
        cid = cursor.execute("SELECT conditionID FROM condition WHERE productID = ? AND condition = ?",[pid,select])
        cid=cid.fetchone()[0]
        if stock > 0 and session["CART"].count(cid) + 1 <= stock:
            session["CART"].append(cid)
            flash("Item Added to Cart")
            return redirect(url_for('product',pid=pid))
        elif session["CART"].count(cid) + 1 > stock:
            flash("Too Much of one Item in Cart")
        else:
            flash("Item is out of Stock")
        return redirect(url_for('product',pid=pid))
    else:
        return redirect(url_for('login'))

@app.route('/sellproduct/<pid>')
def sellproduct(pid):
    connection = sqlite3.connect('retro.db')
    cursor = connection.cursor()
    products = cursor.execute("SELECT * FROM product WHERE productID = ?",[pid])
    product=products.fetchone()
    conds = cursor.execute("SELECT * FROM condition WHERE productID = ?",[pid])
    conds=conds.fetchall()
    prices = []
    conditions = []
    for i in range(7):
        prices.append("${:,.2f}".format(conds[i][4]/2))
        conditions.append(conds[i][2])
    return render_template('sellproduct.htm',product=product,conds=conds,prices=prices,conditions=conditions)

@app.route('/sellproduct/<pid>', methods=['GET', 'POST'])
def sellproduct_post(pid):
    return redirect(url_for('sellproduct',pid=pid))

@app.route('/cart')
def cart():
    #CREDIT TO: https://stackoverflow.com/questions/5189777/python-adding-3-weeks-to-any-date
    u = datetime.datetime.now()
    d = datetime.timedelta(days=7)
    t = u + d
    delivery = str(t.month) + "/" + str(t.day) + "/" + str(t.year)
    if "USERNAME" in session:
        titles, publishers, prices, conds = checkCart()
        space = []
        total = 0
        for i in range(len(titles)):
            total += prices[i]
            space.append(18*i + 9)
        return render_template('cart.htm',titles=titles,publishers=publishers,prices=prices,conds=conds,length=len(titles),space=space,total="${:,.2f}".format(total),delivery=delivery)
    else:
        return redirect(url_for('login'))

@app.route('/cart', methods=['GET', 'POST'])
def cart_post():
    for i in range(len(session["CART"])):
        select = request.form.get('delete' + str(i))
        if select:
            val = session["CART"][i]
            session["CART"].remove(val)
            session["CART"] = session["CART"]
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    #CREDIT TO: https://stackoverflow.com/questions/5189777/python-adding-3-weeks-to-any-date
    u = datetime.datetime.now()
    d = datetime.timedelta(days=7)
    t = u + d
    delivery = str(t.month) + "/" + str(t.day) + "/" + str(t.year)
    if "USERNAME" in session:
        connection = sqlite3.connect('retro.db')
        cursor = connection.cursor()
        data = cursor.execute("SELECT credit FROM account WHERE email = ?", [session["USERNAME"]])
        credits = data.fetchone()[0]
        _, _, prices, _ = checkCart()
        total = 0
        for i in range(len(prices)):
            total += prices[i]
        shipping = 5.99
        if total >= 35:
            shipping = 0
        years = []
        for i in range(6):
            years.append(t.year + i)
        return render_template('billing.htm',prices=prices,length=len(prices),shipping=shipping,total=total,delivery=delivery,states=states,months=months,years=years,credits=credits)
    else:
        return redirect(url_for('login'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout_post():
    connection = sqlite3.connect('retro.db')
    cursor = connection.cursor()
    fname = request.form['fname']
    lname = request.form['lname']
    phone = request.form['phone']
    address = request.form['address']
    zipc = request.form['zip']
    cc = request.form['creditcard']
    sc = request.form['security']
    credit = request.form['quantity']
    state = request.form.get('states')
    month = request.form.get('month')
    year = request.form.get('year')
    print(credit)
    if fname != "" and lname != "":
        if validNumber(phone):
            if address != "":
                if checkZip(zipc):
                    if state != None:
                        if checkCard(cc, sc):
                            if month != None:
                                 if year != None:
                                    u = datetime.datetime.now()
                                    if str(u.year) == year and int(month) <= int(u.month):
                                        flash("Credit card is expired")
                                    else: #PURCHASE CODE
                                        _, _, prices, conds = checkCart()
                                        total = 0
                                        for i in range(len(prices)):
                                            total += prices[i]
                                        data = cursor.execute("SELECT accountID FROM account WHERE email = ?", [session["USERNAME"]])
                                        userid = data.fetchone()[0]
                                        data = cursor.execute("SELECT credit FROM account WHERE email = ?", [session["USERNAME"]])
                                        oldcredit = data.fetchone()[0]
                                        shipping = 5.99
                                        if total >= 35:
                                            shipping = 0
                                        d = datetime.timedelta(days=7)
                                        t = u + d
                                        delivery = str(t.month) + "/" + str(t.day) + "/" + str(t.year)
                                        date = str(u.month) + "/" + str(u.day) + "/" + str(u.year)
                                        time = u.strftime("%H") + ":" + u.strftime("%M") + ":" + u.strftime("%S")
                                        newcredit = oldcredit - float(credit)
                                        cursor.execute('INSERT INTO purchase(accountID, shipping, delivery, status, date, time, fname, lname, phone, address, zip, state, creditcard, security, month, year, credit) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (userid, shipping, delivery, "Processed", date, time, fname, lname, phone, address, zipc, state, cc, sc, month, year, credit))
                                        purid = cursor.lastrowid
                                        for i in range(len(prices)):
                                            cursor.execute('INSERT INTO purchasedItem(purchaseID, conditionID, price) VALUES(?,?,?)', (purid, session["CART"][i], prices[i]))
                                            data = cursor.execute("SELECT stock FROM condition WHERE conditionID = ?", [session["CART"][i]])
                                            stock = data.fetchone()[0]
                                            stock -= 1
                                            cursor.execute('UPDATE condition SET stock = ? WHERE conditionID = ?',[stock, session["CART"][i]])
                                        cursor.execute('UPDATE account SET credit = ? WHERE accountID = ?',[newcredit, userid])
                                        connection.commit()
                                        session["CART"] = []
                                        session["CART"] = session["CART"]
                                        return redirect(url_for('success'))
                                 else:
                                    flash("Year is blank")
                            else:
                                flash("Month is blank")
                        else:
                            flash("Invalid credit card")
                    else:
                        flash("State is blank")
                else:
                    flash("Invalid zip code")
            else:
                flash("Address is blank")
        else:
            flash("Invalid phone number")
    else:
        flash("Name fields are blank")
    return redirect(url_for('checkout'))

@app.route('/success')
def success():
    if "USERNAME" in session:
        return render_template('success.htm',)
    else:
        return redirect(url_for('login'))

@app.route('/success', methods=['GET', 'POST'])
def success_post():
    return redirect(url_for('success'))

@app.route('/instructions')
def instructions():
    return render_template('instructions.htm',)

@app.route('/instructions', methods=['GET', 'POST'])
def instructions_post():
    return redirect(url_for('instructions'))