import requests

def is_available(session):
	return session['capacity'] > 0

def get_forty_five_plus_data(session):
	return session['age_limit'] == 45

def get_eighteen_plus_data(session):
	return session['age_limit'] == 18

def get_session_info(center, session):
	return {
		"name": center["name"],
		"date": session["date"],
		"capacity": session["available_capacity"],
		"age_limit": session["min_age_limit"]
	}

def get_relevant_data(data):
	for center in data['centers']:
		for session in center['sessions']:
			yield get_session_info(center, session)

def get_state_id(state_name):
	url = "https://cdn-api.co-vin.in/api/v2/admin/location/states/"
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
	}
	resp_state = requests.get(url, headers=headers)
	data = resp_state.json()
	for state in data['states']:
		if state['state_name'] == state_name:
			return (state['state_id'])


def get_district_id(dis_name, sta_id):
	url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/" + str(sta_id)
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
	}
	resp_district = requests.get(url, headers=headers)
	data = resp_district.json()
	for district in data['districts']:
		if district['district_name'] == dis_name:
			return (district['district_id'])

def get_seven_days_data_for_fortyfive_plus(dis_id, data):
	url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
	params = {"district_id":dis_id, "date":data}
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
	}
	response = requests.get(url, headers=headers, params=params)
	data = response.json()
	return [session for session in get_relevant_data(data) if get_forty_five_plus_data(session) and is_available(session)]


def get_seven_days_data_for_eighteen_plus(dis_id, data):
	url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
	params = {"district_id":dis_id, "date":data}
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
	}
	response = requests.get(url, headers=headers, params=params)
	data = response.json()
	return [session for session in get_relevant_data(data) if get_eighteen_plus_data(session) and is_available(session)]


def content(info):
	data_list = []
	for data in info:
		data_list.append(f"Name:{data['name']} - Date:{data['date']} - Capacity:{data['capacity']} - Age Limit:{data['age_limit']}")

	return (data_list)

if __name__ == '__main__':
	state_name = input(f'Enter State Name: ').title()
	dis_name = input(f'Enter District Name: ').title()
	date = input('Enter date to check \n Please enter date in format dd-mm-yyyy: ')
	age = input('Enter age to check \n a) Type 18+, to check between 18-45 \n b) Type 45+, to check above 45 : ')

	sta_id = get_state_id(state_name)
	dis_id = get_district_id(dis_name, sta_id)

	if age == '18+':
		resp_data = get_seven_days_data_for_eighteen_plus(dis_id, date)
		get_result = content(resp_data)
		if get_result:
			for data in get_result:
				print(data)
		else:
			print ("No slot available")
	elif age == '45+':
		resp_data = get_seven_days_data_for_fortyfive_plus(dis_id, date)
		get_result = content(resp_data)
		if get_result:
			for data in get_result:
				print(data)
		else:
			print("No slot available")
	else:
		print("Incorrect age entered. Please select correct age between 18+ and 45+")
	
