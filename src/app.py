from flask import Flask,request,Response,jsonify
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json

app= Flask(__name__)
app.config['MONGO_URI']='mongodb+srv://nicolas17197:U3LOaMIzSyZDvPch@cluster0.xyuut.gcp.mongodb.net/Canje?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route("/products", methods=['POST'])
def create_product():
    titulo=request.json['titulo']
    categoria=request.json['categoria']
    descripcion=request.json['descripcion']
    canjeo=request.json['canjeo']
    mongo.db.Products.insert(
        {
            "titulo":titulo,
            "categoria":categoria, 
            "descripcion": descripcion,
            "canjeo":canjeo
        })
    return "Hola, mundo!" 

@app.route('/products', methods=['GET'])
def get_products():
    products = mongo.db.Products.find()
    response = json_util.dumps(products)
    return Response(response, mimetype="application/json")

@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = mongo.db.Products.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(product)
    return Response(response, mimetype="application/json")

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    mongo.db.Products.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Product' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route("/products/<_id>", methods=['PUT'])
def update_product(_id):
    titulo=request.json['titulo']
    categoria=request.json['categoria']
    descripcion=request.json['descripcion']
    canjeo=request.json['canjeo']
    mongo.db.Products.update_one(
        {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
        {'$set':{
            "titulo":titulo,
            "categoria":categoria, 
            "descripcion": descripcion,
            "canjeo":canjeo
        }})
    response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
    response.status_code = 200
    return response


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response 


    
if __name__ == "__main__":
    app.run(debug=True)