import requests

# Returns a random cat fact - CURRENTLY OUT OF ORDER
def getCatFact():
    catFact = requests.get('http://catfacts-api.appspot.com/api/facts')
    if catFact.status_code == 200:
        catFact = catFact.json()['facts'][0]
        return catFact

    else:
        return 'Error 404. Website may be down.'

# Returns a link to a random cat gif
def getCatGif():
    catGif = requests.get('http://thecatapi.com/api/images/get?format=src&type=gif')
    if catGif.status_code == 200:
        catGif = catGif.url
        return catGif

    else:
        return 'Error 404. Website may be down.'

# Returns a link to a random cat picture or cat gif
def getCatPicture():
    catPicture = requests.get('http://thecatapi.com/api/images/get.php')
    if catPicture.status_code == 200:
        catPicture = catPicture.url
        return catPicture

    else:
        return 'Error 404. Website may be down.'
