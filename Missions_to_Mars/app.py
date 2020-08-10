from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Using PyMongo to establish Mongo connection
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # find one record of data from the mongo database
    data = mongo.db.collection.find_one()

    # return the template and data
    return render_template("index.html", mars = data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and saving results
    mars_data = scrape_mars.scrape_info()

    # Updating the mongo database
    mongo.db.collection.update({}, mars_data, upsert = True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)
