from flask import Flask, request, render_template
import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index_html():
    conn = sqlite3.connect("./../airbnb_stanford.db")
    cur = conn.cursor()
    df = pd.read_sql_query("SELECT countries.country, places.place, raiting, description, quantityOfBed, amount_som, amount_dollar  FROM hotels INNER JOIN countries on hotels.id_country = countries.id INNER JOIN places on hotels.id_place = places.id", conn)
    countryUn = cur.execute("""SELECT country FROM countries""")
    countryUn = countryUn.fetchall()
    placeUn = cur.execute("""SELECT place from places""")
    placeUn = placeUn.fetchall()
    conn.close()
    
    return render_template('index.html', hotels=df.to_html(header=True), countryUn=countryUn, placeUn=placeUn, lenCountry = len(countryUn), lenPlace = len(placeUn), selectedPlace="", selectedCountry="", selectedRaiting="", selectedQuantityOfBed="", selectedAmountDollar="")

@app.route("/", methods=['POST'])
def index_post():
    selectedPlace = int(request.form.get("name_place"))+1
    selectedCountry = int(request.form.get("name_country"))+1
    selectedRaiting = int(request.form.get("name_raiting"))
    selectedQuantityOfBed = int(request.form.get("name_quantityOfBed"))
    selectedAmountDollar = request.form.get("name_dollar")
    conn = sqlite3.connect("./../airbnb_stanford.db")
    cur = conn.cursor()
    conditions = []
    params = []
    query = "SELECT countries.country, places.place, raiting, description, quantityOfBed, amount_som, amount_dollar  FROM hotels INNER JOIN countries on hotels.id_country = countries.id INNER JOIN places on hotels.id_place = places.id"
    if selectedCountry != 0:
        conditions.append("countries.id = ?")
        params.append(selectedCountry)
    if selectedPlace != 0:
        conditions.append("places.id = ?")
        params.append(selectedPlace)
    if selectedRaiting != 0:
        conditions.append("hotels.raiting >= ?")
        params.append(selectedRaiting)
    if selectedQuantityOfBed != -1:
        conditions.append("hotels.quantityOfBed = ?")
        params.append(selectedQuantityOfBed)
    if selectedAmountDollar != "":
        conditions.append("hotels.amount_dollar >= ?")
        params.append(int(selectedAmountDollar))
    if conditions:
        res_condition = f"{query} WHERE {' AND '.join(conditions)}"
    else:
        res_condition = query
    df = pd.read_sql_query(res_condition, conn, params=params)
    countryUn = cur.execute("""SELECT country FROM countries""")
    countryUn = countryUn.fetchall()
    placeUn = cur.execute("""SELECT place from places""")
    placeUn = placeUn.fetchall()
    return render_template('index.html', hotels=df.to_html(header=True), countryUn = countryUn, placeUn=placeUn, lenCountry = len(countryUn), lenPlace = len(placeUn), selectedPlace=selectedPlace, selectedCountry=selectedCountry, selectedRaiting=selectedRaiting, selectedQuantityOfBed=selectedQuantityOfBed, selectedAmountDollar=selectedAmountDollar )

if "__main__" == __name__:
    app.run(debug = True)