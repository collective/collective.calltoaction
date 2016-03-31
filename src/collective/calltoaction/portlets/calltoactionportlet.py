# -*- coding: utf-8 -*-
from collective.calltoaction import _
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.portlet.static import static
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getUtility
from zope.formlib import form
from zope.interface import implements

import random
import string


def random_version():
    return ''.join(random.sample(string.ascii_letters, 16))


class ICallToActionPortlet(static.IStaticPortlet):
    """A portlet deriving from the static text portlet.
    """

    milli_seconds_until_popup = schema.Int(
        title=_(u'Milliseconds until popup'),
        description=_(
            u'The number of milliseconds we wait before showing the popup.'),
        default=0,
        required=True)

    new_version = schema.Bool(
        title=_(u'This is a new call to action'),
        description=_(
            u'Checking this option means everyone will get to see the new '
            u'popup. When not checked, visitors who have already seen '
            u'the popup will not see it again.'),
        default=False,
        required=False)


class Assignment(static.Assignment):
    """Portlet assignment.
    """

    implements(ICallToActionPortlet)

    header = _(u'title_call_to_action_portlet',
               default=u'Call to action portlet')
    milli_seconds_until_popup = 0
    new_version = False
    version = ''

    def __init__(self, **kwargs):
        self.milli_seconds_until_popup = kwargs.pop(
            'milli_seconds_until_popup', 0)
        self.new_version = kwargs.pop(
            'new_version', False)
        super(Assignment, self).__init__(**kwargs)
        self.version = random_version()

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        'manage portlets' screen. Here, we use the title that the user gave or
        static string if title not defined.
        """
        return self.header or _(
            u'title_call_to_action_portlet',
            default=u'Call to action portlet')


class Renderer(static.Renderer):
    """Portlet renderer.

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

    def css_class(self):
        """Generate a CSS class from the portlet header
        """
        header = self.data.header
        if header:
            normalizer = getUtility(IIDNormalizer)
            return "portlet-calltoaction-%s" % normalizer.normalize(header)
        return "portlet-calltoaction"


class AddForm(static.AddForm):
    """Portlet add form."""
    form_fields = form.Fields(ICallToActionPortlet)
    form_fields['text'].custom_widget = WYSIWYGWidget
    form_fields = form_fields.omit('new_version')
    label = _(
        u'title_add_calltoaction_portlet',
        default=u'Add call to action portlet')
    description = _(
        u'description_calltoaction_portlet',
        default=u'A portlet which displays a call to action popup '
        'after waiting for some seconds.')

    def create(self, data):
        path = '/'.join(self.context.getPhysicalPath())
        if not ('plone.leftcolumn' in path or 'plone.rightcolumn' in path):
            raise ValueError('Sorry, this portlet is only supported '
                             'in left and right columns.')
        return Assignment(**data)


class EditForm(static.EditForm):
    """Portlet edit form.
    """
    form_fields = form.Fields(ICallToActionPortlet)
    form_fields['text'].custom_widget = WYSIWYGWidget
    label = _(
        u'title_edit_calltoaction_portlet',
        default=u'Edit call to action portlet')
    description = _(
        u'description_calltoaction_portlet',
        default=u'A portlet which displays a call to action popup '
        'after waiting for some seconds.')

    def __call__(self):
        result = super(EditForm, self).__call__()
        assignment = self.context
        if assignment.new_version:
            assignment.new_version = False
            assignment.version = random_version()
        return result
