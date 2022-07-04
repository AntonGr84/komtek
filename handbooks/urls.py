from django.urls import path, re_path
from handbooks.views import (
    HandbookList,
    ElementsList
)

urlpatterns = [
    path('handbook/', HandbookList.as_view()),
    re_path(
        r'^handbook/(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$',
        HandbookList.as_view()
    ),
    re_path(
        r'^handbook/(?P<handbook>[0-9]+)/$',
        ElementsList.as_view()
    ),
    re_path(
        r'^handbook/(?P<handbook>[0-9]+)/(?P<version>[0-9]+\.[0-9]+)/$',
        ElementsList.as_view()
    ),
]
