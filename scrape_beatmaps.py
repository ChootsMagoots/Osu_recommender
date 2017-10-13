from osuapi import OsuApi, AHConnector
import aiohttp
import asyncio
import pymongo
import requests
import time
import random

async def get_beatmap(api, beatmap_id):
	beatmap = await api.get_beatmaps(beatmap_id = beatmap_id)
	return beatmap

def parse_and_store_beatmap(beatmap):
	beatmap_dict = {'approved': str(beatmap.approved), 'approved_date': str(beatmap.approved_date), 'last_update': str(beatmap.last_update), 'artist': str(beatmap.artist), 'beatmap_id': str(beatmap.beatmap_id), 'beatmapset_id': str(beatmap.beatmapset_id), 'bpm': str(beatmap.bpm), 'creator': str(beatmap.creator), 'difficultyrating': str(beatmap.difficultyrating), 'diff_size': str(beatmap.diff_size), 'diff_overall': str(beatmap.diff_overall), 'diff_approach': str(beatmap.diff_approach), 'diff_drain': str(beatmap.diff_drain), 'hit_length': str(beatmap.hit_length), 'source': str(beatmap.source), 'genre_id': str(beatmap.genre_id), 'language_id': str(beatmap.language_id), 'title': str(beatmap.title), 'total_length': str(beatmap.total_length), 'version': str(beatmap.version), 'file_md5': str(beatmap.file_md5), 'mode': str(beatmap.mode), 'tags': str(beatmap.tags), 'favourite_count': str(beatmap.favourite_count), 'playcount': str(beatmap.playcount), 'passcount': str(beatmap.passcount), 'max_combo': str(beatmap.max_combo)}
	mongo_beatmaps.save(beatmap_dict)



if __name__ == '__main__':
	mongodb_uri = None
	mc = pymongo.MongoClient(mongodb_uri)  # Create MongoClient instance
	db = mc['osu_data']  # Specify the database to work with
	user = db['user']  # Specify the collection name to work with
	user_best = db['user_best']
	user_recent = db['user_recent']
	mongo_beatmaps = db['beatmaps']
	api = OsuApi("4f01671000fb773e9c988d46ec7ffec3def52719", connector=AHConnector())

	to_scrape = ['487384']

	for beatmap_id in to_scrape:
		try: 
			beatmaps = asyncio.get_event_loop().run_until_complete(get_beatmap(api, beatmap_id))
			for beatmap in beatmaps: 
				parse_and_store_beatmap(beatmap)
		except aiohttp.client_exceptions.ClientPayloadError:
			print('get_user_recent(): ' + str(beatmap_id) + ' not successful.')
		time.sleep(1)
		print(str(beatmap_id) + "completed.")




'''
approved = Attribute(PreProcessInt(BeatmapStatus))
approved_date = Attribute(Nullable(DateConverter))
last_update = Attribute(DateConverter)
artist = Attribute(str)
beatmap_id = Attribute(int)
beatmapset_id = Attribute(int)
bpm = Attribute(float)
creator = Attribute(str)
difficultyrating = Attribute(float)
diff_size = Attribute(float)
diff_overall = Attribute(float)
diff_approach = Attribute(float)
diff_drain = Attribute(float)
hit_length = Attribute(int)
source = Attribute(str)
genre_id = Attribute(PreProcessInt(BeatmapGenre))
language_id = Attribute(PreProcessInt(BeatmapLanguage))
title = Attribute(str)
total_length = Attribute(int)
version = Attribute(str)
file_md5 = Attribute(str)
mode = Attribute(PreProcessInt(OsuMode))
tags = Attribute(str)
favourite_count = Attribute(int)
playcount = Attribute(int)
passcount = Attribute(int)
max_combo = Attribute(Nullable(int))
'''