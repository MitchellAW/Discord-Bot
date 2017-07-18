import random

from settings import *

# Returns a random magic 8 Ball message
def getEightBall():
	eightBallMessages = ['It is certain', 'It is decidedly so', 'Without a doubt',
				        'Yes, definitely', 'You may rely on it', 'As I see it, yes',
				        'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
				        'Reply hazy, try again', 'Ask again later', 'Better not tell you now',
				        'Cannot predict now', 'Concentrate and ask again',
				        'Don\'t count on it', 'My reply is no', 'My sources say no',
				        'Outlook not so good', 'Very doubtful']

	return random.choice(eightBallMessages)

# Returns random result to a coin flip
def getCoinFace():
	coinFaces = ['Heads', 'Tails']

	return random.choice(coinFaces)

# Returns a random slot machine screen, uses discord emoji in the display
def getSlotsScreen():
	slots = ['chocolate_bar', 'bell', 'tangerine', 'apple', 'cherries', 'seven']
	slot1 = slots[random.randint(0, 5)]
	slot2 = slots[random.randint(0, 5)]
	slot3 = slots[random.randint(0, 5)]
	slot4 = slots[random.randint(0, 5)]

	slotOutput = '|\t:{}:\t|\t:{}:\t|\t:{}:\t|\t:{}:\t|\n'.format(slot1, slot2, slot3, slot4)

	if slot1 == slot2 and slot2 == slot3 and slot3 == slot4 and slot4 != 'seven':
		return slotOutput + '$$ GREAT $$'

	elif slot1 == 'seven' and slot2 == 'seven' and slot3 == 'seven' and slot4 == 'seven':
		return slotOutput + '$$ JACKPOT $$'

	elif slot1 == slot2 and slot3 == slot4 or slot1 == slot3 and slot2 == slot4 or slot1 == slot4 and slot2 == slot3:
		return slotOutput + '$ NICE $'

	else:
		return slotOutput

# Rolls dice using both the number of dice and number of sides per dice given
def rollDice(messageText):
	messageText = messageText.split()
	diceRolls = []
	if len(messageText) == 3:
		if (messageText[1].isdigit() and messageText[2][1:].isdigit() and
		    int(messageText[1]) > 0 and int(messageText[2][1:]) > 0):

			if messageText[2][0].lower() == 'd':
				if int(messageText[1]) <= 20 and int(messageText[2][1:]) <= 100:
					for i in range(int(messageText[1])):
						diceRolls.append(random.randint(1, int(messageText[2][1:])))

					diceOutput = 'Rolled ' + messageText[1] + ' x D' + messageText[2][1:] + ': '
					for i in range(len(diceRolls)):
						diceOutput += str(diceRolls[i])

						if i < len(diceRolls) - 1:
							diceOutput += ' + '

					diceOutput += ' = ' + str(sum(diceRolls))

					return diceOutput

				else:
					return 'Exceeded maximum. Maximum allowed: {}roll 20 D100'.format(config.COMMANDPREFIX)

			else:
				return 'You must specify the number of sides per dice properly. Usage: {}roll 3 D6'.format(config.COMMANDPREFIX)

		else:
			return 'Invalid syntax. Must use positive numbers. Usage: {}roll 3 D6'.format(config.COMMANDPREFIX)

	else:
		return 'Incorrect number of arguments. Usage: {}roll 3 D6'.format(config.COMMANDPREFIX)
