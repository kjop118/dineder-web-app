from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_msearch import Search
from flask_migrate import Migrate
import mysql.connector


mydb = mysql.connector.connect(
    host="bcfetlsp1q3mijpte2pm-mysql.services.clever-cloud.com",
    database="bcfetlsp1q3mijpte2pm",
    user="u7m0erwsyzw2ihys",
    passwd="aqJf3vLng5qBlVweb1xC"
)

print("TEST DB")
print(mydb)

mycursor = mydb.cursor()
mycursor.execute("SHOW tables")
for db in mycursor:
    print(db)


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u7m0erwsyzw2ihys:aqJf3vLng5qBlVweb1xC@bcfetlsp1q3mijpte2pm-mysql.services.clever-cloud.com:3306/bcfetlsp1q3mijpte2pm'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
search = Search()
search.init_app(app)

migrate = Migrate(app, db)

from dineder import routes