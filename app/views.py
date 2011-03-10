from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.conf import settings

import middleware
import mowish.app.feeds.tmdb as tmdb

def index(request):
    return render_to_response('base.html', context_instance=RequestContext(request))

def person(request, person_id, slug):
    person = tmdb.persongetinfo(person_id)
    return render_to_response('person.html', {'person': person}, context_instance=RequestContext(request))
    
    
def user_add(request):    
    middleware.adduser(request.POST['email'], request.POST['password'])
    return render_to_response('message.html', {'status': 'emailsent'}, context_instance=RequestContext(request))

    
def user_activate(request, key):
    expired = middleware.activateuser(key)
    status = ''
    if expired:
        status = 'expired'
    else:    
        status = 'activated'
    return render_to_response('message.html', {'status': status}, context_instance=RequestContext(request))
  
    
def user_login(request):
    user_id = middleware.login(
                request.POST["email"],
                request.POST["password"],
            )

    response = None
    if user_id:
        request.session['loggedin_email'] = request.POST['email']
        request.session['loggedin_id'] = user_id
        response = redirect('my_list')
    else:
        response = render_to_response('base.html', {'failed': True}, context_instance=RequestContext(request))       

    return response
   
     
def user_logout(request):
    del request.session["loggedin_email"]
    del request.session["loggedin_id"]
    return redirect('index')   
    

def movie(request, movie_id, slug):
    movie = tmdb.moviegetinfo(movie_id)
    return render_to_response('movie.html', {'movie': movie}, context_instance=RequestContext(request))

    
def movie_add(request):    
    middleware.addmovie(request.session['loggedin_id'], request.GET['tmdb_id'], request.GET['imdb_id'], request.GET['title'], request.GET['released'])
    return redirect('my_list')    

    
def movie_rate(request, tmdb_id, rating):
    if rating == 'good':
        middleware.setmovierating(request.session['loggedin_id'], tmdb_id, rating)
    if rating == 'bad':
        middleware.setmovierating(request.session['loggedin_id'], tmdb_id, rating)
    
    return redirect('my_list')


def movie_status(request, tmdb_id, status):
    if status == 'removed':
        middleware.setmoviestatus(request.session['loggedin_id'], tmdb_id, status)
    return redirect('my_list')
    
    
def my_profile(request):
    gup, aup, dup = middleware.myprofile(request.session['loggedin_id'])
    return render_to_response('myprofile.html', {'gup': gup, 'aup': aup, 'dup': dup}, context_instance=RequestContext(request))    
  
    
def my_list(request):
    data = middleware.mylist(request.session['loggedin_id'])
    return render_to_response('mylist.html', {'data': data}, context_instance=RequestContext(request))
   

def movies_list(request):
    search_term = request.GET['search_term']
    search_type = request.GET['search_type']
    # TODO remove and check emtpy search field from JS
    if not search_term:
        return render_to_response('resultlist.html', {'data': ['Nothing found.']}, context_instance=RequestContext(request))

    data = None
    if search_type == 'movie':
        data = tmdb.moviesearch(search_term)
    if search_type == 'person':
        data = tmdb.personsearch(search_term)

    response = render_to_response('resultlist.html', {'data': data, 'search_term': search_term, 'search_type': search_type}, context_instance=RequestContext(request)) 
    response.set_cookie('last_search', search_term)            
    response.set_cookie('last_search_type', search_type)    
    return response
    
    
def movies_recommendations(request):
    loggedin_id = None
    if 'loggedin_id' in request.session:
        loggedin_id = request.session['loggedin_id']

    search_type = None
    search_term = None
    if 'search_term' in request.GET:
        search_term = request.GET['search_term']
        search_type = request.GET['search_type']

    last_search = None
    if 'last_search' in request.COOKIES:
        last_search = request.COOKIES['last_search'] 
        search_type = request.COOKIES['last_search_type']
        
    data = middleware.recommendations(loggedin_id, search_term, last_search, search_type)
    return render_to_response('thumblist.html', {'data': data}, context_instance=RequestContext(request))
   
   
def movies_toplist(request):
    data = middleware.toplist()
    return render_to_response('thumblist.html', {'data': data}, context_instance=RequestContext(request))    


def movies_from(request, person_id, slug):
    movies = middleware.moviesfrom(person_id)
    return render_to_response('resultlist.html', {'data': movies}, context_instance=RequestContext(request)) 
    
    