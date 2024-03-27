from RepWise.app import db
from datetime import datetime, timedelta
import random, string, json


def load_categories_from_file(db, filename):
	try:
		with open(filename, 'r') as file:
			data = json.load(file)
			db["categories"] = data

	except FileNotFoundError:
		print("Categories file not found.")

	except json.JSONDecodeError:
		print("Error decoding JSON in categories file.")

	except Exception as e:
		print(f"An error occurred: {str(e)}")


def initialize_database(db):
	if len(db.keys()) == 0:
		db['Users'] = dict()
		db['categories'] = dict()


def time_since_last_update(db) -> str:
	if not db.get("categories"):
		return "No values available"

	timestamps = [
	    item.get("timestamp") for items in db["categories"].values()
	    for item in items
	]
	latest_timestamp = max(timestamps)
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
		return datetime.fromtimestamp(latest_timestamp).strftime(
		    "%B %d, %Y %I:%M %p")


def generate_unique_uid(length=6):
	letters = string.ascii_letters
	return ''.join(random.choice(letters) for _ in range(length))


def add_user(user: str) -> None:
	if not isinstance(user, str):
		print("Username must be a non-empty string.")
		quit()

	username = user.strip().lower()
	if username in db.get('Users', {}):
		print("User already exists in the database.")
		return

	db.setdefault('Users', {}).update({username: {'requirment_agreed': []}})


def add_data_to_categories(json_name, requirements):
	try:
		with open(json_name, 'r+') as file:
			data = json.load(file)

			category = requirements['category']
			if category in data:
				data[category].append(requirements)
			else:
				data[category] = [requirements]

			file.seek(0)
			json.dump(data, file, indent=4)
			file.truncate()

	except FileNotFoundError:
		print("JSON file not found.")
	except json.JSONDecodeError:
		print("Error decoding JSON in the file.")
	except Exception as e:
		print(f"An error occurred: {str(e)}")


def update_requirement(category: str,
                       description: str,
                       db: dict,
                       json_name: str = "file.json") -> None:
	if category not in db:
		db[category] = []

	descriptions = [req['description'] for req in db.get(category, [])]
	if description not in descriptions:
		requirement = {
		    "id": generate_unique_uid(length=6),
		    "timestamp": datetime.now().timestamp(),
		    "description": description,
		    "category": category
		}
		add_data_to_categories(json_name, requirement)
		db[category].append(requirement)
		print("Requirement added successfully.")

	else:
		print("Description Already Exists")


def append_requirment_agreed(values):
	requirements_id, username = values

	user_data = db['Users'].get(username)
	if user_data:
		agreed_requirments = []

		for req_id in requirements_id:
			if req_id not in user_data['requirment_agreed']:
				db['Users'][username]['requirment_agreed'].append(req_id)
		return True
	else:
		return False


def convert_to_dict(categories_data):
	#check if DB Isempty
	empty = [
	    True if len(all_categories) == 0 else False
	    for all_categories in categories_data.values()
	]
	if all(empty):
		return {"eMPTy": "Database Empty"}

	categories_dict = {}
	for category, values in categories_data.items():
		if category not in categories_dict:
			categories_dict[category] = []
		for value in values:
			data = {
			    "id": value.get("id"),
			    "timestamp": value.get("timestamp"),
			    "description": value.get("description"),
			    "category": value.get("category")
			}
			categories_dict[category].append(data)
	return categories_dict


def isUserCompletionStatus(username):
	database = db.get("categories")
	if database is None:
		return False

	user_data = db['Users'].get(username)
	requirements_agreed = user_data.get('requirment_agreed', {})

	if requirements_agreed:
		for category, category_data in db["categories"].items():
			unagreed_requirements = [
			    item for item in category_data
			    if item.get('id') not in requirements_agreed
			]
			if len(unagreed_requirements) > 0:
				return False
		else:
			return True
	return False
