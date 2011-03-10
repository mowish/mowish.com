from mowish.app.models import *
from django.core.mail import send_mail
from django.conf import settings

from hashlib import sha1
import random
import datetime

import mowish.app.feeds.tmdb as tmdb
import mowish.app.feeds.tastekid as tastekid

def adduser(email, password):
    encoded_password = encodepass(password)      
    user = User(
                email=email, 
                password=encoded_password, 
                status="registered",
                timestamp=datetime.datetime.now())
    user.save()
    
    sendactivation(user, password)

def activateuser(key):
    activation = UserActivation.objects.filter(activationkey=key)[0]
    user = activation.user
    
    expired = False
    if datetime.datetime.today() < activation.expires:
        user.status="active"
        user.save()
        activation.delete()
    else:
        activation.delete()
        user.delete()
        expired = True
        
    return expired
        
def login(email, password):
    user = User.objects.filter(email=email)
    if user:
        user = user[0]
        userpass = user.password
        loginpass = encodepass(password)
        if userpass == loginpass:
            return user.id

def addmovie(user_id, tmdb_id, imdb_id, title, released):
    movie = UserList.objects.filter(tmdb_id=tmdb_id)
    if movie:
        return False
    userlist = UserList(user=User(id=user_id), tmdb_id=tmdb_id, title=title, rating='', status='list', timestamp=datetime.datetime.now())
    userlist.save()
    
    toplist = TopList.objects.filter(tmdb_id=tmdb_id)
    if toplist:
        toplist = toplist[0]
        toplist.listed = toplist.listed + 1
    else:
        toplist = TopList(tmdb_id=tmdb_id, listed=1, liked=0)
    toplist.save()
    
    return True

def mylist(user_id):
    movielist = UserList.objects.filter(user__id=user_id, status='list')
    list = []
    for item in movielist:
        movie = tmdb.moviegetinfo(item.tmdb_id)
        list.append(movie)
    return list

def setmovierating(user_id, tmdb_id, rating):
    userlistmovie = UserList.objects.filter(user__id=user_id, tmdb_id=tmdb_id)[0]
    userlistmovie.rating = rating
    userlistmovie.save()
    
    if rating == 'good':
        toplist = TopList.objects.filter(tmdb_id=tmdb_id)[0]
        toplist.liked = toplist.liked + 1
        toplist.save()

    updateprofile(user_id, tmdb_id)

def setmoviestatus(user_id, tmdb_id, status):
    movie = UserList.objects.filter(user__id=user_id, tmdb_id=tmdb_id)[0]
    movie.status = status
    movie.save()

def myprofile(user_id):
    gup = GenreUserProfile.objects.filter(user__id=user_id).order_by('-weight')
    aup = ActorUserProfile.objects.filter(user__id=user_id).order_by('-weight')
    dup = DirectorUserProfile.objects.filter(user__id=user_id).order_by('-weight')
    return gup, aup, dup

def sendactivation(user, password):
    activationkey = getactivationkey(user.email)
    expires = datetime.datetime.today() + datetime.timedelta(settings.REGISTRATION_EXPIRES)
    
    activation = UserActivation(user=user, activationkey=activationkey, expires=expires)
    activation.save()

    data = {'email': user.email, 'password': password, 'site_url': settings.SITE_URL, 'activationkey': activationkey}

    file = open(settings.PROJECT_ROOT + '/templates/user_activation_email.txt')
    template = file.read()
    file.close()
        
    mail_body = template % data 
    mail_subject = unicode('mowish.com user activation: ', 'utf-8') + user.email  
    
    send_mail(mail_subject, mail_body, settings.INFO_EMAIL, [user.email], fail_silently=False)

def updateprofile(user_id, tmdb_id):
    movie = tmdb.moviegetinfo(tmdb_id)
    
    for genre in movie['genres']:
        genre = genre['name']
        gup = GenreUserProfile.objects.filter(user__id=user_id, genre=genre)
        if gup: 
            gup = gup[0]
            gup.weight = gup.weight + 1
        else:
            gup = GenreUserProfile(user=User(id=user_id), genre=genre, weight=1)
        gup.save()            
            
    for cast in movie['cast']:
        name = cast['name']
        if (cast['order'] == 0 or cast['order'] == 1) and cast['job'] == 'Actor':    
            aup = ActorUserProfile.objects.filter(user__id=user_id, actor=name)
            if aup:
                aup = aup[0]
                aup.weight = aup.weight + 1
            else:
                aup = ActorUserProfile(user=User(id=user_id), actor=name, weight=1)
            aup.save()
        if cast['job'] == 'Director':
            dup = DirectorUserProfile.objects.filter(user__id=user_id, director=name)
            if dup:
                dup = dup[0]
                dup.weight = dup.weight + 1
            else:
                dup = DirectorUserProfile(user=User(id=user_id), director=name, weight=1)
            dup.save()

def moviesfrom(person_id):
    person = tmdb.persongetinfo(person_id)
    movies = []
    for movie in person['filmography']:
        tmdbmovie = tmdb.moviegetinfo(str(movie['id']))
        movies.append(tmdbmovie)
    return movies

def recommendations(loggedin_id, search_term, last_search, search_type):
    
    titles = ''
    if search_term:
        # search result page
        if search_type == 'movie':
            titles = search_term
        else:
            # TODO searched for person; get movies from actor?
            titles = '2010' 
    else:
        if loggedin_id:
            # search result page, logged in
            # he likes some movies already
            usermovies = UserList.objects.filter(user__id=loggedin_id, rating='good')
            if not usermovies: 
                # no movies that he likes yet, so take the whole list
                usermovies = UserList.objects.filter(user__id=loggedin_id, status='list')    
            for movie in usermovies:
                titles += movie.title + ','   
        else:
            # not logged in and not on search result page (for e.g. landing page)
            if last_search:
                # has saved search in cookie
                titles = last_search
            else:
                # no cookie, not logged in, no previous search
                # TODO toplist, or other users
                titles = '2010'         
        
    return getmoviesbytitle(titles)

def getmoviesbytitle(titles):
    titles = titles.replace(' ', '%20')
    # TODO refactor tastekid from here
    movies = tastekid.movies(titles)
    # TODO toplist, or other users
    if not movies:
        movies = [{"Name": "2010"}]
    list = []
    for movie in movies:
        tmdbmovie = tmdb.moviesearch(movie['Name'].replace(' ', '%20'))
        if tmdbmovie:
            list.append(tmdbmovie[0])        
    
    return list

def toplist():
    # TODO only movies that has liked > 0
    toplist = TopList.objects.all().order_by('-liked')[:6]
    list = []
    for movie in toplist:        
        movie = tmdb.moviegetinfo(movie.tmdb_id)
        list.append(movie)
        
    return list

def encodepass(password):
    sha = sha1()
    sha.update(password)
    encodedpass = sha.hexdigest()
    return encodedpass
    
def getactivationkey(email):
    salt = sha1(str(random.random())).hexdigest()[:5]
    activationkey = sha1(salt+email).hexdigest()
    return activationkey
    
