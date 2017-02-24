import re
import ipaddress
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from ncrawl import settings, snmp



class BaseTopologyView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(BaseTopologyView, self).get_context_data(**kwargs)
        context.update({'src_address': self.src_address()})
        return context

    def src_address(self):
        address = None
        if self.request.META:
            if 'HTTP_X_FORWARDED_FOR' in self.request.META:
                addr = unicode(self.request.META['HTTP_X_FORWARDED_FOR'].split(',')[0])
            else:
                addr = unicode(self.request.META['REMOTE_ADDR'])
            address = ipaddress.ip_address(address=addr)
        return address


class IndexView(BaseTopologyView):
    template_name = 'ncrawl/index.html'


class BaseTopologyApiView(View):
    def compute_topology(self, *args, **kwargs):
        return {}

    def trim_hostname(self, name):
        regexp = re.compile(r"\.%s" % settings.DOMAIN)
        return regexp.sub('', name)

    def sitecode(self, name):
        regexp = re.compile(settings.SITE_REGEX)
        return regexp.search(name).group('site')

    def get(self, request, *args, **kwargs):
        topology = self.compute_topology()
        response = JsonResponse(topology)
        return response


class LldpTopologyView(BaseTopologyApiView):
    def compute_topology(self):
        start_node = settings.DISC_START_NODE
        poll_queue = [start_node]
        polled = set()
        sites = set()
        nodes, links, node_sets = list(), list(), list()
        snmp_api = snmp.Api()
        mib = "LLDP-MIB"
        table = 'lldpRemTable'
        while poll_queue:
            node = poll_queue.pop()
            if node in polled:
                continue
            else:
                polled.add(node)
                try:
                    neighbors = snmp_api.get_table(mib, table, node)
                    node_name = self.trim_hostname(node)
                    site = self.sitecode(node)
                    nodes.append({'name': node_name, 'icon': 'router', 'site': site})
                    sites.add(site)
                    for index in neighbors:
                        neighbor = str(neighbors[index]["lldpRemSysName"])
                        poll_queue.append(neighbor)
                        neighbor_name = self.trim_hostname(neighbor)
                        link_matched = False
                        for link in links:
                            if link['source'] == neighbor_name and link['target'] == node_name:
                                if not link['bidi']:
                                    link['bidi'] = True
                                    link_matched = True
                                    break
                        if not link_matched:
                            link = {'source': node_name, 'target': neighbor_name, 'bidi': False}
                            links.append(link)
                except:
                    continue
        for link in links:
            if not link['bidi']:
                links.remove(link)
        for site in sites:
            node_set = {'name': site, 'nodes': [], 'icon': 'router'}
            for node in nodes:
                if node['site'] == site:
                    node_set['nodes'].append(node['name'])
            node_sets.append(node_set)
        topology = {'nodes': nodes, 'links': links, 'nodeSet': node_sets}
        return topology
