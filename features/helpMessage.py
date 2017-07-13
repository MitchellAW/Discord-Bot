from settings import *

helpMessage = '''
{0}join
Will join the voice channel that you're in.

{0}leave
Will leave the voice channel that the you're in.

{0}play [youtube Url] or !play [song or video to search for]
Will begin playing the audio of the video/song provided.

{0}pause
Will pause the current audio stream.

{0}resume
Will resume the current audio stream.

{0}stop
Will stop and end the audio stream.

{0}invite
Will send a personal message with the invite link of the bot.

{0}shutdown
Will make the bot logout and shutdown. Will only work for owner of the bot.

{0}status [status here]
Will set the game playing status of the bot. Will only work for the owner of the bot.

{0}joke
Posts a random Chuck Norris joke.

{0}8ball
Will post a wise 8 Ball answer to any question.

{0}coinflip
Will flip a coin and post the result.

{0}roll [# of dice] D[# of sides] Example: !roll 3 D6
Will roll the dice specified and post the result.

{0}slots
Will post a slot machine result.

{0}cat
Will post a random cat picture or gif.

{0}catfact (CURRENTLY OUT OF ORDER)
Will post a random cat fact.

{0}catgif
Will post a random cat gif.

{0}simpsons
Will post a random simpsons quote with the screen at the timestamp of the quote.

{0}simpsonsquote [quote to search for]
Will search for the quote and post the subtitles and screen at the timestamp of the quote

{0}simpsonsclip
Will post a random simpsons clip from the Simpsons Clip youtube channel.

{0}boo
Will post a reply.

{0}futurama
Will post a random futurama quote with the screen at the timestamp of the quote.

{0}futuramaquote [quote to search for]
Will search for the quote and post the subtitles and screen at the timestamp of the quote

{0}hots [hotslogs player ID] - Example: !hots 3141592
Will post the player's MMR for quick match and hero league

{0}gwent [Card Name] - Example: !gwent Geralt
Will post the card description and picture of the gwent card. Has a max search length of 10 characters.'''.format(config.COMMANDPREFIX)
