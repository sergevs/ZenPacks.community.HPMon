################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPSasPhyDrvMap

HPSasPhyDrvMap maps the cpqSasPhyDrvTable to disks objects

$Id: HPSasPhyDrvMap.py,v 1.4 2011/01/05 19:33:29 egor Exp $"""

__version__ = '$Revision: 1.4 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from HPHardDiskMap import HPHardDiskMap

class HPSasPhyDrvMap(HPHardDiskMap):
    """Map HP/Compaq insight manager DA Hard Disk tables to model."""

    maptype = "HPSasPhyDrvMap"
    modname = "ZenPacks.community.HPMon.cpqSasPhyDrv"

    snmpGetTableMaps = (
        GetTableMap('cpqSasPhyDrvTable',
                    '.1.3.6.1.4.1.232.5.5.2.1.1',
                    {
                        '.3': 'bay',
                        '.4': 'description',
                        '.5': 'status',
                        '.7': 'FWRev',
                        '.8': 'size',
                        '.10': 'serialNumber',
                        '.12': 'rpm',
                        '.15': 'hotPlug',
                        '.16': 'diskType',
                    }
        ),
    )

    diskTypes = {1: 'other',
                2: 'SAS',
                3: 'SATA',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not device.id in HPHardDiskMap.oms:
            HPHardDiskMap.oms[device.id] = []
        for oid, disk in tabledata.get('cpqSasPhyDrvTable', {}).iteritems():
            try:
                om = self.objectMap(disk)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId("HardDisk%s"%om.snmpindex).replace('.','_')
                if not getattr(om,'description',''):om.description='Unknown Disk'
                om.setProductKey = MultiArgs(om.description,
                                            om.description.split()[0])
                om.diskType = self.diskTypes.get(getattr(om, 'diskType', 1),
                                    '%s (%d)' %(self.diskTypes[1], om.diskType))
                om.rpm = self.rpms.get(getattr(om,'rpm',1), getattr(om,'rpm',1))
                om.size = getattr(om, 'size', 0) * 1048576
            except AttributeError:
                continue
            HPHardDiskMap.oms[device.id].append(om)
        return
