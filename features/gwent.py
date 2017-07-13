import requests

from settings import *

# Gets the card description/details and card image of the card name following !gwent
def cardSearch(messageText):
	cardSearchLink = 'https://api.gwentapi.com/v0/cards?name='
	cardImageLink = 'https://gwent-api.herokuapp.com/card/name/{}/image'

	# Make sure no more than 10 search characters are provided
	if len(messageText) < 17:
		messageText = messageText.split()
		if len(messageText) > 1:
			searchText = ''
			messageText.remove('gwent')

			# Swap out spaces for +'s in search link
			for i in range(len(messageText)):
				searchText += messageText[i]
				if i < len(messageText) - 1:
					searchText += '+'

			searchResults = requests.get(cardSearchLink + searchText)

			if searchResults.status_code == 200:
				searchResults = requests.get(cardSearchLink + searchText).json()
				numResults = searchResults['count']

				# Check that the search term returned any results
				if numResults > 0:
					firstResult = searchResults['results'][0]
					cardLink = firstResult['href']
					cardName = firstResult['name']

					cardDetails = requests.get(cardLink).json()
					cardFaction = cardDetails['faction']['name']
					cardGroup = cardDetails['group']['name']
					cardDescription = cardDetails['info']
					cardRarity = cardDetails['variations'][0]['rarity']['name']
					cardPosition = ''
					# Display all of the row positions that a card might have
					for i in range(len(cardDetails['positions'])):
						cardPosition += cardDetails['positions'][i]
						if i != len(cardDetails['positions']) - 1:
							cardPosition += ' or '
					cardPosition += ' Row'

					# Get the image of the card - currently outdated pictures, might be a better API available
					cardImage = requests.get('https://gwent-api.herokuapp.com/card/name/' + cardName + '/image')

					# Tell the user how many search results, as some cards contain similar starting words (e.g. Geralt vs. Geralt: Agni)
					if numResults == 1:
						numResults = '1 result found.\n'

					else:
						numResults = str(numResults) + ' results found.\n'

					if cardImage.status_code == 200:
						cardImage = requests.get('https://gwent-api.herokuapp.com/card/name/' + cardName + '/image').text

					else:
						cardImage = '404. No Image Found'

					return numResults + cardImage + '\n' + cardName + ', ' + cardGroup + ' ' + cardRarity + ', ' + cardPosition + '\n' + 'Faction: ' + cardFaction + '\n' + 'Description: ' + cardDescription

				# Error messages
				else:
					return '0 results found. Usage: {}gwent Scorch (case-sensitive)'.format(config.COMMANDPREFIX)

			else:
				return '0 results found. Usage: {}gwent Scorch (case-sensitive)'.format(config.COMMANDPREFIX)

		else:
			return 'Not enough arguments. Usage: {}gwent Scorch (case-sensitive)'.format(config.COMMANDPREFIX)

	else:
		return 'Search too contains too many characters. Usage: {}}gwent Scorch (max 10 search characters)'.format(config.COMMANDPREFIX)
