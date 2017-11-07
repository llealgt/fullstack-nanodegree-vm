from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem
from flask import Flask,render_template , request, redirect , url_for,flash,jsonify

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
	output = render_template('menu.html' , restaurant = restaurant, items = items)
	
	return output
	
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	
	return jsonify(MenuItems = [i.serialize for i in items])
	
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id,menu_id):
	menu_item = session.query(MenuItem).filter_by(id = menu_id).one()
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	
	return jsonify(MenuItem  = menu_item.serialize)
	
@app.route("/restaurant/<int:restaurant_id>/new/" ,methods = ['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == "POST":
		newItem = MenuItem(name = request.form["item_name"],restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New menu item created")
		
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html',restaurant_id = restaurant_id)
	
@app.route("/restaurant/<int:restaurant_id>/<int:menu_id>/edit/",methods = ["GET","POST"])
def editMenuItem(restaurant_id,menu_id):
	edited_item = session.query(MenuItem).filter_by(id = menu_id).one()
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	
	if request.method == "POST":
		new_name = request.form["new_name"]
		
		if new_name:
			edited_item.name = new_name
			session.add(edited_item)
			session.commit()
			
			flash("Item edited")
			
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
	else:
		return render_template('editmenuitem.html',restaurant = restaurant, item = edited_item)
	
@app.route("/restaurant/<int:restaurant_id>/<int:menu_id>/delete/" , methods = ["GET","POST"])	
def deleteMenuItem(restaurant_id,menu_id):
	deleted_item = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == "POST":
		session.delete(deleted_item)
		session.commit()
		flash("Item succesfully deleted")
		
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
	else:
		return render_template('deletemenuitem.html',item = deleted_item)
	
if __name__ == "__main__":
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = "0.0.0.0", port = 5000)
	
