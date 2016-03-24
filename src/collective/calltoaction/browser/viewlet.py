# -*- coding: utf-8 -*-
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter
from zope.component import getUtility
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRetriever
from collective.calltoaction.portlets.calltoactionportlet import ICallToActionPortlet  # noqa


class CallToActionViewlet(ViewletBase):

    def update(self):
        self.data = []
        # We could iterate over all portlet managers.  That includes the
        # dashboard portlet managers, which makes no sense unless you are
        # viewing a dashboard.  By default only left and right are then
        # available.  Possibly footer portlets on Plone 5.  And there could be
        # managers from ContentWellPortlets.  We can hardcode left/right for
        # now.  Maybe fail when we get added somewhere else.
        #
        # from zope.component import getUtilitiesFor
        # list(getUtilitiesFor(IPortletManager))
        left = getUtility(IPortletManager, name='plone.leftcolumn')
        right = getUtility(IPortletManager, name='plone.rightcolumn')

        for manager in (left, right):
            retriever = getMultiAdapter(
                (self.context, manager), IPortletRetriever)
            portlets = retriever.getPortlets()
            for portlet in portlets:
                assignment = portlet['assignment']
                if not ICallToActionPortlet.providedBy(assignment):
                    continue
                # Proof of concept: we can get data from a portlet assignment
                # in the left or right portlet manager.
                self.data.append(assignment.milli_seconds_until_popup)
