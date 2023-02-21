from django.contrib import admin
from posts_api.models import Comment, Image

# Register your models here.
admin.site.register(Image)
admin.site.register(Comment)