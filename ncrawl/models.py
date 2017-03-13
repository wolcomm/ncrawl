from __future__ import unicode_literals
import re
from django.db import models
from ncrawl import settings


class Node(models.Model):
    name = models.CharField(max_length=50, unique=True)
    driver = models.CharField(max_length=20, default=settings.DEFAULT_DRIVER)

    @property
    def hostname(self):
        regexp = re.compile(r"\.%s" % settings.DOMAIN)
        return regexp.sub('', self.name)

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)


class Interface(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('node', 'name')

    def __str__(self):
        return "%s(%s-%s)" % (self.__class__.__name__, self.node.name, self.name)


class Adjacency(models.Model):
    source = models.ForeignKey(
        Interface,
        related_name='right_adjacenies',
        on_delete=models.CASCADE
    )
    target = models.ForeignKey(
        Interface,
        related_name='left_adjacencies',
        on_delete=models.CASCADE
    )
