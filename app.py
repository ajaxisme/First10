import urllib2
import urllib

pocket_api = {'get_access_token' : '/v3/oauth/request',
	   'authorize' : '/v3/oauth/authorize',
	   'add2pocket' : '/v3/add'
}

guardian_api = {'search' : '/search'}

guardian_parametes = {'page' : 1,'from-date':'2015-01-01','to-date':'2015-01-03','page-size':10, 'api-key': 'test', 'section':'sport', 'tag':'tag-name', 'q': 'soccer'}



