import asyncio
import discord
import requests
import youtube_dl

from features import *
from settings import *

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in...')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))
    print('Invite URL: ' + 'https://discordapp.com/oauth2/authorize?&client_id=' + client.user.id + '&scope=bot&permissions=0')

# Announce the change in voice state through text to speech (ignores mutes/deafens)
@client.event
async def on_voice_state_update(before, after):
    # Ensure bot is connected to voice client (!join has been used)
    if client.is_voice_connected(before.server) == True:
        global player
        previousChannel = before.voice_channel
        newChannel = after.voice_channel

        # Bot only talks when user's channel changes, not on mutes/deafens
        if previousChannel != newChannel:
            # When user joins or moves to bot's channel
            if newChannel == currentChannel:
                tts.createAnnouncement(after.name, 'has joined the channel')

            # When user leaves bot's channel
            elif previousChannel != None and newChannel == None and previousChannel == currentChannel:
                tts.createAnnouncement(after.name, 'has left the channel')

            # When user moves out of bot's channel to a new channel
            elif previousChannel == currentChannel and newChannel != currentChannel:
                tts.createAnnouncement(after.name, 'had moved to another channel')

            # After user joins, leaves or moves, announce the new announcement
            if (newChannel == currentChannel or previousChannel != None and
                newChannel == None and previousChannel == currentChannel or
                previousChannel == currentChannel and newChannel != currentChannel):

                try:
                    if player.is_playing() == False:
                        player = voice.create_ffmpeg_player('announce.mp3')
                        player.start()

                except NameError:
                    player = voice.create_ffmpeg_player('announce.mp3')
                    player.start()

@client.event
async def on_message(message):
    # If the message author isn't the bot and the message starts with the
    # command prefix ('!' by default), check if command was executed
    if message.author.id != config.BOTID and message.content.startswith(config.COMMANDPREFIX):
        # Remove prefix and change to lowercase so commands aren't case-sensitive
        message.content = message.content[1:].lower()

        # Shuts the bot down - only usable by the bot owner specified in config
        if message.content.startswith('shutdown') and message.author.id == config.OWNERID:
            await client.send_message(message.channel, 'Shutting down. Bye!')
            await client.logout()
            await client.close()

        # Allows owner to set the game status of the bot
        elif message.content.startswith('status') and message.author.id == config.OWNERID:
            await client.change_presence(game=discord.Game(name=message.content[7:]))

        # Help Message, sends a personal message with a list of all the commands
        # and how to use them correctly
        elif message.content.startswith('help'):
            await client.send_message(message.channel, 'Sending you a PM!')
            await client.send_message(message.author, helpMessage.helpMessage)

        # Sends a personal message with the invite link of the bot
        elif message.content.startswith('invite'):
            await client.send_message(message.channel, 'Sending you a PM!')
            await client.send_message(message.author, 'Invite URL: ' + 'https://discordapp.com/oauth2/authorize?&client_id=' + client.user.id + '&scope=bot&permissions=0')

        # Searches the second word following pythonhelp in python docs
        elif message.content.startswith('pythonhelp'):
            messagetext = message.content
            split = messagetext.split(' ')
            if len(split) > 1:
                messagetext = split[1]
                await client.send_message(message.channel, 'https://docs.python.org/3/search.html?q=' + messagetext)

        # Messages a random chuck norris joke - do not use, they're bloody terrible
        elif message.content.startswith('joke'):
            chuckJoke = requests.get('http://api.icndb.com/jokes/random?')
            if chuckJoke.status_code == 200:
                chuckJoke = chuckJoke.json()['value']['joke']
                await client.send_message(message.channel, chuckJoke)

        # Random 8 Ball message
        elif message.content.startswith('8ball'):
            await client.send_message(message.channel, rng.getEightBall())

        # Random coin flip
        elif message.content.startswith('coinflip'):
            await client.send_message(message.channel, rng.getCoinFace())

        elif message.content.startswith('roll'):
            await client.send_message(message.channel, rng.rollDice(message.content))

        # Slots machine in emoji format for discord
        elif message.content.startswith('slots'):
            await client.send_message(message.channel, rng.getSlotsScreen())

        # Random cat gif
        elif message.content.startswith('catgif'):
            await client.send_message(message.channel, cats.getCatGif())

        # Random cat picture
        elif message.content.startswith('cat'):
            await client.send_message(message.channel, cats.getCatPicture())

        # Messages link to a random Simpsons clip
        elif message.content.startswith('simpsonsclip'):
            await client.send_message(message.channel, cartoons.getSimpsonsVideo())

        # Searches for a Simpsons quote and sends the full quote with accompanying picture
        elif message.content.startswith('simpsonsquote'):
            await client.send_message(message.channel, cartoons.findSimpsonsQuote(message.content))

        # Messages a random Simpsons quote with accompanying picture
        elif message.content.startswith('simpsons'):
            await client.send_message(message.channel, cartoons.getSimpsonsQuote())

        # Messages Boo-urns
        elif message.content.startswith('boo'):
            await client.send_message(message.channel, cartoons.booUrns())

        # Searches for a Futurama quote and sends the full quote with accompanying picture
        elif message.content.startswith('futuramaquote'):
            await client.send_message(message.channel, cartoons.findFuturamaQuote(message.content))

        # Messages a random Futurama quote with accompanying picture
        elif message.content.startswith('futurama'):
            await client.send_message(message.channel, cartoons.getFuturamaQuote())

        # Messages a random XKCD comic
        elif message.content.startswith('xkcd'):
            await client.send_message(message.channel, cartoons.getXkcdComic())

        # Heroes of the Storm - Hots Logs - Messages MMR of playerID and Hots logs link
        elif message.content.startswith('hots'):
            await client.send_message(message.channel, hots.getHotsStats(message.content))

        # Takes following words as search arguments and messages information of gwent card
        elif message.content.startswith('gwent'):
            await client.send_message(message.channel, gwent.cardSearch(message.content))

        ########## VOICE COMMANDS ##########

        # Will join the voice channel of the message author if they're in a channel
        # and the bot is not currently connected to a voice channel
        elif message.content.startswith('join'):
            if message.author.voice_channel != None and client.is_voice_connected(message.server) != True:
                global currentChannel
                global player
                global voice
                currentChannel = client.get_channel(message.author.voice_channel.id)
                voice = await client.join_voice_channel(currentChannel)

            elif message.author.voice_channel == None:
                await client.send_message(message.channel, 'You are not in a voice channel.')

            else:
                await client.send_message(message.channel, 'I am already in a voice channel. Use !leave to make me leave.')

        # Will leave the current voice channel
        elif message.content.startswith('leave'):
            if client.is_voice_connected(message.server):
                currentChannel = client.voice_client_in(message.server)
                await currentChannel.disconnect()

        # Will play music using the following words as search parameters or use the
        # linked video if a link is provided
        elif message.content.startswith('play'):
            if message.author.voice_channel != None:
                if client.is_voice_connected(message.server) == True:
                    try:
                        if player.is_playing() == False:
                            print('not playing')
                            player = await voice.create_ytdl_player(youtubeLink.getYoutubeLink(message.content))
                            player.start()
                            await client.send_message(message.channel, ':musical_note: Currently Playing: ' + player.title)

                        else:
                            print('is playing')

                    except NameError:
                        print('name error')
                        player = await voice.create_ytdl_player(youtubeLink.getYoutubeLink(message.content))
                        player.start()
                        await client.send_message(message.channel, ':musical_note: Currently Playing: ' + player.title)

                else:
                    await client.send_message(message.channel, 'I am not connected to a voice channel. Use !join to make me join')

            else:
                await client.send_message(message.channel, 'You are not connected to a voice channel. Enter a voice channel and use !join first.')

        # Will pause the audio player
        elif message.content.startswith('pause'):
            try:
                player.pause()

            except NameError:
                await client.send_message(message.channel, 'Not currently playing audio.')

        # Will resume the audio player
        elif message.content.startswith('resume'):
            try:
                player.resume()

            except NameError:
                await client.send_message(message.channel, 'Not currently playing audio.')

        # Will stop the audio player
        elif message.content.startswith('stop'):
            try:
                player.stop()

            except NameError:
                await client.send_message(message.channel, 'Not currently playing audio.')

client.run(config.TOKEN)
