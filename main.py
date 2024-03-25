from RepWise.app import app, db





"""
I've already created functions that interact directly with the database.Instead, 
I suggest that perhaps later on, you'll create an admin page to access everything, 
including adding users, deleting users, adding categories, deleting categories, 
adding requirements, deleting requirements, and updating requirements, 
along with other functionalities. Below is the basic usage of how to add a user and update categories.
"""



#importing the required module
from RepWise.app.functions import add_user, update_requirement, delete_data_by_uuid, load_categories_from_file



filename = "file.json"
#uncomment to load requirements from json file 
#load_categories_from_file(db, filename)





# Consider this snippet from ./RepWise/app/functions/home_functions.py
# the fuction add_user() is use to add_user to the whitelist
def add_replit_username():
	username = ''

	if username:
		add_user(username)
		print("user added successfully")
	else:
	    print("Please enter a valid username.")




# Consider this snippet from ./RepWise/app/functions/home_functions.py
# the fuction update_requirement(...) is use to update requiement by category
def update_requirement_demo():

    json_file = "file.json"
    category_name = ''
    description = """  

	              """

    if category_name and description:
        update_requirement(category_name, description, db, json_file)
        print(f"Requirement added successfully for the '{category_name}' category.")
    else:
        print("Please enter a valid category name and description.")




# Consider this snippet from ./RepWise/app/functions/home_functions.py
# the fuction delete_data_by_uuid(..) is use to delete requiement by id
def delete_requirement_demo():
	json_file= "file.json"
	req_id = ""

	if req_id and json_file:
		delete_data_by_uuid(json_file, req_id)
		print(f"Requirement deleted successfully for the '{req_id}' id.")
	else:
		print("Please enter a valid id.")
		




#This are judt demo to show how to use the functions
add_replit_username()
update_requirement_demo()
delete_requirement_demo()



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

