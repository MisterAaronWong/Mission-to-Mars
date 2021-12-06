# we'll use Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for
# we'll use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo
# use the scraping code, we will convert from Jupyter notebook to Python
import scraping

app = Flask(__name__)

# tell Python how to connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
# tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# the URI we'll be using to connect our app to Mongo.
# This URI is saying that the app can reach Mongo through our localhost server,
# using port 27017, using a database named "mars_app"
mongo = PyMongo(app)

# The code we create next will set up our Flask routes:
# one for the main HTML page everyone will view when visiting the web app,
# and one to actually scrape new data using the code we've written
# This function is what links our visual representation of our work, our web app, to the code that powers it.

# define the route for the HTML page
@app.route("/") # tells Flask what to display when we're looking at the home page,
    # index.html (index.html is the default HTML file that we'll use to display the content we've scraped
    # when we visit our web app's HTML page, we will see the home page
def index():
   mars = mongo.db.mars.find_one() # uses PyMongo to find the "mars" collection in our database,
    # which we will create when we convert our Jupyter scraping code to Python Script
    # We will also assign that path to themars variable for use later
   return render_template("index.html", mars=mars) # tells Flask to return an HTML template using an index.html file
    # We'll create this file after we build the Flask routes.
    # , mars=mars) tells Python to use the "mars" collection in MongoDB.

# Our next function will set up our scraping route.
# This route will be the "button" of the web application,
# the one that will scrape updated data when we tell it to from the homepage of our web app
# It'll be tied to a button that will run the code when it's clicked.

@app.route("/scrape") # defines the route that Flask will be using
    # This route, “/scrape”, will run the function that we create just beneath it
    # The next lines allow us to access the database,
    # scrape new data using our scraping.py script,
    # update the database, and return a message when successful
def scrape(): # First, we define it 
   mars = mongo.db.mars # assign a new variable that points to our Mongo database
   mars_data = scraping.scrape_all() # create a new variable to hold the newly scraped data: mars_data = scraping.scrape_all()
    # we're referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook
   mars.update({}, mars_data, upsert=True) # Now that we've gathered new data, we need to update the database using .update()
    # We're inserting data, so first we'll need to add an empty JSON object with {} in place of the query_parameter
    # Next, we'll use the data we have stored in mars_data
    # Finally, the option we'll include is upsert=True
    # This indicates to Mongo to create a new document if one doesn't already exist
    # and new data will always be saved (even if we haven't already created a document for it).
   return redirect('/', code=302) # add a redirect after successfully scraping the data: return redirect('/', code=302)
    # This will navigate our page back to / where we can see the updated content

# The final bit of code we need for Flask is to tell it to run
if __name__ == "__main__":
   app.run()