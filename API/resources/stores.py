from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from database.conn import DatabaseConnection


class Store(Resource):  # This class will add, modify, delete or return a store
    @classmethod
    @jwt_required
    def checking(cls, store_name):  # checks if the store exists, used at post put and delete
        with DatabaseConnection('./database/data.db') as cursor:
            search_store_query = "SELECT * FROM items WHERE store_name=?"
            result = cursor.execute(search_store_query, (store_name,))

            if result.fetchall():
                return True
            else:
                return False

    @staticmethod
    @jwt_required
    def get(store_name):
        with DatabaseConnection('./database/data.db') as cursor:
            search_store_query = "SELECT * FROM items WHERE store_name=?"
            result = cursor.execute(search_store_query, (store_name,))
            rows = result.fetchall()

        if rows:
            store = {'name': store_name, 'items': [{'name': row[1], 'price': row[2]} for row in rows if row[1] != 'NULL']}
            return {'store': store}, 200
        else:
            return {'message': 'store name not found'}, 404

    @jwt_required
    def post(self, store_name):
        check = self.checking(store_name)
        if not check:
            new_store_query = "INSERT INTO items VALUES (?, 'NULL', 'NULL')"
            try:
                with DatabaseConnection('./database/data.db') as cursor:
                    cursor.execute(new_store_query, (store_name,))
            except:
                return {'message': 'error while adding new store'}, 500
            else:
                return {'message': 'store added'}, 201
        else:
            return {'message': 'store name already exists'}, 401

    @jwt_required
    def put(self, store_name):
        check = self.checking(store_name)
        if check:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True, help='this field cannot be left blank')
            data = parser.parse_args()
            new_name = data['name']

            new_name_query = "UPDATE items SET store_name=? WHERE store_name=?"
            try:
                with DatabaseConnection('./database/data.db') as cursor:
                    cursor.execute(new_name_query,  (new_name, store_name))
            except:
                return {"message": "error while changing the store's name"}, 500
            else:
                return {'message': 'store name modified'}, 201
        else:
            return {'message': 'store name not found'}, 404

    @jwt_required
    def delete(self, store_name):
        check = self.checking(store_name)
        if check:
            delete_store_query = "DELETE FROM items WHERE store_name=?"
            try:
                with DatabaseConnection('./database/data.db') as cursor:
                    cursor.execute(delete_store_query, (store_name,))
            except:
                return {'message': 'error occurred while deleting the item'}, 500
            else:
                return {'message': 'Store deleted'}
        else:
            return {'message': 'store name not found'}, 404


class AllStores(Resource):  # This class will return all stores
    @staticmethod
    @jwt_required
    def get():
        with DatabaseConnection('./database/data.db') as cursor:
            result = cursor.execute("SELECT * FROM items")
            rows = result.fetchall()

            if rows:
                known_names = []
                for row in rows:  # append all the stores names that are available to the known_names list
                    store_name = row[0]
                    if store_name not in known_names:
                        known_names.append(store_name)

                stores = []
                for name in known_names:
                    get_store_query = "SELECT * FROM items WHERE store_name=?"
                    result = cursor.execute(get_store_query, (name,))
                    rows = result.fetchall()
                    store_name = rows[0][0]
                    stores.append({'name': store_name, 'items': None})

                    all_items = [{'name': row[1], 'price': row[2]} for row in rows]

                    for store in stores:
                        if store['name'] == store_name:
                            store['items'] = all_items

                return {'stores': stores}
            else:
                return {'message': 'stores not found'}, 404
