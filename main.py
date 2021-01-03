from flask import Flask, Response, request, render_template, redirect, url_for, flash
from bson.objectid import ObjectId
import pymongo
import json


app = Flask(__name__)

###################################################
#MONGO DATABASE CONNECTION
try:
    mongo = pymongo.MongoClient(
        host="localhost", 
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.parroquia
    mongo.server_info()
except:
    print("ERROR - cannot connect to DB")
###################################################


###################################################
#SESSION SETINGS
app.secret_key = "mysecretkey"
###################################################

@app.route("/")
def index():
    return render_template('landing.html')

@app.route("/add")
def add():
    return render_template('add.html')

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/difuntos")
def difuntos():
    data = list(db.difuntos.find())
    for difunto in data:
        difunto["_id"] = str(difunto["_id"])
    return render_template('index.html', difuntos = data)

@app.route("/difuntos", methods=["POST"])
def crear_difunto():

    try:
        difunto = {
            "rut":request.form["rut"], 
            "nombre":request.form["nombre"],
            "f_defuncion":request.form["f_defuncion"],
            "f_nacimiento":request.form["f_nacimiento"],
            "sepultura":request.form["sepultura"],
            }
        db.difuntos.insert_one(difunto)
        flash("Registro añadido con exito")
        return redirect( url_for("add") )
    except Exception as ex:
        print(ex)

@app.route("/delete/<id>")
def borrar_difunto(id):
    try:
        dbResponse = db.difuntos.delete_one(
            {"_id":ObjectId(id)}
        )
        if(dbResponse.deleted_count == 1):
            return redirect( url_for("difuntos") )
        else:
            return redirect( url_for("difuntos") )
            
    except Exception as ex:
        print(ex)

@app.route("/edit/<id>")
def edit_difunto(id):
    try:
        data = list(db.difuntos.find({"_id":ObjectId(id)}) )
        print(data)
        return render_template('edit.html', difunto = data[0])
    except Exception as ex:
        print(ex)

@app.route("/update/<id>", methods=["POST"])
def update_difunto(id):
    try:
        dbResponse = db.difuntos.update_one(
            {"_id":ObjectId(id)},
            {"$set": {
                "rut":request.form["rut"],
                "nombre":request.form["nombre"],
                "f_defuncion":request.form["f_defuncion"],
                "f_nacimiento":request.form["f_nacimiento"],
                "sepultura":request.form["sepultura"]}}
        )
        if(dbResponse.modified_count == 1):
            return redirect( url_for("difuntos") )
        else:
            return redirect( url_for("difuntos") )
    except Exception as ex:
        print(ex)

@app.route("/search/rut" ,methods=["POST"])
def search_rut():
    param = request.form["rut_search"]
    data = list(db.difuntos.find({"rut": param}) )
    flash("ok")
    return render_template('search.html', resultados = data)

@app.route("/search/name" ,methods=["POST"])
def search_name():
    param = request.form["name_search"]
    data = list(db.difuntos.find({"nombre": param}) )
    flash("ok")
    return render_template('search.html', resultados = data)


### # ### # ### # ### # ### # ### # ### # ### # ###
### #                   API                   # ###
### # ### # ### # ### # ### # ### # ### # ### # ###
@app.route("/api", methods=["GET"])
def get_difuntos():
    try:
        data = list(db.difuntos.find())
        for difunto in data:
            difunto["_id"] = str(difunto["_id"])
        return Response(
            response = json.dumps(data),
            status = 200,
            mimetype = "application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({"message":"Cannot read difuntos"}),
            status = 500,
            mimetype = "application/json"
        )

@app.route("/api", methods=["POST"])
def create_difunto():
    try:
        difunto = {
            "rut":request.form["rut"], 
            "nombre":request.form["nombre"],
            "f_defuncion":request.form["f_defuncion"],
            "f_nacimiento":request.form["f_nacimiento"],
            "sepultura":request.form["sepultura"],
            }
        dbResponse = db.difuntos.insert_one(difunto)
        return Response(
            response = json.dumps( 
                {"message":"difunto creado", 
                "id":f"{dbResponse.inserted_id}"}
            ),
            status = 200,
            mimetype = "application/json"
        )
    except Exception as ex:
        print(ex)

@app.route("/api/<id>", methods=["PATCH"])
def update(id):
    try:
        dbResponse = db.difuntos.update_one(
            {"_id":ObjectId(id)},
            {"$set": {
                "rut":request.form["rut"],
                "nombre":request.form["nombre"],
                "f_defuncion":request.form["f_defuncion"],
                "f_nacimiento":request.form["f_nacimiento"],
                "sepultura":request.form["sepultura"]}}
        )
        if(dbResponse.modified_count == 1):
            return Response(
                response = json.dumps({"message":"User updated"}),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps({"Nothing to update"}),
                status = 200,
                mimetype = "application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({"message":"Cannot update user"}),
            status = 500,
            mimetype = "application/json"
        )

@app.route("/api/<id>", methods=["DELETE"])
def delete_difunto(id):
    try:
        dbResponse = db.difuntos.delete_one(
            {"_id":ObjectId(id)}
        )
        if(dbResponse.deleted_count == 1):
            return Response(
                response = json.dumps( 
                    {"message":"difunto deleted", "id" :f"{id}"}
                ),
                status = 200,
                mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps( 
                    {"message":"difunto not found"}
                ),
                status = 200,
                mimetype = "application/json"
            )
    except Exception as ex:
        print(ex)

### # ### # ### # ### # ### # ### # ### # ### # ###

if __name__ == "__main__":
    app.run(port=80, debug=True)