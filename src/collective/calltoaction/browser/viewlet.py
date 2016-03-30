# -*- coding: utf-8 -*-
from collective.calltoaction.portlets.calltoactionportlet import ICallToActionPortlet  # noqa
from plone.app.layout.viewlets.common import ViewletBase
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletRetriever
from zope.component import getMultiAdapter
from zope.component import getUtility


class CallToActionViewlet(ViewletBase):

    def update(self):
        self.data = []
        left = getUtility(IPortletManager, name='plone.leftcolumn')
        right = getUtility(IPortletManager, name='plone.rightcolumn')
        # For Plone 5 this can be nice:
        # footer = getUtility(IPortletManager, name='plone.footerportlets')
        # But portlets in Plone 5 need to be based on z3c.form, so it may be
        # tricky to support Plone 4 and 5 with the same code base.

        for manager in (left, right):
            retriever = getMultiAdapter(
                (self.context, manager), IPortletRetriever)
            portlets = retriever.getPortlets()
            for portlet in portlets:
                assignment = portlet['assignment']
                if not ICallToActionPortlet.providedBy(assignment):
                    continue
                renderer = self._data_to_portlet(manager, assignment.data)
                html = renderer.render()
                info = {
                    'assignment': assignment,
                    'html': html,
                }
                self.data.append(info)

    def _data_to_portlet(self, manager, data):
        """Helper method to get the correct IPortletRenderer for the given
        data object.

        Adapted from plone.portlets/manager.py _dataToPortlet.
        """
        return getMultiAdapter((self.context, self.request, self.view,
                                manager, data, ), IPortletRenderer)
