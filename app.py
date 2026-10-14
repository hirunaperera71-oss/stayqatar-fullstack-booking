from flask import Flask, render_template, request, jsonify
import sqlite3, os, re, secrets
from datetime import datetime

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
DB = os.path.join(os.path.dirname(__file__), "bookings.db")

STAYS = [
 {"id":1,"name":"Palm City Villa","location":"Doha, Qatar","price":1200,"rating":4.8,"type":"Villa","guests":8,"bedrooms":4,"tag":"Guest favourite","amenities":["Private pool","Sea view","Wi-Fi","Kitchen"],"image":"https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=1200&q=85","desc":"A private luxury villa with spacious rooms, a pool and beautiful city views."},
 {"id":2,"name":"The Pearl Residence","location":"The Pearl, Doha","price":850,"rating":4.7,"type":"Apartment","guests":4,"bedrooms":2,"tag":"Waterfront","amenities":["Marina view","Gym","Wi-Fi","Parking"],"image":"https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85","desc":"Modern waterfront living close to restaurants, shopping and the marina."},
 {"id":3,"name":"West Bay Skyline","location":"West Bay, Doha","price":620,"rating":4.6,"type":"Hotel","guests":2,"bedrooms":1,"tag":"City escape","amenities":["Rooftop pool","Restaurant","Wi-Fi","Gym"],"image":"https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=85","desc":"A contemporary city hotel with skyline views and thoughtful guest service."},
 {"id":4,"name":"Msheireb Heritage Stay","location":"Msheireb, Doha","price":520,"rating":4.6,"type":"Boutique","guests":3,"bedrooms":1,"tag":"Cultural pick","amenities":["Courtyard","Breakfast","Wi-Fi","Walkable area"],"image":"https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=1200&q=85","desc":"A boutique stay blending local character with calm interiors and easy access to museums."},
 {"id":5,"name":"Al Wakrah Garden Resort","location":"Al Wakrah, Qatar","price":690,"rating":4.5,"type":"Resort","guests":5,"bedrooms":2,"tag":"Family friendly","amenities":["Garden","Kids pool","Wi-Fi","Restaurant"],"image":"https://images.unsplash.com/photo-1540541338287-41700207dee6?auto=format&fit=crop&w=1200&q=85","desc":"A laid-back garden resort with room for families and easy access to the coast."},
 {"id":6,"name":"Marina View Suites","location":"Lusail, Qatar","price":710,"rating":4.7,"type":"Suite","guests":4,"bedrooms":2,"tag":"Modern favourite","amenities":["Marina view","Balcony","Wi-Fi","Parking"],"image":"https://images.unsplash.com/photo-1584132967334-10e028bd69f7?auto=format&fit=crop&w=1200&q=85","desc":"Contemporary suites overlooking Lusail Marina with premium facilities."},
 {"id":7,"name":"Golden Dunes Lodge","location":"Mesaieed, Qatar","price":540,"rating":4.4,"type":"Lodge","guests":4,"bedrooms":2,"tag":"Desert escape","amenities":["Desert views","Pool","Restaurant","Parking"],"image":"https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1200&q=85","desc":"A peaceful desert-inspired lodge for an unforgettable weekend."},
 {"id":8,"name":"Corniche Grand","location":"Doha Corniche","price":980,"rating":4.9,"type":"Hotel","guests":2,"bedrooms":1,"tag":"Top rated","amenities":["Sea view","Spa","Restaurant","Wi-Fi"],"image":"https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=1200&q=85","desc":"Five-star comfort near the Corniche with exceptional dining and views."}
]
EXPERIENCES = [
 {"id":101,"name":"Desert Safari & Inland Sea","location":"Mesaieed","category":"Adventure","duration":"6 hours","price":350,"rating":4.9,"image":"https://images.unsplash.com/photo-1509316785289-025f5b846b35?auto=format&fit=crop&w=1000&q=85","desc":"Cross golden dunes with a local guide and take in the dramatic Inland Sea landscape."},
 {"id":102,"name":"Doha Heritage Walk","location":"Msheireb & Souq Waqif","category":"Culture","duration":"3 hours","price":120,"rating":4.8,"image":"https://images.unsplash.com/photo-1518684079-3c830d090?auto=format&fit=crop&w=1000&q=85","desc":"Explore traditional markets, historic streets and stories of Qatar's cultural heritage."},
 {"id":103,"name":"Sunset Dhow Cruise","location":"Doha Corniche","category":"Water","duration":"2 hours","price":180,"rating":4.7,"image":"https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1000&q=85","desc":"See Doha's skyline from the water aboard a traditional-style dhow at sunset."},
 {"id":104,"name":"Qatari Food Discovery","location":"Doha","category":"Food","duration":"3 hours","price":220,"rating":4.8,"image":"https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1000&q=85","desc":"Taste regional favourites and discover the flavours and stories behind local cuisine."},
 {"id":105,"name":"Coastal Kayak Morning","location":"Al Thakhira","category":"Adventure","duration":"2 hours","price":160,"rating":4.6,"image":"https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1000&q=85","desc":"Paddle calm coastal waters and enjoy a peaceful morning out in nature."},
 {"id":106,"name":"Museum & Architecture Tour","location":"Doha","category":"Culture","duration":"4 hours","price":260,"rating":4.9,"image":"https://images.unsplash.com/photo-1565060169194-19fabf63012b?auto=format&fit=crop&w=1000&q=85","desc":"A guided introduction to the city's architecture, museums and contemporary design."}
]

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS bookings(
          id INTEGER PRIMARY KEY AUTOINCREMENT, reference TEXT UNIQUE,
          item_type TEXT NOT NULL, item_id INTEGER NOT NULL, item_name TEXT NOT NULL,
          name TEXT NOT NULL, email TEXT NOT NULL, checkin TEXT NOT NULL,
          checkout TEXT, guests INTEGER NOT NULL, total REAL NOT NULL,
          status TEXT NOT NULL DEFAULT 'Request received',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        con.execute("""CREATE TABLE IF NOT EXISTS newsletter(
          id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

@app.route("/")
def home():
    return render_template("index.html")

@app.get("/api/stays")
def get_stays():
    q = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "all")
    max_price = request.args.get("max_price", "")
    guests = request.args.get("guests", "")
    sort = request.args.get("sort", "recommended")
    items = STAYS[:]
    if q:
        items = [x for x in items if q in (x["name"]+" "+x["location"]+" "+x["type"]).lower()]
    if category != "all":
        items = [x for x in items if x["type"].lower() == category.lower()]
    if max_price.isdigit():
        items = [x for x in items if x["price"] <= int(max_price)]
    if guests.isdigit():
        items = [x for x in items if x["guests"] >= int(guests)]
    if sort == "price-low": items.sort(key=lambda x: x["price"])
    elif sort == "price-high": items.sort(key=lambda x: x["price"], reverse=True)
    elif sort == "rating": items.sort(key=lambda x: x["rating"], reverse=True)
    return jsonify(items)

@app.get("/api/experiences")
def get_experiences():
    q = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "all")
    items = EXPERIENCES[:]
    if q:
        items = [x for x in items if q in (x["name"]+" "+x["location"]+" "+x["category"]).lower()]
    if category != "all":
        items = [x for x in items if x["category"].lower() == category.lower()]
    return jsonify(items)

@app.post("/api/book")
def book():
    data = request.get_json(silent=True) or {}
    required = ["item_type", "item_id", "name", "email", "checkin", "guests"]
    if any(str(data.get(k, "")).strip() == "" for k in required):
        return jsonify(ok=False, message="Please complete all required fields."), 400
    email = str(data["email"]).strip()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify(ok=False, message="Please enter a valid email address."), 400
    item_type = data["item_type"]
    pool = STAYS if item_type == "stay" else EXPERIENCES if item_type == "experience" else []
    try:
        item = next((x for x in pool if x["id"] == int(data["item_id"])), None)
        guests = int(data["guests"])
    except (ValueError, TypeError):
        item, guests = None, 0
    if not item:
        return jsonify(ok=False, message="The selected item could not be found."), 404
    if guests < 1:
        return jsonify(ok=False, message="Guest count must be at least one."), 400
    checkin, checkout = data["checkin"], data.get("checkout", "")
    units = 1
    if item_type == "stay":
        if guests > item["guests"]:
            return jsonify(ok=False, message=f"This stay allows up to {item['guests']} guests."), 400
        try:
            start = datetime.strptime(checkin, "%Y-%m-%d")
            end = datetime.strptime(checkout, "%Y-%m-%d")
            units = (end-start).days
            if units < 1:
                return jsonify(ok=False, message="Check-out must be after check-in."), 400
        except (ValueError, TypeError):
            return jsonify(ok=False, message="Choose valid check-in and check-out dates."), 400
    total = item["price"] * units if item_type == "stay" else item["price"] * guests
    reference = "SQ" + datetime.now().strftime("%y%m%d") + secrets.token_hex(3).upper()
    with db() as con:
        con.execute("""INSERT INTO bookings(reference,item_type,item_id,item_name,name,email,checkin,checkout,guests,total)
          VALUES(?,?,?,?,?,?,?,?,?,?)""",
          (reference,item_type,item["id"],item["name"],str(data["name"]).strip(),email,checkin,checkout,guests,total))
    return jsonify(ok=True, reference=reference, total=total, message="Your booking request has been saved.")

@app.post("/api/newsletter")
def newsletter():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify(ok=False, message="Please enter a valid email address."), 400
    try:
        with db() as con:
            con.execute("INSERT INTO newsletter(email) VALUES(?)", (email,))
    except sqlite3.IntegrityError:
        return jsonify(ok=True, message="You are already subscribed. Thank you!")
    return jsonify(ok=True, message="Thanks! You are on the travel inspiration list.")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
