from RepWise.app import app, db





"""
I couldn't add the JSON file to this project because 
I've already created functions that interact directly with the database.Instead, 
I suggest that perhaps later on, you'll create an admin page to access everything, 
including adding users, deleting users, adding categories, deleting categories, 
adding requirements, deleting requirements, and updating requirements, 
along with other functionalities. Below is the basic usage of how to add a user and update categories.

"""



#importing the required modules
from RepWise.app.functions import add_user, update_requirement


# Consider this snippet from ./RepWise/app/functions/home_functions.py
# the fuction is use to add user to the whitelist
def add_replit_username():
	username = input("Enter Replit Username: ").strip()

	if username:
		add_user(username)
		print("user added successfully")
	else:
	    print("Please enter a valid username.")




# Consider this snippet from ./RepWise/app/functions/home_functions.py
# the fuction is use to update or add new requiement and description 
def update_requirement_demo():
    category_name = input("Enter the category name (e.g., 'Finance', 'Marketing', 'HR'): ").strip()
    description = input(f"Enter the description for the requirement in the '{category_name}' category: ").strip()

    if category_name and description:
        update_requirement(category_name, description, db)
        print(f"Requirement added successfully for the '{category_name}' category.")
    else:
        print("Please enter a valid category name and description.")
















if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)




	
	#Uncomment to add a user and update categories
	add_replit_username()
	#update_requirement_demo()