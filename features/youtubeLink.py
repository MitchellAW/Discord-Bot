import requests

# Returns a youtube link using the message text
def getYoutubeLink(messageText):
    # Ignore 'play '
    linkText = messageText[5:]
    if len(linkText.split()) > 1:
        # Search for video if more than one word after !play
        return searchYoutube(linkText)

    else:
        # If the standard beginnings of the link aren't there, just search youtube with the text
        if linkText[:4] != 'www.' and linkText[:11] != 'http://www.' and linkText[:12] != 'https://':
            return searchYoutube(linkText)

        # Otherwise, append http:// and try the youtube link
        else:
            linkText = 'http://' + linkText

            testLink = requests.get(linkText)
            if testLink.status_code == 200:
                return testLink

            else:
                return ('404 page not found. Usage: !play cantina theme or '
                + '!play http://www.youtube.com/watch?v=FWO5Ai_a80M')

# Will return the link to youtube's first result
def searchYoutube(searchText):
    searchUrl = ('https://www.googleapis.com/youtube/v3/search?order=relevance'
                + '&part=snippet&type=video&searchmaxResults=1&key=GOOGLE_API_KEY_HERE'
                + searchText)

    searchPage = requests.get(searchUrl)

    if searchPage.status_code == 200:
        searchPage = searchPage.json()

        # Check number of search results using search parameters
        if searchPage['pageInfo']['totalResults'] != 0:
            videoId = searchPage['items'][0]['id']['videoId']
            return 'http://www.youtube.com/watch?v=' + videoId

        # If no results, return error message
        else:
            return ('No results found. Usage: !play cantina theme or '
                    + '!play http://www.youtube.com/watch?v=FWO5Ai_a80M')

    else:
        return ('404 Page not found. Usage: !play cantina theme or '
                + '!play http://www.youtube.com/watch?v=FWO5Ai_a80M')
