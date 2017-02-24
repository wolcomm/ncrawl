from __future__ import unicode_literals
import os
from collections import defaultdict
from pysnmp.hlapi import *
from ncrawl.settings import SNMP
from ncrawl.snmp import mibs


class Api(object):
    def __init__(self):
        self.eng = SnmpEngine()
        self.usm = UsmUserData(
            SNMP['user'],
            authKey=SNMP['authPass'],
            privKey=SNMP['privKey'],
            authProtocol=usmHMACSHAAuthProtocol,
            privProtocol=usmAesCfb128Protocol
        )
        self.ctx = ContextData()
        self.mibs = os.path.dirname(os.path.realpath(mibs.__file__))
        self.target = None
        self.obj = None

    def _set_target(self, host=None):
        self.target = UdpTransportTarget((host, SNMP['port']))
        return self

    def _set_object(self, mib=None, name=None):
        self.obj = ObjectIdentity(mib, name).addMibSource(self.mibs)
        return self

    def get_table(self, mib=None, name=None, host=None):
        self._set_target(host=host)
        self._set_object(mib=mib, name=name)
        table = defaultdict(defaultdict)
        for (err_indication, err_status, err_index, var_binds) in bulkCmd(
                self.eng, self.usm, self.target, self.ctx, 0, 25, ObjectType(self.obj),
                lexicographicMode=False, lookupMib=True):
            if err_indication:
                raise RuntimeError(err_indication)
            elif err_status:
                err = '%s at %s' % (err_status.prettyPrint(), err_index and var_binds[-1][int(err_index) - 1] or '?')
                raise RuntimeError(err)
            else:
                for (key, val) in var_binds:
                    if not isinstance(val, EndOfMibView):
                        (mib, name, indices) = key.loadMibs(mib).getMibSymbol()
                        index = '.'.join([str(i) for i in indices])
                        table[index][name] = val
        return table
