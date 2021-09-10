import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from redis import Redis
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from security import authenticate, identity


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #local
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://db-data:/var/lib/postgresql/data')

#app.config['SQLALCHEMY_DATABASE_URI'] = \
#    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
#        user=DBUSER,
#        passwd=DBPASS,
#        host=DBHOST,
#        port=DBPORT,
#        db=DBNAME)
print(1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://christian:coolpassword@db:5432/testdb')
#conn_str = "postgresql+psycopg2://user:coolpassword@postgres_db:5432/api"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    print(os.environ.get('DATABASE_URL'))
    print(os.environ.get('SQLALCHEMY_DATABASE_URI'))
    db.create_all()

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    print(0)
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)