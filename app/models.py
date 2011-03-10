from django.db import models

class User(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=40)
    status = models.CharField(max_length=20)
        
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return self.email

class UserActivation(models.Model):
    user = models.ForeignKey(User)
    activationkey = models.CharField(max_length=40)
    expires = models.DateTimeField()
    
class UserList(models.Model):
    user = models.ForeignKey(User)
    tmdb_id = models.CharField(max_length=20)
    title = models.CharField(max_length=40)
    rating = models.CharField(max_length=5)
    status = models.CharField(max_length=20)
    
    timestamp = models.DateTimeField()

class TopList(models.Model):
    tmdb_id = models.CharField(max_length=20)
    liked = models.IntegerField()
    listed = models.IntegerField()
    
class TmdbMovieCache(models.Model):
    tmdb_id = models.CharField(max_length=20)
    imdb_id = models.CharField(max_length=20, blank=True)    
    title = models.CharField(max_length=50)
    released = models.CharField(max_length=20)
    updated = models.DateTimeField()
    version = models.IntegerField()
    jsondata = models.TextField()
    timestamp = models.DateTimeField()

class TmdbPersonCache(models.Model):
    tmdb_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    birth = models.CharField(max_length=20)
    updated = models.DateTimeField()
    version = models.IntegerField()
    jsondata = models.TextField()
    timestamp = models.DateTimeField()
    
# class TastekidCache(models.Model):
    
class ActorUserProfile(models.Model):
    actor = models.CharField(max_length=40)
    user = models.ForeignKey(User)
    weight = models.IntegerField()
    
class DirectorUserProfile(models.Model):
    director = models.CharField(max_length=40)
    user = models.ForeignKey(User)
    weight = models.IntegerField()
    
class GenreUserProfile(models.Model):
    genre = models.CharField(max_length=40)
    user = models.ForeignKey(User)
    weight = models.IntegerField() 
