from data_vine.functions import createDelta, getCurrentState
from data_vine.json_a import json_to_avro
from settings import *
import json
from datetime import datetime


db = SQLAlchemy(app)

def formatdb(name):
    if name=='order':
        rv = [{'Field':'id', 'Type':'integer', 'Null':'NO'}, {'Field':'userid', 'Type':'integer', 'Null':'NO'}, 
        {'Field':'status', 'Type':'char', 'Null':'NO'}, {'Field':'subtotal', 'Type':'float', 'Null':'NO'}, 
        {'Field':'discount', 'Type':'float', 'Null':'NO'}, {'Field':'tax', 'Type':'float','Null':'NO'}, 
        {'Field':'grandtotal', 'Type':'float', 'Null':'NO'}, {'Field':'description', 'Type':'char', 'Null':'NO'}, 
        {'Field':'createdat', 'Type':'char', 'Null':'NO'}, {'Field':'updatedat', 'Type':'char', 'Null':'NO'}]
    elif name=='product':
        rv = [{'Field':'productid', 'Type':'integer', 'Null':'NO'}, {'Field':'productname', 'Type':'char', 'Null':'NO'}, 
        {'Field':'price', 'Type':'float', 'Null':'NO'}, {'Field':'quantity', 'Type':'float', 'Null':'NO'}, 
        {'Field':'description', 'Type':'char', 'Null':'NO'}, {'Field':'supplierid', 'Type':'integer', 'Null':'NO'}, 
        {'Field':'createdat', 'Type':'char', 'Null':'NO'}, {'Field':'updatedat', 'Type':'char', 'Null':'NO'}]
    elif name=='user':
        rv = [{'Field':'userid', 'Type':'integer', 'Null':'NO'}, {'Field':'username', 'Type':'char', 'Null':'NO'}, 
        {'Field':'contactno', 'Type':'bigint', 'Null':'NO'}, {'Field':'email', 'Type':'char', 'Null':'NO'}, 
        {'Field':'createdat', 'Type':'char', 'Null':'NO'}, {'Field':'updatedat', 'Type':'char', 'Null':'NO'}]
    elif name=='supplier':
        rv = [{'Field':'supplierid', 'Type':'integer', 'Null':'NO'}, {'Field':'suppliername', 'Type':'char', 'Null':'NO'}, 
        {'Field':'description', 'Type':'char', 'Null':'NO'}, {'Field':'contactno', 'Type':'integer', 'Null':'NO'}, 
        {'Field':'email', 'Type':'char', 'Null':'NO'}, {'Field':'createdat', 'Type':'char', 'Null':'NO'}, 
        {'Field':'updatedat', 'Type':'char', 'Null':'NO'}]
    return rv

class ordertable(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    status = db.Column (db.String(30), nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    grandtotal = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    createdat = db.Column(db.String, nullable=False)
    updatedat= db.Column(db.String, nullable=False)

    def json(self):
        return{'id': self.id, 'userid': self.userid, 'status': self.status, 'subtotal': self.subtotal, 
        'discount': self.discount, 'tax': self.tax, 'grandtotal': self.grandtotal,'description': self.description, 'createdat': self.createdat, 
        'updatedat': self.updatedat}

    def add_order(_userid, _status, _subtotal, _discount, _tax, _grandtotal, _description): #change
        ddmm = datetime.now()
        ts = datetime.timestamp(ddmm) #timestamp
        dt_string=ddmm.strftime("%Y%m%d_%H%M%S") #YYYY MM DD HH MM SS in String for DB
        new_order=ordertable(userid=_userid, status=_status, subtotal=_subtotal, discount=_discount, tax=_tax, 
        grandtotal=_grandtotal, description=_description, createdat=dt_string, updatedat=dt_string)
        oldstate = [ordertable.json(order) for order in ordertable.query.all()]
        #print(oldstate)
        db.session.add(new_order)
        db.session.commit()
        newstate = [ordertable.json(order) for order in ordertable.query.all()]
        # print(newstate)
        createDelta('order', oldstate, newstate, 'POST', dt_string, 'id')

    def get_all_orders():
        return [ordertable.json(order) for order in ordertable.query.all()]

    def get_order(_id):
        return [ordertable.json(ordertable.query.filter_by(id=_id).first())]

    def update_order(_id, _userid, _status, _subtotal, _discount, _tax, _grandtotal, _description):
        ddmm = datetime.now()
        ts = datetime.timestamp(ddmm) #timestamp
        dt_string=ddmm.strftime("%Y%m%d_%H%M%S") #YYYY MM DD HH MM SS in String for DB
        order_to_update=ordertable.query.filter_by(id=_id).first()
        order_to_update.userid=_userid
        order_to_update.status=_status
        order_to_update.subtotal=_subtotal
        order_to_update.discount=_discount
        order_to_update.tax=_tax
        order_to_update.grandtotal=_grandtotal
        order_to_update.description=_description
        order_to_update.updatedat=dt_string
        oldstate = [ordertable.json(order) for order in ordertable.query.all()]
        db.session.commit()
        newstate = [ordertable.json(order) for order in ordertable.query.all()]
        createDelta('order', oldstate, newstate, 'PUT', dt_string, 'id', _id)

    def delete_order(_id):
        ddmm = datetime.now()
        ts = datetime.timestamp(ddmm)
        dt_string=ddmm.strftime("%Y%m%d_%H%M%S")
        oldstate = [ordertable.json(order) for order in ordertable.query.all()]
        ordertable.query.filter_by(id=_id).delete()
        db.session.commit()
        newstate = [ordertable.json(order) for order in ordertable.query.all()]
        createDelta('order', oldstate, newstate, 'DELETE', dt_string, 'id', _id)

class producttable(db.Model):

    __tablename__ = 'product'
    productid= db.Column(db.Integer, primary_key=True)
    productname= db.Column(db.String(40), nullable=False)
    price= db.Column(db.Float, nullable=False)
    quantity= db.Column(db.Integer, nullable=False)
    description= db.Column(db.String(40), nullable=False)
    supplierid = db.Column(db.Integer, nullable=False)
    createdat = db.Column(db.String, nullable=False)
    updatedat = db.Column(db.String, nullable=False)
    def json(self):
        return{'productid': self.productid, 'productname': self.productname, 'price': self.price, 'quantity': self.quantity, 
        'description': self.description, 'supplierid': self.supplierid, 'createdat': self.createdat, 'updatedat': self.updatedat}


    def add_product(_productname, _price, _quantity, _description, _supplierid):
        ddmm = datetime.now()
        ts = datetime.timestamp(ddmm) #timestamp
        dt_string=ddmm.strftime("%Y%m%d_%H%M%S") #YYYY MM DD HH MM SS in String for DB
        new_product=producttable(productname=_productname, price=_price, 
        quantity=_quantity, description=_description, supplierid=_supplierid, createdat=dt_string, updatedat=dt_string)
        oldstate = [producttable.json(product) for product in producttable.query.all()]
        db.session.add(new_product)
        db.session.commit()
        newstate = [producttable.json(product) for product in producttable.query.all()]
        createDelta('product', oldstate, newstate, 'POST', dt_string, 'productid')

    def get_all_products():
        return [producttable.json(product) for product in producttable.query.all()]

    def get_product(_productid):
        return [producttable.json(producttable.query.filter_by(productid=_productid).first())]

    def update_product(_productid, _productname, _price, _quantity, _description, _supplierid):

        ddmm = datetime.now()
        ts = datetime.timestamp(ddmm) #timestamp
        dt_string=ddmm.strftime("%Y%m%d_%H%M%S") #YYYY MM DD HH MM SS in String for DB
        product_to_update=producttable.query.filter_by(productid=_productid).first()
        product_to_update.productname=_productname
        product_to_update.price=_price
        product_to_update.quantity=_quantity
        product_to_update.description=_description
        product_to_update.supplierid=_supplierid
        product_to_update.updatedat= dt_string
        oldstate = [producttable.json(product) for product in producttable.query.all()]
        db.session.commit()
        newstate = [producttable.json(product) for product in producttable.query.all()]
        createDelta('product', oldstate, newstate, 'PUT', dt_string, 'productid', _productid)

    def delete_product(_productid):
        oldstate = [producttable.json(product) for product in producttable.query.all()]
        ddmm = datetime.now()
        ts = datetime.timestamp(ddmm)
        dt_string=ddmm.strftime("%Y%m%d_%H%M%S")
        producttable.query.filter_by(productid=_productid).delete()
        db.session.commit()
        newstate = [producttable.json(product) for product in producttable.query.all()]
        createDelta('product', oldstate, newstate, 'DELETE', dt_string, 'productid', _productid)

class suppliertable(db.Model):
    __tablename__ = 'supplier'
    supplierid= db.Column(db.Integer, primary_key=True)
    suppliername= db.Column(db.String(40), nullable=False)
    description= db.Column(db.String(40), nullable=False)
    contactno= db.Column(db.BigInteger, nullable=False)
    email= db.Column(db.String(40), nullable=False)
    createdat = db.Column(db.String, nullable=False)
    updatedat = db.Column(db.String, nullable=False)


    def json(self):
        return{'supplierid': self.supplierid, 'suppliername': self.suppliername, 
        'description': self.description, 'contactno': self.contactno, 'email': self.email, 'createdat': self.createdat, 'updatedat': self.updatedat}

    def add_supplier(_suppliername, _description, _contactno, _email):
        ddmm = datetime.now()
        ts = datetime.timestamp(ddmm) #timestamp
        dt_string=ddmm.strftime("%Y%m%d_%H%M%S") #YYYY MM DD HH MM SS in String for DB
        new_supplier=suppliertable(suppliername=_suppliername, description=_description, contactno=_contactno, email=_email, createdat=dt_string, updatedat=dt_string)
        oldstate = [suppliertable.json(supplier) for supplier in suppliertable.query.all()]
        db.session.add(new_supplier)
        db.session.commit()
        newstate = [suppliertable.json(supplier) for supplier in suppliertable.query.all()]
        createDelta('supplier', oldstate, newstate, 'POST', dt_string, 'supplierid')

    def get_all_suppliers():    
        return [suppliertable.json(supplier) for supplier in suppliertable.query.all()]

    def get_supplier(_supplierid):
        return [suppliertable.json(suppliertable.query.filter_by(supplierid=_supplierid).first())]

    def update_supplier(_supplierid, _suppliername, _description, _contactno, _email):
        ddmm = datetime.now()
        ts = datetime.timestamp(ddmm) #timestamp
        dt_string=ddmm.strftime("%Y%m%d_%H%M%S") #YYYY MM DD HH MM SS in String for DB
        supplier_to_update=suppliertable.query.filter_by(supplierid=_supplierid).first()
        supplier_to_update.suppliername=_suppliername
        supplier_to_update.description= _description
        supplier_to_update.contactno= _contactno
        supplier_to_update.email= _email
        supplier_to_update.updatedat=dt_string
        oldstate = [suppliertable.json(supplier) for supplier in suppliertable.query.all()]
        db.session.commit()
        newstate = [suppliertable.json(supplier) for supplier in suppliertable.query.all()]
        createDelta('supplier', oldstate, newstate, 'PUT', dt_string, 'supplierid', _supplierid)

    def delete_supplier(_supplierid):
        oldstate = [suppliertable.json(supplier) for supplier in suppliertable.query.all()]
        ddmm = datetime.now()
        ts = datetime.timestamp(ddmm)
        dt_string=ddmm.strftime("%Y%m%d_%H%M%S")
        suppliertable.query.filter_by(supplierid=_supplierid).delete()
        db.session.commit()
        newstate = [suppliertable.json(supplier) for supplier in suppliertable.query.all()]
        createDelta('supplier', oldstate, newstate, 'DELETE', dt_string, 'supplierid', _supplierid)
        


    
class usertable(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    contactno = db.Column(db.BigInteger, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    createdat = db.Column(db.String, nullable=False)
    updatedat = db.Column(db.String, nullable=False)

    def json(self):
        return{'userid': self.userid, 'username': self.username, 
        'contactno': self.contactno, 'email': self.email, 'createdat': self.createdat, 'updatedat': self.updatedat}

    def add_user(_username, _contactno, _email):
        ddmm = datetime.now()
        ts = datetime.timestamp(ddmm) #timestamp
        dt_string=ddmm.strftime("%Y%m%d_%H%M%S") #YYYY MM DD HH MM SS in String for DB
        new_user=usertable(username=_username, contactno=_contactno, email=_email, createdat=dt_string, updatedat= dt_string)
        oldstate = [usertable.json(user) for user in usertable.query.all()]
        db.session.add(new_user)
        db.session.commit()
        newstate = [usertable.json(user) for user in usertable.query.all()]
        createDelta('user', oldstate, newstate, 'POST', dt_string, 'userid')

    def get_all_users():
        return [usertable.json(user) for user in usertable.query.all()]

    def get_user(_userid):
        return [usertable.json(usertable.query.filter_by(userid=_userid).first())]

    def update_user(_userid, _username, _contactno, _email):
        ddmm = datetime.now()
        ts = datetime.timestamp(ddmm) #timestamp
        dt_string=ddmm.strftime("%Y%m%d_%H%M%S") #YYYY MM DD HH MM SS in String for DB
        user_to_update=usertable.query.filter_by(userid=_userid).first()
        user_to_update.userid=_userid
        user_to_update.username=_username
        user_to_update.contactno=_contactno
        user_to_update.email=_email
        user_to_update.updatedat= dt_string
        oldstate = [usertable.json(user) for user in usertable.query.all()]
        db.session.commit()
        newstate = [usertable.json(user) for user in usertable.query.all()]
        createDelta('user', oldstate, newstate, 'PUT', dt_string, 'userid', _userid)

    def delete_user(_userid):
        oldstate = [usertable.json(user) for user in usertable.query.all()]
        ddmm = datetime.now()
        ts = datetime.timestamp(ddmm)
        dt_string=ddmm.strftime("%Y%m%d_%H%M%S")
        usertable.query.filter_by(userid=_userid).delete()
        db.session.commit()
        newstate = [usertable.json(user) for user in usertable.query.all()]
        createDelta('user', oldstate, newstate, 'DELETE', dt_string, 'userid', _userid)