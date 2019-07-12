# Josh Ryan 2019
# application to mine spotify feature data for a given mp3 dataset. 

import spotipy
import os
from os import listdir
from os.path import isdir, splitext
import glob
import csv
import numpy as np
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

# init spotify api connection and oauth
client_credentials_manager = SpotifyClientCredentials(client_id='CLIENT_ID_HERE',
                                                      client_secret='CLIENT_SECRET_HERE')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# create dataframe containing track metadata
# we need track_id, artist_name, track_title
tracks_vals = pd.read_csv('metadata/raw_tracks.csv', delimiter = ',')

# csv to update
new_csv = pd.DataFrame()
new_data = {'track_id': None, 'track_key': None, 'track_mode': None}

#new_csv = new_csv.append({'track_id': None, 'track_key': None, 'track_mode': None}, ignore_index=True)


# add directories to list
music_folders = [f for f in glob.glob("fma_small/*") if isdir(f)]

num_tracks = 0
questionable = 0
total_tracks = 0
for folder in music_folders:
	for song in listdir(folder):
		# split text for song_id, return query 
		song_data = tracks_vals[tracks_vals.track_id == int(splitext(song)[0])]
		artist = song_data.iloc[0]['artist_name']
		track = song_data.iloc[0]['track_title']

		track_id = sp.search(q='artist:' + artist + ' track:' + track, type='track')

		if track_id['tracks']['total'] != 0:
			questionable +=1
		if (track_id['tracks']['total'] == 1):
			new_data['track_id'] = str(song_data.iloc[0]['track_id'])

			# get spotify id
			new_data['spot_id'] = track_id['tracks']['items'][0]['id']

			# get audio features form spotify api
			features = sp.audio_features([new_data['spot_id']])
			new_data['track_key'] = features[0]['key']
			new_data['track_mode'] = features[0]['mode']

			new_csv = new_csv.append(new_data, ignore_index=True)
			num_tracks += 1
		else:
			os.remove("{}/{}".format(folder,song))

		total_tracks += 1

		# for i, t in enumerate(results['tracks']['items']):
  #  			print(' {i} {t}'.format(i, t['name']))
	print('matching tracks: {}'.format(num_tracks))
	print('questionable tracks: {}'.format(questionable))
	print('total tracks: {}'.format(total_tracks))

# convert to CSV
new_csv.to_csv('tmp/aggregate.csv')

