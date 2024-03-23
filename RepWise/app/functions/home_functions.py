from RepWise.app import db
from datetime import datetime, timedelta
import random, string





def is_database_empty(db):
	categories_exist = bool(db['categories'].keys())
	return not categories_exist





def get_latest_values_by_category(json_data:str , user = None) -> list:
	latest_values = []
	un_agreed = []
	
	for category, values in json_data.items():
		latest_value = max(values, key=lambda x: x['timestamp'])
		latest_values.append(latest_value)
		
	if not user :
		return latest_values

	
	user_data = db['whitelist'].get(user)
	for value in latest_values:
		if value['id'] not in user_data['requirment_agreed']:
			un_agreed.append(value)
			
	#print(un_agreed, user_data['requirment_agreed'])
	return un_agreed





def time_since_last_update(latest_values) -> str:
	if not latest_values:
		return "No values available"
		
	latest_timestamp = max(value["timestamp"] for value in latest_values)
	current_time = datetime.now()
	time_difference = current_time - datetime.fromtimestamp(latest_timestamp)

	if time_difference < timedelta(seconds=60):
		return "a few seconds ago"
	elif time_difference < timedelta(minutes=60):
		minutes = int(time_difference.total_seconds() // 60)
		return f"{minutes} minutes ago"
	elif time_difference < timedelta(hours=24):
		hours = int(time_difference.total_seconds() // 3600)
		return f"{hours} hours ago"
	else:
		return datetime.fromtimestamp(latest_timestamp).strftime("%B %d, %Y %I:%M %p")




def generate_unique_uid(length=6):
	letters = string.ascii_letters
	return ''.join(random.choice(letters) for _ in range(length))


def add_user(user: str) -> None:
	if user not in db['whitelist']:
		db['whitelist'][user.lower()] = {
		       'requirment_agreed': []
	      }


def update_requirement(category: str, description: str) -> None:
	category_data = db.get('categories', {})
	if category not in category_data:
		category_data[category] = []

	descriptions = [req['description'] for req in category_data.get(category, [])]
	if description not in descriptions:
		requirement = {
			"id": generate_unique_uid(),
			"timestamp": datetime.now().timestamp(),
			"description": description,
			"category": category
		}
		category_data[category].append(requirement)
		db['categories'] = category_data
	else:
		print("Description Already Exists")


def store_values_in_db(values):
    agreed_requirments = []
    requirements_id , username = values
    user_data = db['whitelist'].get(username)


    for id in requirements_id:
        if id not in user_data['requirment_agreed']:
            db['whitelist'][username]['requirment_agreed'].append(id)
            agreed_requirments.append(id)

    return agreed_requirments






def convert_to_dict(categories_data):
	categories_dict = {}
	for category, values in categories_data.items():
		if category not in categories_dict:
			categories_dict[category] = []
		
		for value in values:
			data = {
			         "id": value["id"],
			         "timestamp": value["timestamp"],
			         "description": value["description"],
			         "category": value["category"]
			         }
			categories_dict[category].append(data)
			
	return categories_dict
			
		
			
			
			


	

