import os
from django.core.management.base import BaseCommand
from pysnmp.hlapi import *
from ncrawl import settings


class Command(BaseCommand):
    help = 'Crawl the network for nodes and links'

    def handle(self, *args, **options):
        node = settings.DISC_START_NODE
        self.stdout.write("Beginning network discovery at %s" % node)
        snmp = SnmpEngine()
        usm = UsmUserData(
            settings.SNMP['user'],
            authKey=settings.SNMP['authPass'],
            privKey=settings.SNMP['privKey'],
            authProtocol=usmHMACSHAAuthProtocol,
            privProtocol=usmAesCfb128Protocol
        )
        obj = ObjectIdentity('LLDP-MIB', 'lldpRemTable').addAsn1MibSource(
            # os.path.dirname(os.path.realpath(__file__))
            'http://mibs.snmplabs.com/asn1/@mib@'
        )
        target = UdpTransportTarget((node, settings.SNMP['port']))
        for (errorIndication, errorStatus,
             errorIndex, varBinds) in bulkCmd(snmp, usm, target, ContextData(), 0, 25, ObjectType(obj),
                                              lexicographicMode=False, lookupMib=True):
            if errorIndication:
                raise RuntimeError(errorIndication)
            elif errorStatus:
                raise RuntimeError('%s at %s' % (errorStatus.prettyPrint(),
                                                 errorIndex and varBinds[-1][int(errorIndex) - 1] or '?'))
            else:
                for varBind in varBinds:
                    self.stdout.write(' = '.join([x.prettyPrint() for x in varBind]))
                # for (key, val) in varBinds:
                #     if not isinstance(val, EndOfMibView):
                #         (mib, name, index) = key.loadMibs('LLDP-MIB').getMibSymbol()
                #         self.stdout.write("%s %s %s = %s" % (mib, name, index, val))
