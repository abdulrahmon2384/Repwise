


`
#importing the required module
from RepWise.app.functions import update_requirement, delete_data_by_uuid, load_categories_from_file
`


filename = "file.json"
#uncomment to load requirements from json file 
load_categories_from_file(db, filename)




`

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
`




# Consider this snippet from ./RepWise/app/functions/home_functions.py
# the fuction delete_data_by_uuid(..) is use to delete requiement by id






#This are judt demo to show how to use the functions
update_requirement_demo()
delete_requirement_demo()
