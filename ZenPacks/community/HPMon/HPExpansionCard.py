################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPExpansionCard

HPExpansionCard is an abstraction of a PCI card.

$Id: HPExpansionCard.py,v 1.2 2011/01/04 23:11:06 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.ZenModel.ExpansionCard import ExpansionCard
from HPComponent import *

class HPExpansionCard(ExpansionCard, HPComponent):
    """ExpansionCard object"""
    status = 1

    # we don't monitor cards
    monitor = False

    _properties = ExpansionCard._properties + (
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    factory_type_information = (
        {
            'id'             : 'ExpansionCard',
            'meta_type'      : 'ExpansionCard',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addExpansionCard',
            'immediate_view' : 'viewHPExpansionCard',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPExpansionCard'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(HPExpansionCard)
