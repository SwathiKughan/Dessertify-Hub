from flask import Flask, render_template, request, url_for,redirect
import psycopg2

app = Flask(__name__)


hostname = 'localhost'
database = 'RecipeDB'
username = 'postgres'
pwd = 'SQL@160601'
port_id = 5432


@app.route("/",methods=["GET","POST"])
def home():
    return render_template("/home.html")

@app.route('/about')
def about():
    return render_template('/about.html')

@app.route('/cookies')
def cookies():
    return render_template('/Cookies.html')

@app.route('/brownies')
def brownie():
    return render_template('/Brownies.html')

@app.route('/bread')
def bread():
    return render_template('/Bread&Bun.html')

@app.route('/donut')
def donut():
    return render_template('/Donuts.html')

@app.route('/cheesecake')
def cheese():
    return render_template('/Cheesecake.html')

@app.route('/tiramisu')
def tiramisu():
    return render_template('/Tiramisu.html')

@app.route('/signup')
def signup():
    return render_template('/signup.html')

@app.route('/login')
def login():
    return render_template('/login.html')

@app.route('/user')
def user():
    return render_template('/user.html')


@app.route('/add_recipe')
def index():
    return render_template('/add_recipe.html')


@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    try:
        conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id)
        cur = conn.cursor()

        recipe_name = request.form['recipe_name']
        ingredients = request.form['ingredients']
        directions = request.form['directions']

        insert_script = 'INSERT INTO RecipeDB(Recipe_Name, Ingredients, Directions) VALUES (%s, %s, %s)'
        insert_value = (recipe_name, ingredients, directions)
        cur.execute(insert_script, insert_value)
        conn.commit()

        return 'Recipe added successfully!'
    except Exception as e:
        return str(e)
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()


def main():
    return render_template("/home.html")

if __name__ == '__main__':
    app.run(debug=True)



'''@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            conn = psycopg2.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id)
            cur = conn.cursor()

            username = request.form['username']
            password = request.form['password']

            insert_script = 'INSERT INTO Users(username, password) VALUES (%s, %s)'
            insert_value = (username, password)  # You should hash the password for security
            cur.execute(insert_script, insert_value)
            conn.commit()

            return redirect('/login')
        except Exception as e:
            return str(e)
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
    return render_template('/signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            conn = psycopg2.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id)
            cur = conn.cursor()

            username = request.form['username']
            password = request.form['password']

            query = 'SELECT * FROM Users WHERE username = %s AND password = %s'
            cur.execute(query, (username, password))  # Again, password should be hashed and compared
            user = cur.fetchone()

            if user:
                session['username'] = username
                return redirect('/add_recipe')
            else:
                return "Invalid username or password"
        except Exception as e:
            return str(e)
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
    return render_template('/login.html')
'''

'''from flask import Flask, render_template, request, redirect, session
import psycopg2
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

hostname = 'localhost'
database = 'RecipeDB'
username = 'postgres'
pwd = 'SQL@160601'
port_id = 5432


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("/home.html")


@app.route('/about')
def about():
    return render_template('/about.html')


@app.route('/cookies')
def cookies():
    return render_template('/Cookies.html')


@app.route('/brownies')
def brownie():
    return render_template('/Brownies.html')


@app.route('/bread')
def bread():
    return render_template('/Bread&Bun.html')


@app.route('/donut')
def donut():
    return render_template('/Donuts.html')


@app.route('/cheesecake')
def cheese():
    return render_template('/Cheesecake.html')


@app.route('/tiramisu')
def tiramisu():
    return render_template('/Tiramisu.html')


DATABASE = 'new.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS swa (username TEXT UNIQUE, password TEXT)")

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        try:
            with get_db_connection() as conn:
                conn.execute("INSERT INTO swa (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
        except sqlite3.IntegrityError:
            return "User already exists!", 400
        return redirect("/login")
    return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM swa WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            return "Login successful!", 200
        else:
            return "Invalid credentials", 401
    return render_template('login.html')



@app.route('/user')
def user():
    return render_template('/user.html')


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        try:
            conn = psycopg2.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id)
            cur = conn.cursor()

            recipe_name = request.form['recipe_name']
            ingredients = request.form['ingredients']
            directions = request.form['directions']

            insert_script = 'INSERT INTO Recipes(recipe_name, ingredients, directions) VALUES (%s, %s, %s)'
            insert_value = (recipe_name, ingredients, directions)
            cur.execute(insert_script, insert_value)
            conn.commit()

            return redirect('/')
        except Exception as e:
            return str(e)
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
    return render_template('/add_recipe.html')


if __name__ == '__main__':
    app.run(debug=True)
 '''
 
'''from flask import Flask, render_template, request, redirect, session
import psycopg2
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# PostgreSQL connection 
hostname = 'localhost'
database = 'RecipeDB'
username = 'postgres'
pwd = 'SQL@160601'
port_id = 5432

# SQLite database 
DATABASE = 'new.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS swa1 (username TEXT UNIQUE, password TEXT)")

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        try:
            with get_db_connection() as conn:
                conn.execute("INSERT INTO swa1 (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return "User already exists!", 400
    return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM swa1 WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect('/add_recipe')
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'username' not in session:
        return redirect('/signup')

    if request.method == 'POST':
        try:
            conn = psycopg2.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id)
            cur = conn.cursor()

            recipe_name = request.form['recipe_name']
            ingredients = request.form['ingredients']
            directions = request.form['directions']

            insert_script = 'INSERT INTO recipes(recipe_name, ingredients, directions) VALUES (%s, %s, %s)'
            cur.execute(insert_script, (recipe_name, ingredients, directions))
            conn.commit()
            return redirect('/')
        except Exception as e:
            return str(e)
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
    return render_template('/add_recipe.html')

if __name__ == '__main__':
    app.run(debug=True)
'''