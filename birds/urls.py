from django.conf.urls import patterns, url


urlpatterns = patterns(
    'birds.views',
    url(r'^birds$', 'birds', name='birds_url'),
)
