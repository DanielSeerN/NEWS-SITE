from django.contrib import admin
from .models import *


admin.site.register(NewsArticle)
admin.site.register(Reader)
admin.site.register(FavouriteArticle)
admin.site.register(SourceCategory)


# Register your models here.
