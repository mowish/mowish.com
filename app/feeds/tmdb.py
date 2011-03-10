from mowish.app.models import *
from django.conf import settings
import datetime
import utils
import json


def moviesearch(search_term):
    url = settings.TMDB_MOVIESEARCH_URL + search_term.replace(' ', '%20')
    result = utils.getjsonfromurl(url)
    if result[0] == 'Nothing found.':
        return False
    else:
        return result 

def personsearch(search_term):
    url = settings.TMDB_PERSONSEARCH_URL + search_term.replace(' ', '%20')
    result = utils.getjsonfromurl(url)
    if result[0] == 'Nothing found.':
        return False
    else:
        return result 

def moviegetinfo(tmdb_id):
    return cache(settings.TMDB_MOVIEGETINFO_URL, tmdb_id)

def persongetinfo(tmdb_id):
    return cache(settings.TMDB_PERSONGETINFO_URL, tmdb_id)

import logging
def cache(tmdburl, id):
    tmdbcache = None
    if tmdburl == settings.TMDB_PERSONGETINFO_URL:
        tmdbcache = TmdbPersonCache.objects.filter(tmdb_id=id)
    if tmdburl == settings.TMDB_MOVIEGETINFO_URL:
        tmdbcache = TmdbMovieCache.objects.filter(tmdb_id=id)

    tmdbitem = None
    if tmdbcache:
        # there's a cached version
        tmdbcache = tmdbcache[0]
        if tmdbcache.timestamp + datetime.timedelta(hours=settings.TMDB_CACHE_PERIOD) < datetime.datetime.now():
            # cached version is expired
            url = tmdburl + tmdbcache.tmdb_id
            updated = utils.getjsonfromurl(url)[0] 
            if updated:
                if updated['version'] > tmdbcache.version:
                    # if there's new version, update
                    tmdbcache.jsondata = json.dumps(updated)
                    tmdbcache.updated = updated['last_modified_at']
                    tmdbcache.version = updated['version']
            # checked for new version so update the timestamp        
            tmdbcache.timestamp = datetime.datetime.now()
            tmdbcache.save()
        tmdbitem = json.loads(tmdbcache.jsondata)
    else:
        # there's no cached version so get the data and cache it
        url = tmdburl + id
        logging.error(url)
        tmdbitem = utils.getjsonfromurl(url)[0]
        logging.error(tmdbitem)
        logging.error(tmdbitem['id'])
        cache = None
        if tmdburl == settings.TMDB_MOVIEGETINFO_URL:
            cache = TmdbMovieCache(tmdb_id=tmdbitem['id'], imdb_id=tmdbitem['imdb_id'], title=tmdbitem['name'], released=tmdbitem['released'], updated=tmdbitem['last_modified_at'], version=tmdbitem['version'], jsondata=json.dumps(tmdbitem), timestamp=datetime.datetime.now())  
        if tmdburl == settings.TMDB_PERSONGETINFO_URL:
            cache = TmdbPersonCache(tmdb_id=tmdbitem['id'], name=tmdbitem['name'], birth=tmdbitem['birthday'], updated=tmdbitem['last_modified_at'], version=tmdbitem['version'], jsondata=json.dumps(tmdbitem), timestamp=datetime.datetime.now())  
        cache.save()
    return tmdbitem
    
def moviebrowse():
    return None

