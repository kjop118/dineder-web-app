from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_msearch import Search
from flask_migrate import Migrate
import mysql.connector


mydb = mysql.connector.connect(
    host="br5qeuqmq0vt0kswckki-mysql.services.clever-cloud.com",
    database="br5qeuqmq0vt0kswckki",
    user="u9gff7om6scemu0o",
    passwd="uEkd3YF6kHfcUkrFQeMP"
)

#
# MYSQL_ADDON_HOST=br5qeuqmq0vt0kswckki-mysql.services.clever-cloud.com
# MYSQL_ADDON_DB=br5qeuqmq0vt0kswckki
# MYSQL_ADDON_USER=u9gff7om6scemu0o
# MYSQL_ADDON_PORT=3306
# MYSQL_ADDON_PASSWORD=uEkd3YF6kHfcUkrFQeMP
# MYSQL_ADDON_URI=mysql://u9gff7om6scemu0o:uEkd3YF6kHfcUkrFQeMP@br5qeuqmq0vt0kswckki-mysql.services.clever-cloud.com:3306/br5qeuqmq0vt0kswckki


print("TEST DB")
print(mydb)

mycursor = mydb.cursor()

# mycursor.execute('INSERT into users value (1,"Janusz", "Kowalski", "janusz@email.com", "haslojanusza")')
# print(mycursor.execute("SELECT * from users"))

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u9gff7om6scemu0o:uEkd3YF6kHfcUkrFQeMP@br5qeuqmq0vt0kswckki-mysql.services.clever-cloud.com:3306/br5qeuqmq0vt0kswckki'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
search = Search()
search.init_app(app)

migrate = Migrate(app, db)

from dineder import routes