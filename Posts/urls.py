from django.contrib import admin
from django.urls import path
from posts_api.views import ImageView, ImageLikeView, CommentCreateView,UserSignupView, UserLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('images/', ImageView.as_view()),
    path('images/<int:pk>/', ImageView.as_view()),
    path('images/<int:image_id>/like/', ImageLikeView.as_view()),
    path('comments/', CommentCreateView.as_view()),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]

