from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from database.conn import DatabaseConnection


class Item(Resource):  # This class will add, modify, delete or return an item of a specific store

    parser = reqparse.RequestParser()  # creating parser object, will be useful at 'post' and 'put' methods
    parser.add_argument('price', type=float, required=True, help='this field cannot be left blank')  # so the request can only accept 'price' info

    @classmethod
    def checking(cls, store_name, item_name):
        with DatabaseConnection('./database/data.db') as cursor:
            search_items_query = "SELECT * FROM items WHERE store_name=?"
            result = cursor.execute(search_items_query, (store_name,))
            rows = result.fetchall()
        for row in rows:
            if row[1] == item_name:
                return True
        return False

    @jwt_required
    def get(self, store_name, item_name):
        check = self.checking(store_name, item_name)
        if check:  # if the item and the store name exist
            get_item_query = "SELECT * FROM items WHERE store_name=? AND item=?"
            try:
                with DatabaseConnection('./database/data.db') as cursor:
                    result = cursor.execute(get_item_query, (store_name, item_name))  # get the item that matches the method's arguments
                    row = result.fetchone()
            except:
                return {'message': 'error occurred while getting the item'}, 500
            else:
                return {'name': row[1], 'price': row[2]}
        else:
            return {'message': 'item or store name not found'}, 404

    @jwt_required
    def post(self, store_name, item_name):
        check = self.checking(store_name, item_name)
        if not check:  # if the check failed it means that the item doesnt exist so lets create one
            price = self.parser.parse_args()['price']  # uses the parser object that belongs to the 'Item' class(this class) to parse the request data
            insert_query = "INSERT INTO items VALUES (?, ?, ?)"
            try:
                with DatabaseConnection('./database/data.db') as cursor:
                    cursor.execute(insert_query, (store_name, item_name, price))
            except:
                return {'message': 'error occurred while creating item'}, 500
            else:
                return {'message': 'item added'}, 201
        else:
            return {'message': 'item or store name already exists'}, 400

    @jwt_required
    def put(self, store_name, item_name):
        check = self.checking(store_name, item_name)
        if check:
            new_price = self.parser.parse_args()['price']
            update_query = "UPDATE items SET price=? WHERE store_name=? AND item=?"  # update the item that matches the method's arguments
            try:
                with DatabaseConnection('./database/data.db') as cursor:
                    cursor.execute(update_query, (new_price, store_name, item_name))
            except:
                return {'message': 'error occurred while updating the item'}, 500
            else:
                return {'message': 'item modified successfully'}, 201
        else:
            return {'message': 'item or store name not found'}, 404

    @jwt_required
    def delete(self, store_name, item_name):
        check = self.checking(store_name, item_name)
        if check:
            delete_item_query = "DELETE FROM items WHERE store_name=? AND item=?"  # delete the item that matches the method's arguments
            try:
                with DatabaseConnection('./database/data.db') as cursor:
                    cursor.execute(delete_item_query, (store_name, item_name))
            except:
                return {'message': 'error occurred while deleting the item'}, 500
            else:
                return {'message': 'Item deleted'}
        else:
            return {'message': 'item or store name not found'}, 404


class AllItems(Resource):  # This class will return all items of a store
    @staticmethod
    @jwt_required
    def get(store_name):
        with DatabaseConnection('./database/data.db') as cursor:
            all_items_query = "SELECT * FROM items WHERE store_name=?"
            result = cursor.execute(all_items_query, (store_name,))
            rows = result.fetchall()
        if rows:
            items = [{'name': row[1], 'price': row[2]} for row in rows]
            return {'items': items}
        else:
            return {'message': 'store name not found'}
