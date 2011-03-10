import utils

def movies(titles):
    url = 'http://www.tastekid.com/ask/ws?q=movie:' + titles + '&format=JSON'
    return utils.getjsonfromurl(url)['Similar']['Results']