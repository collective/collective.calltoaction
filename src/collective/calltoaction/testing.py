# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.calltoaction


class CollectiveCalltoactionLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.calltoaction)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.calltoaction:default')
        applyProfile(portal, 'collective.calltoaction:testfixture')


COLLECTIVE_CALLTOACTION_FIXTURE = CollectiveCalltoactionLayer()


COLLECTIVE_CALLTOACTION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CALLTOACTION_FIXTURE,),
    name='CollectiveCalltoactionLayer:IntegrationTesting'
)


COLLECTIVE_CALLTOACTION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CALLTOACTION_FIXTURE,),
    name='CollectiveCalltoactionLayer:FunctionalTesting'
)


COLLECTIVE_CALLTOACTION_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_CALLTOACTION_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveCalltoactionLayer:AcceptanceTesting'
)
