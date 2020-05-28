from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.register import UserRegister
from resources.items import Item, AllItems
from resources.stores import Store, AllStores

app = Flask(__name__)
app.secret_key = 'x'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(Item, '/stores/<string:store_name>/item=<string:item_name>')  # Adds the Api resource(class Item) to specified URL
api.add_resource(Store, '/stores/<string:store_name>')
api.add_resource(AllItems, '/stores/<string:store_name>/items')
api.add_resource(AllStores, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000)
