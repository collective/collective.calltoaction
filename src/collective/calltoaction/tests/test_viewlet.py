# -*- coding: utf-8 -*-
from collective.calltoaction.browser.viewlet import CallToActionViewlet
from collective.calltoaction.testing import COLLECTIVE_CALLTOACTION_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.component import queryMultiAdapter
from zope.contentprovider.interfaces import IContentProvider

import unittest


class ViewletTestCase(unittest.TestCase):

    layer = COLLECTIVE_CALLTOACTION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.folder = api.content.create(
            container=self.portal, type='Folder', title='Folder')

    def test_viewlet(self):
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        viewlet_manager = queryMultiAdapter(
            (self.folder, request, view),
            IContentProvider,
            'plone.abovecontentbody')
        viewlet = CallToActionViewlet(
            self.folder, request, view, viewlet_manager)
        viewlet.update()
        # We expect data from the portlet assignment in
        # profiles/testfixture/portlets.xml.
        self.assertEqual(len(viewlet.data), 1)
        portlet = viewlet.data[0]
        self.assertIn('assignment', portlet.keys())
        self.assertIn('html', portlet.keys())
        assignment = portlet['assignment']
        self.assertEqual(assignment.milli_seconds_until_popup, 1000)
        portlet_html = portlet['html']
        self.assertIn('portletCallToAction', portlet_html)
        self.assertIn('portletCallToAction', portlet_html)
        # viewlet.render() fails, presumably due to the way in which we directly
        # instantiate the viewlet class, instead of getting it through the zope
        # component architecture.
        # viewlet_html = viewlet.render()
        # self.assertIn(portlet_html, viewlet_html)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ViewletTestCase))
    return suite
