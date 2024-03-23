from RepWise.app import app, db





"""
I couldn't add the JSON file to this project because 
I've already created functions that interact directly with the database.Instead, 
I suggest that perhaps later on, you'll create an admin page to access everything, 
including adding users, deleting users, adding categories, deleting categories, 
adding requirements, deleting requirements, and updating requirements, 
along with other functionalities. Below is the basic usage of how to add a user and update categories.

"""



# Consider this snippet from ./RepWise/app/functions/home_functions.py
# the fuction is use to add user to the whitelist and update requirements
from RepWise.app.functions import add_user, update_requirement


username = ''

category_name = ""
description = """    """

if username:
	add_user(username)
	print("user added successfully")

if category_name and description:
	update_requirement(category_name, description)
	print("Database updated successfully")

















if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)
