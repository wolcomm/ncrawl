from django.conf.urls import url
from ncrawl.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='ncrawl-index')
]