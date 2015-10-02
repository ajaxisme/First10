from datetime import date, timedelta
import simplejson as json
import requests

GDEBUG = 0
PDEBUG = 0

#Get yesterday and today
today = date.today()
yesterday = today - timedelta(days=1)
from_date = yesterday.strftime("%y-%m-%d")
from_date = '20' + from_date
to_date = today.strftime("%y-%m-%d")
to_date = '20' + to_date
if GDEBUG:
	print from_date
	print to_date

guardian_api = {'search' : '/search'}

guardian_parametes = {'page' : 1,'from-date':'2015-01-01','to-date':'2015-01-03','page-size':10, 'api-key': 'test', 'section':'sport', 'tag':'tag-name', 'q': 'soccer'}

with open('guardian_api', 'r') as f:
	guardian_key = f.read()

guardian_key = guardian_key[:-1]

guardian_url = 'http://content.guardianapis.com'

guardian_request_data = {'api-key': guardian_key, 'page': 1,
						 'page-size' : 10, 'from-date' : from_date,
						 'to-date' : to_date}

#Send request to guardian for posts
guardian_uri = guardian_url + guardian_api['search']
if GDEBUG:
	print "Request-data: %s" % str(guardian_request_data)

if not GDEBUG:
	response = requests.get(guardian_uri, params=guardian_request_data)
	#Guardian response data in json format
	json_data = response.json()
else:
	with open('sample.json', 'r') as f:
		json_data = eval(f.read())

status = json_data.get('response').get('status')

if status == "ok":
	results = json_data.get('response').get('results')

data = {} #data from guardian to upload to pocket

for result in results:
	if result.get('type') == "article": #Only consider articles
		data[result.get('webUrl')] = result.get('webTitle')

#Upload data to pocket

pocket_api = {'get_token' : '/v3/oauth/request',
	   'authorize' : '/v3/oauth/authorize',
	   'add2pocket' : '/v3/add'
}

pocket_url = 'https://getpocket.com'

with open('pocket_consumer_key', 'r') as f:
	pocket_ckey = f.read()

headers = {"Content-Type":"application/json; charset=UTF-8",
			"X-Accept": "application/json"}

params = {"consumer_key":pocket_ckey,
		  "redirect_uri":"http://example.com"}

pocket_uri = pocket_url + pocket_api.get('get_token')

if PDEBUG:
	print pocket_uri

if not PDEBUG:
		response = requests.post(pocket_uri, headers=headers, data=json.dumps(params))

		pocket_json = response.json()
else:
	with open("pkt.json", "r") as f:
		pocket_json = eval(f.read())
		print json.dumps(pocket_json)
		pocket_json = json.loads(json.dumps(pocket_json))

#Add to Pocket
access_code = pocket_json.get("code")

authorize_params = {"consumer_key":pocket_ckey[:-1],
		  "code": access_code}
#print authorize_params

pocket_uri = pocket_url + pocket_api.get('authorize')
response = requests.post(pocket_uri, headers=headers, data=json.dumps(authorize_params))
print response.text

"""
add_params = {}
if PDEBUG:
	single_data = {}
	for key in data:
		single_data[key] = data[key]
		break

	for key in single_data:
		add_params["url"] = key
		add_params["title"] = single_data[key]
		add_params["consumer_key"] = pocket_ckey[:-1]
		add_params["access_token"] = access_code

	print add_params

pocket_uri = pocket_url + pocket_api.get('add2pocket')
response = requests.post(pocket_uri, headers=headers, data=json.dumps(add_params))
print response.text
"""
