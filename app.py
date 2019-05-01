# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars2

# create instance of Flask app
app = Flask(__name__)

# connection between mongo and Flask
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsDB"
mongo = PyMongo(app) 

# set up the route and the webscraping function
@app.route("/")
def home():
    mars = mongo.db.marsDB.find_one()
    print(mars)
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.marsDB
    mars_scrape = scrape_mars2.scrape()
   # Need to connect to mongo DB and push info in to mars to db
    mars.update({}, mars_scrape, upsert=True)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)