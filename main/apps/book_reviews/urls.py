from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^books/(?P<book_id>\d+)$', views.reviews_for_book),
	url(r'^reviews/new/submit$', views.new_review_submit),
	url(r'^reviews/new$', views.new_review),
	url(r'^reviews$', views.reviews),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^register$', views.register),
    url(r'^$', views.index),
]
