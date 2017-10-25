from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem
from flask import Flask

app = Flask(__name__)

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route("/")
@app.route("/restaurants/")
def restaurants():
	restaurants = session.query(Restaurant).all()
	output  =""
	
	for restaurant in restaurants:
		output += str(restaurant.id)+"</br>"
		output += restaurant.name +"</br>"
		output += "</br>"
		
	return output 

@app.route("/restaurants/<int:restaurant_id>/")
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	output = ""
	
	for item in items:
		output += item.name+"</br>"
		output += item.price + "</br>"
		output += item.description  + "</br>"
		output += "</br>"
		
	return output
	
@app.route("/restaurant/<int:restaurant_id>/new/")
def newMenuItem(restaurant_id):
	return "page to create a new menu item"
	
@app.route("/restaurant/<int:restaurant_id>/<int:menu_id>/edit/")
def editMenuItem(restaurant_id,menu_id):
	return "page to edit a  menu item"
	
@app.route("/restaurant/<int:restaurant_id>/<int:menu_id>/delete/")	
def deleteMenuItem(restaurant_id,menu_id):
	return "page to delete a  menu item"
	
if __name__ == "__main__":
	app.debug = True
	app.run(host = "0.0.0.0", port = 5000)
	
