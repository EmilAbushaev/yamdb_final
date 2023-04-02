from django.urls import include, path
from rest_framework import routers

import api.views as av

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', av.TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    av.ReviewViewSet,
    basename='reviews',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    av.CommentViewSet,
    basename='comments',
)
router_v1.register(r'users', av.UsersViewSet)


urlpatterns = [
    path('categories/', av.CategoryList.as_view()),
    path('categories/<slug:slug>/', av.CategoryDelete.as_view()),
    path('genres/', av.GenreList.as_view()),
    path('genres/<slug:slug>/', av.GenreDelete.as_view()),
    path('', include(router_v1.urls)),
    path('auth/signup/', av.SignUp.as_view()),
    path('auth/token/', av.get_jwt_token),
]
