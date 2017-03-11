from __future__ import unicode_literals
from django.db import models


class Node(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)


class Interface(models.Model):
    name = models.CharField(max_length=50, unique=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)

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
