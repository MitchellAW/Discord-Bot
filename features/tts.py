from gtts import gTTS

# Will create a tts announcement that username has left, joined or moved to another channel
def createAnnouncement(username, message):
    global player
    try:
        if player.is_playing() == False:
            tts = gTTS(text=username + ' ' + message, lang='en')
            tts.save("announce.mp3")

    except NameError:
        tts = gTTS(text=username + ' ' + message, lang='en')
        tts.save("announce.mp3")
