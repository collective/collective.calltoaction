# ============================================================================
# EXAMPLE ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.calltoaction -t test_example.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.calltoaction.testing.COLLECTIVE_CALLTOACTION_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/calltoaction/tests/robot/test_example.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a visitor I do not want to see the popup initially
  Given I am on the home page
   Then I do not see the popup

Scenario: As a visitor I want to see the popup after a while
  Given I am on the home page
   When I wait a short time
   Then I do see the popup


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

I am on the home page
  Go To  ${PLONE_URL}
  Wait until page contains  Home

a login form
  Go To  ${PLONE_URL}/login_form
  Wait until page contains  Login Name
  Wait until page contains  Password


# --- WHEN -------------------------------------------------------------------

I enter valid credentials
  Input Text  __ac_name  admin
  Input Text  __ac_password  secret
  Click Button  Log in

I wait a short time
  Sleep  1.5

# --- THEN -------------------------------------------------------------------

I am logged in
  Wait until page contains  You are now logged in
  Page should contain  You are now logged in

I do not see the popup
  Element Should Not Be Visible  css=.portletCallToActionPortlet

I do see the popup
  Element Should Be Visible  css=.portletCallToActionPortlet
