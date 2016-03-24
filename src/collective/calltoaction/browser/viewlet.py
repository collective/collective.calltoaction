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
        # We could iterate over all portlet managers.  But this includes the
        # dashboard portlet managers, which makes no sense unless you are
        # viewing a dashboard.  By default only left and right are then
        # available.  Possibly footer portlets on Plone 5.  And there could be
        # managers from ContentWellPortlets.  We can hardcode left/right for
        # now.  Maybe fail when we get added somewhere else.  We do that now in
        # the Assignment class.
        #
        # from zope.component import getUtilitiesFor
        # for manager_id, manager in getUtilitiesFor(IPortletManager):
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
                # Proof of concept: we can get data from a portlet assignment
                # in the left or right portlet manager.
                self.data.append(assignment.milli_seconds_until_popup)
