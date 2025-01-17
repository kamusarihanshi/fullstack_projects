from flask import Blueprint
from flask_restful import Api,Resource,reqparse
from models import db,Products
from flask_cors import CORS
from datetime import datetime
product_bp=Blueprint('product',__name__,url_prefix='/product')
product_api=Api(product_bp)

CORS(product_bp)

product_parser=reqparse.RequestParser()
product_parser.add_argument('name',type=str,required=True,help='Name is required')
product_parser.add_argument('price',type=float,required=True,help='Price is required')
product_parser.add_argument('description',type=str,required=True,help='Description is required')
product_parser.add_argument('stock',type=int,required=True,help='stock is required')
product_parser.add_argument('image_url',type=str,required=True,help='Image URL is required') 
product_parser.add_argument('category_id',type=int,required=True,help='Category ID is required')
product_parser.add_argument('created_at',type=datetime,required=True)
product_parser.add_argument('updated_at',type=datetime,required=True)




class ProductResource(Resource):
    def get(self,id):
        product=Products.query.get_or_404(id)
        return {'id':product.id,'name':product.name,'price':product.price,'description':product.description,'stock':product.stock,'image_url':product.image_url,'category_id':product.category_id,'created_at':product.created_at,'updated':product}
    
    def put(self,id):
        data=product_parser.parse_args()
        product=Products.query.get_or_404(id)
        product.name=data['name']
        product.price=data['price']
        product.description=data['description']
        product.stock=data['stock']
        product.image_url=data['image_url']
        product.category_id=data['category_id']
        product.created_at=data['created_at']
        product.updated_at=data['updated_at']
        db.session.commit()
        return{'message':'product updated successfully'}
    
    def delete(self,id):
        product=Products.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return{'message':'product deleted successfully'}
    

product_api.add_resource(ProductResource,'/<int:id>')

class ProductList(Resource):
    def get(self):
        products=Products.query.all()
        return [{'id':product.id,'name':product.name,'price':product.price,'description':product.description,'stock':product.stock,'image_url':product.image_url,'category_id':product.category_id,'created_at':product.created_at,'updated':product} for product in products]
    
    def post(self):
        data=product_parser.parse_args()
        new_product=Products(name=data['name'],price=data['price'],description=data['description'],stock=data['stock'],image_url=data['image_url'],category_id=data['category_id'],created_at=data['created_at'],updated_at=data['updated_at'])
        db.session.add(new_product)
        db.session.commit()
        return{'message':'product added successfully'},201
    
    def delete(self):
        products=Products.query.all()
        db.session.delete(products)
        db.session.commit()
        return{'message':'All products deleted successfully'}


product_api.add_resource(ProductList,'/list_products')