import requests

from settings import *

# Returns the Quick Match and Hero League MMR of the hotslogs profile using their player ID
def getHotsStats(messageText):
    messageText = messageText.split(' ')
    hotsName = ''

    referenceUrl = 'https://www.hotslogs.com/Player/Profile?PlayerID='
    hotsApiUrl = 'https://api.hotslogs.com/Public/Players/'

    if len(messageText) > 1:
        hotsName = messageText[1]

        profile = requests.get(hotsApiUrl + messageText[1])

        if profile.status_code == 200:
            hotsJson = profile.json()

            if profile.text != 'null':
                quickMatchMMR = 'null'
                heroLeagueMMR = 'null'

                hotsLogsUrl = referenceUrl + str(hotsJson['PlayerID'])

                # Check if they have MMR's for QM/HL and only change them from null if they do
                if len(hotsJson['LeaderboardRankings']) > 0:
                    quickMatchMMR = str(hotsJson['LeaderboardRankings'][0]['CurrentMMR'])

                elif len(hotsJson['LeaderboardRankings']) > 1:
                    heroLeagueMMR = str(hotsJson['LeaderboardRankings'][1]['CurrentMMR'])

                return (referenceUrl + messageText[1] + '\n' + 'Quick Match MMR: ' + quickMatchMMR + '\n' +
                        'Hero League MMR: ' + heroLeagueMMR)

            else:
                return 'Failed to find player. Make sure your playerID is corrent. Usage: {}hots 3141592'.format(config.COMMANDPREFIX)

        else:
            return 'Error 404. Website may be down.'

    else:
        return 'You need to enter your playerID. Usage: {}hots 3141592'.format(config.COMMANDPREFIX)
