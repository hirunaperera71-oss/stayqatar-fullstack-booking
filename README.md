# StayQatar — Advanced Full-Stack Travel Website

This is an upgraded version of the original StayQatar project. It keeps the original Flask project structure and adds working Stays + Experiences browsing, richer search/filter/sort, booking requests, favourites, newsletter signup and additional content sections.

## Technology
- HTML5, CSS3, JavaScript (ES6+)
- Python 3 + Flask
- REST-style JSON API
- SQLite database
- Responsive desktop/mobile layout

## Features
- Hero image carousel
- Search Qatar stays by name, destination or accommodation type
- Filter by Hotels, Villas, Apartments, Resorts and Boutique stays
- Filter by guest capacity and maximum price
- Sort by recommendation, rating or price
- Stays detail dialog with amenities and booking request form
- Experiences catalogue with Adventure, Culture, Water and Food filters
- Booking requests stored in SQLite with validation and reference numbers
- Favourites stored in browser localStorage
- Newsletter signup stored in SQLite
- Travel journal, About/benefits section and FAQ
- Responsive mobile navigation
- GitHub-ready folder structure

## Run on Windows
1. Extract the ZIP.
2. Open Command Prompt in the extracted project folder.
3. Run `python -m venv venv`
4. Run `venv\\Scripts\\activate`
5. Run `pip install -r requirements.txt`
6. Run `python app.py`
7. Open `http://127.0.0.1:5000`

The database is created automatically as `bookings.db`.

## Important demo notes
This is a portfolio project, not a live travel agency integration. Listings/prices are sample data. Booking requests are stored locally and do not reserve real hotels, send emails, or process payments. Images/fonts require an internet connection. Before public production deployment, add authentication, CSRF protection, rate limiting, secure production configuration and real provider/payment integrations.

## Suggested GitHub repository
`stayqatar-fullstack-booking`
