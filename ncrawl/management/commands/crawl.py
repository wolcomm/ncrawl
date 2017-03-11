from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from ncrawl import models, poll


class Command(BaseCommand):
    help = 'Crawl the network for nodes and links'

    def add_arguments(self, parser):
        parser.add_argument('start_node', type=str)

    def handle(self, *args, **options):
        try:
            self.stdout.write("Trying to get starting node %s." % options['start_node'])
            start_node = models.Node.objects.get(name=options['start_node'])
            self.stdout.write("Found starting node %s." % start_node)
        except models.Node.DoesNotExist:
            self.stdout.write("Starting node not found, creating it instead.")
            start_node = models.Node.objects.create(name=options['start_node'])
            start_node.save()
            self.stdout.write("Created starting node %s" % start_node)
        queue = [start_node]
        polled = set()
        while queue:
            self.stdout.write("Getting next node from polling queue.")
            node = queue.pop()
            if node in polled:
                self.stdout.write("Node %s already polled. Skipping.")
                continue
            else:
                self.stdout.write("Polling for neighbors of node %s" % node)
                with poll.Poller(node=node) as poller:
                    neighbors = poller.get_lldp_neighbors()
                self.stdout.write("Found %d neighbors of node %s" % (len(neighbors), node))
                queue.append(neighbors)
            self.stdout.write("Finished polling node %s. %d nodes still queued." % (node, len(queue)))
            continue
        self.stdout.write("Crawl completed.")
