from mowish.app.models import *

from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
   list_display = ('email', 'password', 'status', 'timestamp')
   search_fields = []
   list_filter = []

class UserActivationAdmin(admin.ModelAdmin):
   list_display = ('user', 'activationkey', 'expires')
   search_fields = []
   list_filter = []
   
class UserListAdmin(admin.ModelAdmin):
   list_display = ('user', 'tmdb_id', 'rating', 'status', 'timestamp')
   search_fields = []
   list_filter = []

class TopListAdmin(admin.ModelAdmin):
   list_display = ('tmdb_id', 'liked', 'listed')
   search_fields = []
   list_filter = []
   
class TmdbMovieCacheAdmin(admin.ModelAdmin):
   list_display = ('tmdb_id', 'imdb_id', 'title', 'released', 'updated', 'version', 'jsondata', 'timestamp')
   search_fields = []
   list_filter = []

class TmdbPersonCacheAdmin(admin.ModelAdmin):
   list_display = ('tmdb_id', 'name', 'birth', 'updated', 'version', 'jsondata', 'timestamp')
   search_fields = []
   list_filter = []
   
class ActorUserProfileAdmin(admin.ModelAdmin):
   list_display = ('actor', 'user', 'weight')
   search_fields = []
   list_filter = []
   
class DirectorUserProfileAdmin(admin.ModelAdmin):
   list_display = ('director', 'user', 'weight')
   search_fields = []
   list_filter = []
   
class GenreUserProfileAdmin(admin.ModelAdmin):
   list_display = ('genre', 'user', 'weight')
   search_fields = []
   list_filter = []
   
admin.site.register(User, UserAdmin)
admin.site.register(UserActivation, UserActivationAdmin)
admin.site.register(UserList, UserListAdmin)
admin.site.register(TopList, TopListAdmin)
admin.site.register(TmdbMovieCache, TmdbMovieCacheAdmin)
admin.site.register(TmdbPersonCache, TmdbPersonCacheAdmin)
admin.site.register(ActorUserProfile, ActorUserProfileAdmin)
admin.site.register(DirectorUserProfile, DirectorUserProfileAdmin)
admin.site.register(GenreUserProfile, GenreUserProfileAdmin)


