# Josh Ryan 2019
# application to slice song data, and create spectrograms

from subprocess import Popen, PIPE, STDOUT
import os
from os.path import isdir, splitext
from PIL import Image
import glob
import eyed3

#Remove logs
eyed3.log.setLevel("ERROR")

currentPath = os.path.dirname(os.path.realpath(__file__)) 

def createSpectrogram(path,filename,track_id):
	# create new directory for song
	f = "tmp/spec/{}".format(track_id)

	try:
		os.makedirs(f)
	except FileExistsError:
		# directory already exists
		pass

	if eyed3.load('{}/{}'.format(path,filename)).info.mode == 'Mono':
		command = "cp '{}/{}' '/tmp/{}.mp3'".format(path,filename,track_id)
	else:
		#Create temporary mono track
		command = "sox '{}/{}' 'tmp/{}.mp3' remix 1,2".format(path,filename,track_id)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print(errors)


	#Create spectrograms
	filename.replace(".mp3","")

	# sox args: 
	# -Y height is nearest power of 2, so -Y 300 -> height = 256
	# -X is pixels/second (x axis)
	# -m monochrome
	# -r no axis or legends
	# -o output name

	counter = 0

	while (counter < 10):

		command = "sox 'tmp/{}.mp3' -n sinc 500 trim {} {} rate 10k spectrogram -Y 200 -X {} -m -r -o 'tmp/spec/{}/{}.png'".format(track_id,counter*3, 3, 25,track_id, counter)
		p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
		output, errors = p.communicate()
		if errors:
			print(errors)
		counter+=1

	#Remove tmp mono track
	try:
		os.remove("tmp/{}.mp3".format(track_id))
	except FileNotFoundError:
		"track {} is already mono"

# add directories to list
music_folders = [f for f in glob.glob("fma_small/*") if isdir(f)]

num = len(music_folders)
c = 0
for folder in music_folders:
	for song in os.listdir(folder):
		c += 1
		# split text for song_id, return query 
		createSpectrogram(folder,song, str(splitext(song)[0]))

	print('{}/{} songs converted to spectrogram'.format(c,num))
