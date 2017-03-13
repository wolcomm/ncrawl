from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from ncrawl import models


class Command(BaseCommand):
    help = 'Clean out all nodes before a fresh crawl'

    def handle(self, *args, **options):
        nodes = models.Node.objects.all()
        self.stdout.write("Deleting %d nodes." % nodes.count())
        for n in nodes:
            n.delete()
        self.stdout.write("Deleted all nodes.")
