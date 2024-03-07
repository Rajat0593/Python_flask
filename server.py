from flask import Flask, make_response
from flask import request
app = Flask(__name__)
data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]

@app.route("/data")
def get_data():
        try:
                if data and len(data) > 0:
                        return {"message": f"Data of length {len(data)} found"}
                else:
                        return {"message": "Data is empty"}, 500
        except NameError:
                return {"message":"Data not found"}, 404

#Create a method called name_search with the @app.route decorator. This method should be called when a client requests for the /name_search URL. 
#The method will not accept any parameter, however, will look for the argument q in the incoming request URL. This argument holds the first_name the client is looking for. 
#The method returns:
#Person information with a status of HTTP 400 if the first_name is found in the data
#Message of Invalid input parameter with a status of HTTP 422 if the argument q is missing from the request
#Message of Person not found with a status code of HTTP 404 if the person is not found in the data

@app.route("/name_search")
def name_search():
        query = request.args.get("q")
        if not query:
                return {"message":"Invalid input parameter"},422
        for person in data:
                if query.lower() in person["first_name"].lower():
                        return person
        return ({"message":"Person not found"}, 404)

#Add the @app.get() decorator for the /count URL. Define the count function that simply returns the number of items in the data list.

@app.route("/count")
def count():
    try:
        return {"data count": len(data)}, 200
    except NameError:
        return {"message": "data not defined"}, 500

#Create a new endpoint for http://localhost/person/unique_identifier. The method should be named find_by_uuid. 
#It should take an argument of type UUID and return the person JSON if found. If the person is not found, the method should return a 404 with a message of person not found. 
#Finally, the client (curl) should only be able to call this method by passing a valid UUID type id.
                  
@app.route("/person/<uuid:id>")      
def find_by_uuid(id):      
    for person in data:
        if person["id"] == str(id):
            return person
    return {"message": "person not found"}, 404

#Create a new endpoint for DELETE http://localhost/person/unique_identifier. The method should be named delete_by_uuid.
#It should take in an argument of type UUID and delete the person from the data list with that id. 
#If the person is not found, the method should return a 404 with a message of person not found. Finally, the client (curl) should call this method by passing a valid UUID type id.

@app.route("/person/<uuid:id>", methods=['DELETE'])
def delete_by_uuid(id):                                              
    for person in data:            
        if person["id"] == str(id):
            data.remove(person)          
            return {"message":f"{id}"}, 200                  
    return {"message": "person not found"}, 404   

#Create a method called add_by_uuid with the @app.route decorator. This method should be called when a client requests with the POST method for the /person URL.
#The method will not accept any parameter but will grab the person details from the JSON body of the POST request. 
#The method returns:
#person id if the person was successfully added to data; HTTP 200 code
#message of Invalid input parameter with a status of HTTP 422 if the json body is missing

@app.route("/person", methods=['POST'])
        def add_by_uuid():
                new_person = request.json
                if not new_person:
                        return {"message":"Invalid input parameter"},422
                try:
                        data.append(new_person)
                except NameError:
                        return {"message":"data not defined"}, 500
                return {"message": f"{new_person['id']}"},200

#Create a method called api_not_found with the @app.errorhandler decorator. 
#This method will return a message of API not found with an HTTP status code of 404 whenever the client requests a URL that does not lead to any endpoints defined by the server.
@app.errorhandler(404)
def api_not_found(error):
    return {"message": "API not found"}, 404
