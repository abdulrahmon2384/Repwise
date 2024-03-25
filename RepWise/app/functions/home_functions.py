from RepWise.app import db
from datetime import datetime, timedelta
import random, string, uuid


def is_database_empty(db):
    tables_exist = db.get('categories').keys()
    print(db.get('categories').keys())
    return True if len(tables_exist) == 0 else False


def get_latest_values_by_category(json_data: str, user=None) -> list:
	latest_values = []
	un_agreed = []

	for category, values in json_data.items():
		latest_value = max(values, key=lambda x: x['timestamp'])
		latest_values.append(latest_value)

	if not user:
		return latest_values

	user_data = db['whitelist'].get(user)
	if user_data is None:
		return []

	agreed_requirements = user_data.get('requirment_agreed', [])
	for value in latest_values:
		if value['id'] not in agreed_requirements:
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

	if username in db.get('whitelist', {}):
		print("User already exists in the database.")
		return

	# Add user to the whitelist
	db.setdefault('whitelist',
	              {}).update({username: {
	                  'requirment_agreed': []
	              }})


def update_requirement(category: str, description: str, db: dict) -> None:

	if category not in db:
		db[category] = []

	descriptions = [req['description'] for req in db.get(category, [])]
	if description not in descriptions:
		requirement = {
		    "id": str(uuid.uuid4()),
		    "timestamp": datetime.now().timestamp(),
		    "description": description,
		    "category": category
		}
		db[category].append(requirement)
		print("Requirement added successfully.")
	else:
		print("Description Already Exists")


def store_values_in_db(values):
	requirements_id, username = values

	user_data = db['whitelist'].get(username)
	if user_data:
		agreed_requirments = []

		for req_id in requirements_id:
			if req_id not in user_data['requirment_agreed']:
				db['whitelist'][username]['requirment_agreed'].append(id)
				agreed_requirments.append(id)
		return agreed_requirments
	else:
		return []


def convert_to_dict(categories_data):
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
