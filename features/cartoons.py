import random
import requests

from settings import *

# Returns a random simpsons quote and image at the timestamp of that quote
def getSimpsonsQuote():
	frinkiacUrl = requests.get('https://frinkiac.com/api/random')
	if frinkiacUrl.status_code == 200:
		frinkiacJson = frinkiacUrl.json()

		episode = frinkiacJson['Frame']['Episode']
		timestamp = frinkiacJson['Frame']['Timestamp']

		frinkiacUrl = 'https://frinkiac.com/caption/' + str(episode) + '/' + str(timestamp)
		imageUrl = 'https://frinkiac.com/img/' + str(episode) + '/' + str(timestamp) + '.jpg'
		caption = '\n'.join([subtitle['Content'] for subtitle in frinkiacJson['Subtitles']])

		return imageUrl + '\n' + caption

	else:
	    return 'Error 404. Website may be down.'

def findSimpsonsQuote(messageText):
	frinkiacSearchUrl = 'https://frinkiac.com/api/search?q='
	frinkiacCaption = 'http://frinkiac.com/api/caption?e={}&t={}'
	if len(messageText) > 14:
		messageText = messageText[14:].split()
		searchText = ''
		for i in range(len(messageText)):
				searchText += messageText[i]
				if i < len(messageText) - 1:
					searchText += '+'

		frinkiacSearchUrl = requests.get(frinkiacSearchUrl + searchText)

		if frinkiacSearchUrl.status_code == 200:
			firstResult = frinkiacSearchUrl.json()
			if len(firstResult) > 0:
				firstResult = firstResult[0]

				episode = firstResult['Episode']
				timestamp = firstResult['Timestamp']
				imageUrl = 'https://frinkiac.com/img/' + str(episode) + '/' + str(timestamp) + '.jpg'
				caption = ''


				frinkiacCaption = requests.get(frinkiacCaption.format(str(episode), str(timestamp)))
				if frinkiacCaption.status_code == 200:
					for quote in frinkiacCaption.json()['Subtitles']:
						caption += quote['Content'] + '\n'

					return imageUrl + '\n' + caption

				else:
					return imageUrl + '\n' + 'Error 404. Website may be down.'

			else:
				return 'No results found. Usage: {}simpsonsquote stupid sexy flanders'.format(config.COMMANDPREFIX)

		else:
			return 'Error 404. Website may be down. Usage: {}simpsonsquote stupid sexy flanders'.format(config.COMMANDPREFIX)

	else:
		return 'Invalid number of arguments. Usage: {}simpsonsquote stupid sexy flanders'.format(config.COMMANDPREFIX)

# Returns a random futurama quote and image at the timestamp of that quote
def getFuturamaQuote():
    morboUrl = requests.get('https://morbotron.com/api/random')
    if morboUrl.status_code == 200:
        morboJson = morboUrl.json()

        episode = morboJson['Frame']['Episode']
        timestamp = morboJson['Frame']['Timestamp']

        morboUrl = 'https://morbotron.com/caption/' + str(episode) + '/' + str(timestamp)
        imageUrl = 'https://morbotron.com/img/' + str(episode) + '/' + str(timestamp) + '.jpg'
        caption = '\n'.join([subtitle['Content'] for subtitle in morboJson['Subtitles']])

        return imageUrl + '\n' + caption

    else:
        return 'Error 404. Website may be down.'

def findFuturamaQuote(messageText):
	morboSearchUrl = 'https://morbotron.com/api/search?q='
	morboCaption = 'http://morbotron.com/api/caption?e={}&t={}'
	if len(messageText) > 14:
		messageText = messageText[14:].split()
		searchText = ''
		for i in range(len(messageText)):
				searchText += messageText[i]
				if i < len(messageText) - 1:
					searchText += '+'

		morboSearchUrl = requests.get(morboSearchUrl + searchText)

		if morboSearchUrl.status_code == 200:
			firstResult = morboSearchUrl.json()
			if len(firstResult) > 0:
				firstResult = firstResult[0]

				episode = firstResult['Episode']
				timestamp = firstResult['Timestamp']
				imageUrl = 'https://morbotron.com/img/' + str(episode) + '/' + str(timestamp) + '.jpg'
				caption = ''

				morboCaption = requests.get(morboCaption.format(str(episode), str(timestamp)))

				if morboCaption.status_code == 200:
					for quote in morboCaption.json()['Subtitles']:
						caption += quote['Content'] + '\n'

					return imageUrl + '\n' + caption

				else:
					return imageUrl + '\n' + 'Error 404. Website may be down.'

			else:
				return 'No results found. Usage: {}futurama just shutup and take my money'.format(config.COMMANDPREFIX)

		else:
			return 'Error 404. Website may be down. Usage: {}futurama just shutup and take my money'.format(config.COMMANDPREFIX)

	else:
		return 'Invalid number of arguments. Usage: {}futuramaquote just shutup and take my money'.format(config.COMMANDPREFIX)

# I was saying boo-urns
def booUrns():
	return 'https://frinkiac.com/meme/S06E18/1054719.jpg?b64lines=SSB3YXMgc2F5aW5nLAogImJ1dS11cm5zLiI='

# Returns a random simpsons clip from the Simpsons Clips youtube channel
def getSimpsonsVideo():
	youtubeUrl = 'https://www.youtube.com/watch?v='
	url = 'https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&type=video&channelId=UCjQyoKg38Her282_PUiEI7Q&maxResults=50&key=AIzaSyB7klDTBbbo0Y5GUmmoqXtLA1bmllnZNqY&pageToken='
	loopNumber = random.randint(1, 5)
	nextPageToken = ''

	for i in range(loopNumber):
		page = requests.get(url + nextPageToken).json()
		nextPageToken = page['nextPageToken']

	videoNumber = random.randint(1, len(page['items']) - 1)

	return youtubeUrl + page['items'][videoNumber]['id']['videoId']

def getXkcdComicWithInfo():
	xkcdUrl = 'http://xkcd.com/{}/info.0.json'

	lastNumber = requests.get(latestXkcdUrl)
	if lastNumber.status_code == 200:
		lastNumber = lastNumber.json()['num']
		randomXkcd = requests.get(xkcdUrl.format(random.randint(1, lastNumber)))
		if randomXkcd.status_code == 200:
			return randomXkcd.json()['img'] + '\n' + randomXkcd.json()['title']

		else:
			return 'Error 404. Website may be down. Usage: {}xkcd'.format(config.COMMANDPREFIX)

	else:
		return 'Error 404. Website may be down. Usage: {}xkcd'.format(config.COMMANDPREFIX)

def getXkcdComic():
	xkcdBaseUrl = 'http://xkcd.com/{}/'
	latestXkcdUrl = 'https://xkcd.com/info.0.json'

	lastNumber = requests.get(latestXkcdUrl)
	if lastNumber.status_code == 200:
		lastNumber = lastNumber.json()['num']
		return xkcdBaseUrl.format(random.randint(1, lastNumber))

	else:
		return 'Error 404. Website may be down. Usage: {}xkcd'.format(config.COMMANDPREFIX)
