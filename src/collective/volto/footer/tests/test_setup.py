# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.volto.footer.testing import (  # noqa: E501
    COLLECTIVE_VOLTO_FOOTER_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.volto.footer is properly installed."""

    layer = COLLECTIVE_VOLTO_FOOTER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if collective.volto.footer is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.volto.footer"))

    def test_browserlayer(self):
        """Test that ICollectiveVoltoFooterLayer is registered."""
        from collective.volto.footer.interfaces import ICollectiveVoltoFooterLayer
        from plone.browserlayer import utils

        self.assertIn(ICollectiveVoltoFooterLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_VOLTO_FOOTER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.volto.footer")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.volto.footer is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("collective.volto.footer"))

    def test_browserlayer_removed(self):
        """Test that ICollectiveVoltoFooterLayer is removed."""
        from collective.volto.footer.interfaces import ICollectiveVoltoFooterLayer
        from plone.browserlayer import utils

        self.assertNotIn(ICollectiveVoltoFooterLayer, utils.registered_layers())
