from django.conf.urls import url, include
from ncrawl.views import IndexView, LldpTopologyView

topology_urls = [
    url(r'^lldp/$', LldpTopologyView.as_view(), name='lldp-topology')
]
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='ncrawl-index'),
    url(r'^topology/', include(topology_urls))
]