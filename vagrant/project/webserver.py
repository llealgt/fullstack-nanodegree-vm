from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header("Content-type","text/html")
				self.end_headers()
				
				output = ""
				output+= "<html><body>Hello!"
				output += "<form method='POST' enctype='multipart/form-data' action = '/hello'>"
				output += "<h2>what would you like me to say?</h2><input name = 'message' type = 'text'>"
				output += "<input type='submit' value = 'Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print(output)
				return
			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header("Content-type","text/html")
				self.end_headers()
				
				output = ""
				output+= "<html><body>&#161Hola <a href = '/hello'>Back to hello</a>"
				output += "<form method='POST' enctype='multipart/form-data' action = '/hello'>"
				output += "<h2>what would you like me to say?</h2><input name = 'message' type = 'text'>"
				output += "<input type='submit' value = 'Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print(output)
				return
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header("Content-type","text/html")
				self.end_headers()
				
				output = "<html><body>"
				restaurants = session.query(Restaurant).all()
				
				for restaurant in restaurants:
					output+=restaurant.name+"<br>"
					output+='<a href="#">Edit</a><br>'
					output+= '<a href="#">Delete</a><br>'
					output += '<br>'
					
				output += "</body></html>"
				
				print(output)
				self.wfile.write(output)
				
				return
			
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header("Content-type","text/html")
				self.end_headers()
				
				output = "<html></body><h1>New Restaurant</h1>"
				output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/new'>"
				output += "<input name = 'newRestaurantName' type='text' placeholder = 'New Restaurant Name'>"
				output += "<input type = 'submit' value = 'Create'>"
				
				output += "</form></body></html>"
				
				print(output)
				self.wfile.write(output)
				
				return
				
				
		except IOError:
			self.send_error(404,"File not found %s"%self.path)
			
	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype,parameters_dict = cgi.parse_header(
					self.headers.getheader('content-type'))
					
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile,parameters_dict)
					new_restaurant_name = fields.get('newRestaurantName')[0]
					
					new_restaurant = Restaurant(name = new_restaurant_name)
					session.add(new_restaurant)
					session.commit()
					
					self.send_response(301)
					self.send_header('Content-type','text-html')
					self.send_header('Location','/restaurants')
					self.end_headers()
					
					return;
					
			self.send_response(301)
			self.end_headers()
			
			ctype, pdict = cgi.parse_header(self.headers.getheader("content-type"))
			if ctype == "multipart/form-data":
				fields = cgi.parse_multipart(self.rfile,pdict)
				messagecontent = fields.get("message")
				
			output = ""
			output += "<html><body>"
			output += "<h2>Okay, how about this: </h2>"
			output += "<h1> %s </h1>"%messagecontent[0]
			
			output += "<form method='POST' enctype='multipart/form-data' action = '/hello'>"
			output += "<h2>what would you like me to say?</h2><input name = 'message' type = 'text'>"
			output += "<input type='submit' value = 'Submit'></form>"
			output += "</body></html>"
			self.wfile.write(output)
			print(output)
		
		except Exception as e:
			print("exception",e)
			
def main():
	try:
		port = 8080
		server = HTTPServer(("",port),webserverHandler)
		print("Web server running on port %s"%port)
		server.serve_forever()
	
	except KeyboardInterrupt:
		print("Ctlr+C entered, stopping web server...")
		server.socket.close()
	
if __name__ == "__main__":
	main()
