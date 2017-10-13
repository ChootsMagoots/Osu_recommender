from osuapi import OsuApi, AHConnector
import aiohttp
import asyncio
import pymongo
import requests
import time
import random

async def get_user(api, user_id):
	results = await api.get_user(user_id)
	return results
async def get_user_best(api, user_id):
	results = await api.get_user_best(user_id)
	return results

async def get_user_recent(api, user_id):
	results = await api.get_user_recent(user_id)
	return results

def parse_user(user):
	user_dict = {'user_id': str(user.user_id), 'username': str(user.username), 'count300': str(user.count300), 'count100': str(user.count100), 
					'count50': str(user.count50), 'playcount': str(user.playcount), 'ranked_score': str(user.ranked_score), 
					'total_score': str(user.total_score), 'pp_rank': str(user.pp_rank), 'level': str(user.level), 'pp_raw': str(user.pp_raw), 
					'accuracy': str(user.accuracy), 'count_rank_ss': str(user.count_rank_ss), 'count_rank_s': str(user.count_rank_s), 
					'count_rank_a': str(user.count_rank_a), 'country': str(user.country), 'pp_country_rank': str(user.pp_country_rank),
					'events': str(user.events)}
	return user_dict

def parse_user_recent(point, user_id):
	recent_dict = {'user_id': str(user_id), 'beatmap_id': str(point.beatmap_id), 'enabled_mods': str(point.enabled_mods), 'date': str(point.date)}
	return recent_dict

	'''
	beatmap_id = Attribute(str)
    enabled_mods = Attribute(PreProcessInt(OsuMod))
    date = Attribute(DateConverter)
    '''

#with mongodb running in terminal:
mongodb_uri = None
mc = pymongo.MongoClient(mongodb_uri)  # Create MongoClient instance
db = mc['osu_data']  # Specify the database to work with
user = db['user']  # Specify the collection name to work with
user_best = db['user_best']
user_recent = db['user_recent']
# Get a collection instance
# Now we have a collection instance, ready to play with...

# Clear up previous lecture cruft if needed:
# result = coll.delete_many({})
# print(result.deleted_count)

# coll.find_one()
# coll.find().count()
# coll.save({'test': 1})
# coll.find_one()
# coll.find().count()
# coll.update({'test': 1}, {'test': 2})
# coll.find_one()
# coll.find().count()

#if __name__ == '__main__':

user_ids = random.sample(range(1, 5000000), 500000)
api = OsuApi("4f01671000fb773e9c988d46ec7ffec3def52719", connector=AHConnector())
collected = 0
i = 0
requests = 0
while requests < 550000:
	user_id = user_ids[i]
	try:
		results = asyncio.get_event_loop().run_until_complete(get_user_recent(api, user_id))
		requests += 1
		time.sleep(0.25)
		if results != []:
			for result in results:
				user_recent.save(parse_user_recent(result, user_id))
			collected = collected + 1
		'''
		else: 
			user.remove({'user_id': str(user_id)})
			user_best.remove({'user_id': str(user_id)})
			user_recent.remove({'user_id': str(user_id)})
			break
		'''
	except aiohttp.client_exceptions.ClientPayloadError:
		print('get_user_recent(): ' + str(user_id) + ' not successful.')
	try:
		results = asyncio.get_event_loop().run_until_complete(get_user(api, user_id))
		requests += 1
		time.sleep(0.25)
		if results != []:
			user.save(parse_user(results[0]))
			collected += 1
		'''
		else: 
			user.remove({'user_id': str(user_id)})
			user_best.remove({'user_id': str(user_id)})
			user_recent.remove({'user_id': str(user_id)})
			break
		'''
	except aiohttp.client_exceptions.ClientPayloadError:
		print('get_user():' + str(user_id) + ' not successful.')
	try: 
		results = asyncio.get_event_loop().run_until_complete(get_user_best(api, user_id))
		requests += 1
		time.sleep(0.25)
		if results != []:
			for result in results:
				user_best.save(parse_user_recent(result, user_id))
			collected += 1
		'''
		else: 
			user.remove({'user_id': str(user_id)})
			user_best.remove({'user_id': str(user_id)})
			user_recent.remove({'user_id': str(user_id)})
			break
		'''
	except aiohttp.client_exceptions.ClientPayloadError:
		print('get_user_best(): ' + str(user_id) + ' not successful.')
	print('user: ' + str(user_id) + ': completed.')
	print('Data collected: ', collected)

	i += 1
api.close()



'''
	user_id = Attribute(int)
    username = Attribute(str)
    count300 = Attribute(Nullable(int))
    count100 = Attribute(Nullable(int))
    count50 = Attribute(Nullable(int))
    playcount = Attribute(Nullable(int))
    ranked_score = Attribute(Nullable(int))
    total_score = Attribute(Nullable(int))
    pp_rank = Attribute(Nullable(int))
    level = Attribute(Nullable(float))
    pp_raw = Attribute(Nullable(float))
    accuracy = Attribute(Nullable(float))
    count_rank_ss = Attribute(Nullable(int))
    count_rank_s = Attribute(Nullable(int))
    count_rank_a = Attribute(Nullable(int))
    country = Attribute(str)
    pp_country_rank = Attribute(int)
    events = Attribute(JsonList(str))
 '''