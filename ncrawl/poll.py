from napalm_ios import IOSDriver
from ncrawl import models, settings


class Poller(object):
    def __init__(self, node=None):
        if not isinstance(node, models.Node):
            raise TypeError()
        self.node = node
        self.device = IOSDriver(
            hostname=self.node.name,
            username=settings.SSH['user'],
            password=settings.SSH['pass'],
            optional_args={'secret': settings.SSH['enable']}
        )

    def __enter__(self):
        self.device.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.device.close()

    def get_lldp_neighbors(self):
        neighbors = self.device.get_lldp_neighbors_detail()
        remote_nodes = set()
        for i in neighbors:
            src_interface = models.Interface.objects.get_or_create(name=i, node=self.node.id)
            for a in neighbors[i]:
                remote_node = models.Node.objects.get_or_create(name=a['remote_system_name'])
                dst_interface = models.Interface.objects.get_or_create(name=a['remote_port'], node=remote_node.id)
                try:
                    models.Adjacency.objects.get(source=src_interface.id, target=dst_interface.id)
                except models.Adjacency.DoesNotExist:
                    adj = models.Adjacency.objects.create(source=src_interface, target=dst_interface)
                    adj.save()
                remote_nodes.add(remote_node)
        return remote_nodes
