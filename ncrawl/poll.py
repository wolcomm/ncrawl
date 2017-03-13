import re
from napalm_base import get_network_driver
from ncrawl import models, settings


class Poller(object):
    def __init__(self, node=None):
        if not isinstance(node, models.Node):
            raise TypeError()
        self.node = node
        driver = get_network_driver(self.node.driver)
        self.device = driver(
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
                remote_name = a['remote_system_name']
                remote_description = a['remote_system_description']
                remote_port = a['remote_port']
                if not self._local_domain(remote_name) and settings.IGNORE_FOREIGN:
                    continue
                remote_type = self._identify_system_type(remote_description)
                remote_node = models.Node.objects.get_or_create(name=remote_name, driver=remote_type)[0]
                dst_interface = models.Interface.objects.get_or_create(name=remote_port, node=remote_node)[0]
                adj = models.Adjacency.objects.get_or_create(source=src_interface, target=dst_interface)[0]
                remote_nodes.add(remote_node)
        return list(remote_nodes)

    def _identify_system_type(self, system_descr=None):
        system_type = settings.DEFAULT_DRIVER
        type_map = {
            'ios': r"^Cisco IOS Software",
            'eos': r"^Arista Networks EOS"
        }
        for t in type_map:
            match = re.search(type_map[t], system_descr)
            if match:
                system_type = t
                break
        return system_type

    def _local_domain(self, system_name=None):
        local_domain = False
        match = re.search(r"\.%s" % settings.DOMAIN, system_name)
        if match:
            local_domain = True
        return local_domain

    def _infer_site(self, system_name=None):
        regexp = re.compile(settings.SITE_REGEX)
        return regexp.search(system_name).group('site')
