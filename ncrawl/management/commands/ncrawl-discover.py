from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from ncrawl import settings
from ncrawl.snmp import Api


class Command(BaseCommand):
    help = 'Crawl the network for nodes and links'

    def handle(self, *args, **options):
        start_node = settings.DISC_START_NODE
        self.stdout.write("Beginning network discovery at %s" % start_node)
        poll_queue = [start_node]
        polled = set()
        nodes, links = set(), list()
        snmp_api = Api()
        mib = "LLDP-MIB"
        table = 'lldpRemTable'
        while poll_queue:
            node = poll_queue.pop()
            if node in polled:
                continue
            else:
                polled.add(node)
                try:
                    self.stdout.write("Finding neighbors of %s" % node)
                    neighbors = snmp_api.get_table(mib, table, node)
                    nodes.add(node)
                    for index in neighbors:
                        neighbor = str(neighbors[index]["lldpRemSysName"])
                        self.stdout.write("Found neighbor: %s" % neighbor)
                        poll_queue.append(neighbor)
                        link = {'src': node, 'dst': neighbor}
                        links.append(link)
                except:
                    self.stdout.write("failed to query %s" % node)
                    continue
        self.stdout.write(str(nodes))
        self.stdout.write(str(links))

