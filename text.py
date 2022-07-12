from flask import Flask,render_template,request,url_for,session, jsonify
from flask_wtf import FlaskForm
from flask_pymongo import PyMongo
from wtforms import StringField
from wtforms.validators import InputRequired,Length,AnyOf,DataRequired,Email
from pymongo import MongoClient
import pprint

import json

client = MongoClient("mongodb://developer:tnt_developer@dev0-shard-00-00.4zcxu.mongodb.net:27017,dev0-shard-00-01.4zcxu.mongodb.net:27017,dev0-shard-00-02.4zcxu.mongodb.net:27017/petnt_dev2?replicaSet=atlas-tpci1n-shard-0&authSource=admin&retryWrites=true&w=majority&ssl=true")
mydb=client["petnt_dev2"]
mycol=mydb["transportPermit"]

app=Flask(__name__)
app.config["SECRET_KEY"]='TRAIL'

class contactform(FlaskForm):
    sourceEntityId=StringField('sourceEntityId',validators=[InputRequired('plz enter the sourceEntityId ')])

@app.route('/',methods=["POST","GET"])
def index():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def form():
    form = contactform()
    if request.method=='POST':
        k = form.sourceEntityId.data
        #c=mydb.transportPermit.find_one({"sourceEntityId": k},{"_id":0,"consignment.productDetails.brandName":1,"consignment.productDetails.brandCode":1})
        x=[]
        c = mydb.transportPermit.aggregate([
            {
                '$match': {
                    'sourceEntityId': k
                }
            },
            {
                "$unwind":
                    {
                        "path": "$consignment",
                        "includeArrayIndex": "arrayIndex"
                    }

            },
            {
                '$project': {
                    "_id":0,
                    'consignment.productDetails.approvedQty': 1,
                    'consignment.productDetails.shipmentQty': 1
                }
            }])
        for doc in c:
            x.append(doc)

            #print(x)
            #print(type(x))

        return jsonify(x)

    return render_template('check.html', form=form)


if __name__=='__main__':
    app.run(debug=True)
