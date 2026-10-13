from flask import Flask, render_template, request, jsonify
import sqlite3, os, re

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), "bookings.db")

HOTELS = [
    {"id":1,"name":"Palm City Villa","location":"Doha, Qatar","price":1200,"rating":4.8,"type":"Villa","guests":8,
     "image":"https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=1200&q=85",
     "desc":"A private luxury villa with spacious rooms, a pool and beautiful city views."},
    {"id":2,"name":"The Pearl Residence","location":"The Pearl, Doha","price":850,"rating":4.7,"type":"Apartment","guests":4,
     "image":"https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85",
     "desc":"Modern waterfront living close to restaurants, shopping and the marina."},
    {"id":3,"name":"West Bay Skyline","location":"West Bay, Doha","price":620,"rating":4.6,"type":"Hotel","guests":2,
     "image":"https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=85",
     "desc":"Elegant hotel rooms with skyline views, a rooftop pool and premium service."},
    {"id":4,"name":"Souq Heritage House","location":"Msheireb, Doha","price":490,"rating":4.5,"type":"Boutique","guests":3,
     "image":"https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=1200&q=85",
     "desc":"A stylish boutique stay inspired by traditional Qatari architecture."},
    {"id":5,"name":"Desert Pearl Retreat","location":"Al Wakrah, Qatar","price":760,"rating":4.7,"type":"Resort","guests":5,
     "image":"https://images.unsplash.com/photo-1540541338287-41700207dee6?auto=format&fit=crop&w=1200&q=85",
     "desc":"Relaxing resort escape with pools, gardens and family-friendly amenities."},
    {"id":6,"name":"Marina View Suites","location":"Lusail, Qatar","price":690,"rating":4.6,"type":"Suite","guests":4,
     "image":"https://images.unsplash.com/photo-1584132967334-10e028bd69f7?auto=format&fit=crop&w=1200&q=85",
     "desc":"Contemporary suites overlooking Lusail Marina with premium facilities."},
    {"id":7,"name":"Golden Dunes Lodge","location":"Mesaieed, Qatar","price":540,"rating":4.4,"type":"Lodge","guests":4,
     "image":"https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1200&q=85",
     "desc":"A peaceful desert-inspired lodge for an unforgettable weekend."},
    {"id":8,"name":"Corniche Grand","location":"Doha Corniche","price":980,"rating":4.9,"type":"Hotel","guests":2,
     "image":"https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=1200&q=85",
     "desc":"Five-star comfort near the Corniche with exceptional dining and views."}
]

def init_db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hotel_id INTEGER, name TEXT, email TEXT, checkin TEXT,
        checkout TEXT, guests INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    con.commit()
    con.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.get("/api/hotels")
def hotels():
    q = request.args.get("q","").strip().lower()
    max_price = request.args.get("max_price","").strip()
    data = HOTELS
    if q:
        data = [h for h in data if q in h["name"].lower() or q in h["location"].lower() or q in h["type"].lower()]
    if max_price.isdigit():
        data = [h for h in data if h["price"] <= int(max_price)]
    return jsonify(data)

@app.post("/api/book")
def book():
    data = request.get_json(silent=True) or {}
    required = ["hotel_id","name","email","checkin","checkout","guests"]
    if any(not data.get(k) for k in required):
        return jsonify({"ok":False,"message":"Please complete all booking fields."}), 400
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", str(data["email"])):
        return jsonify({"ok":False,"message":"Please enter a valid email address."}), 400
    con = sqlite3.connect(DB)
    cur = con.execute(
        "INSERT INTO bookings(hotel_id,name,email,checkin,checkout,guests) VALUES(?,?,?,?,?,?)",
        (data["hotel_id"], data["name"], data["email"], data["checkin"], data["checkout"], data["guests"])
    )
    con.commit()
    booking_id = cur.lastrowid
    con.close()
    return jsonify({"ok":True,"booking_id":booking_id,"message":"Booking request confirmed."})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
