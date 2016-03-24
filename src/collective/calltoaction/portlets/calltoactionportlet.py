# -*- coding: utf-8 -*-
from collective.calltoaction import _
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.formlib import form
from zope.interface import implements


class ICallToActionPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    milli_seconds_until_popup = schema.Int(
        title=_(u"Milliseconds until popup"),
        description=_(
            u"The number of milliseconds we wait before showing the popup."),
        default=0,
        required=True)

    # image, title, body


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ICallToActionPortlet)

    milli_seconds_until_popup = 0

    def __init__(self, milli_seconds_until_popup=0):
        self.milli_seconds_until_popup = milli_seconds_until_popup

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Call to action portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.

    We want to show nothing here by default.  The rendering should be
    handled by a viewlet.  Reason: if this is the only available
    portlet, then a portlet column will be shown even though we do not
    want to show anything initially.  Our content is only meant to be
    shown in a popup.

    We do keep the 'render' method, so the viewlet can call this.
    """

    render = ViewPageTemplateFile('calltoactionportlet.pt')

    @property
    def available(self):
        return 'debug_calltoaction' in self.request


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ICallToActionPortlet)

    def create(self, data):
        path = '/'.join(self.context.getPhysicalPath())
        if not ('plone.leftcolumn' in path or 'plone.rightcolumn' in path):
            raise ValueError('Sorry, this portlet is only supported '
                             'in left and right columns.')
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ICallToActionPortlet)
