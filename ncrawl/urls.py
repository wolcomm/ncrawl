from django.conf.urls import url, include
from ncrawl.views import IndexView, LldpGraphTopology

topology_urls = [
    url(r'^lldp/$', LldpGraphTopology.as_view(), name='lldp-topology')
]
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='ncrawl-index'),
    url(r'^topology/', include(topology_urls))
]