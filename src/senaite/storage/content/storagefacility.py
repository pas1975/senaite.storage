# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.STORAGE
#
# Copyright 2019 by it's authors.

from Products.Archetypes.Field import StringField
from Products.Archetypes.Schema import Schema
from Products.Archetypes.Widget import StringWidget
from Products.Archetypes.atapi import registerType
from bika.lims.browser.fields.addressfield import AddressField
from bika.lims.browser.widgets.addresswidget import AddressWidget
from bika.lims.content.bikaschema import BikaFolderSchema
from bika.lims.idserver import renameAfterCreation
from plone.app.folder.folder import ATFolder
from senaite.storage import PRODUCT_NAME
from senaite.storage import senaiteMessageFactory as _
from senaite.storage.interfaces import IStorageFacility, IStorageLayoutContainer
from zope.interface import implements

Phone = StringField(
    name = 'Phone',
    widget = StringWidget(
        label = _("Phone")
    )
)

EmailAddress = StringField(
    name = 'EmailAddress',
    widget = StringWidget(
        label=_("Email Address"),
    ),
    validators = ('isEmail',)
)

Address = AddressField(
    name = 'Address',
    widget = AddressWidget(
       label=_("Address"),
       render_own_label=True,
    ),
    subfield_validators = {
        'country': 'inline_field_validator',
        'state': 'inline_field_validator',
        'district': 'inline_field_validator',
    },
)

schema = BikaFolderSchema.copy() + Schema((
    Phone,
    EmailAddress,
    Address,
))

class StorageFacility(ATFolder):
    """Physical location or place where storage containers are located
    """
    implements(IStorageFacility)
    _at_rename_after_creation = True
    displayContentsTab = False
    schema = schema

    def _renameAfterCreation(self, check_auto_id=False):
        renameAfterCreation(self)

    def getPossibleAddresses(self):
        return [Address.getName()]

    def get_layout_containers(self):
        """Returns the containers that belong to this facility and implement
        IStorageLayoutContainer
        """
        return filter(lambda obj: IStorageLayoutContainer.providedBy(obj),
                            self.objectValues())

    def get_samples_capacity(self):
        """Returns the total number of samples this facility can store
        """
        return sum(map(lambda con: con.get_samples_capacity(),
                       self.get_layout_containers()))

    def get_samples_utilization(self):
        """Returns the total number of samples this facility actually stores
        """
        return sum(map(lambda con: con.get_samples_utilization(),
                       self.get_layout_containers()))


registerType(StorageFacility, PRODUCT_NAME)
