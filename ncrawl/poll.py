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
            src_interface = models.Interface.objects.get_or_create(name=i, node=self.node)[0]
            for a in neighbors[i]:
                remote_node = models.Node.objects.get_or_create(name=a['remote_system_name'])[0]
                dst_interface = models.Interface.objects.get_or_create(name=a['remote_port'], node=remote_node)[0]
                adj = models.Adjacency.objects.get_or_create(source=src_interface, target=dst_interface)[0]
                remote_nodes.add(remote_node)
        return list(remote_nodes)
