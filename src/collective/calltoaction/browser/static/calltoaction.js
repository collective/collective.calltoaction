(function($) {
  "use strict";
  $(document).ready(function() {
    $('.calltoaction-portlet-wrapper').each( function() {
      // Check if the user has already seen this popup.
      // var cookiename = $(this).attr('data-cookiename');
      var cookiename = 'calltoaction';
      // Note: readCookie and createCookie are define in
      // Products/CMFPlone/skins/plone_ecmascript/cookie_functions.js
      if (!readCookie(cookiename)) {
        var timeout = $(this).attr('data-timeout');
        var el = $(this);
        setTimeout(
          function(){
            // Overlay adapted from http://jquerytools.github.io/demos/overlay/trigger.html
            el.overlay({
              // custom top position
              top: 260,
              // some mask tweaks suitable for facebox-looking dialogs
              mask: {
                // you might also consider a "transparent" color for the mask
                color: '#fff',
                // load mask a little faster
                loadSpeed: 200,
                // very transparent
                opacity: 0.5
              },
              // disable this for modal dialog-type of overlays
              closeOnClick: true,
              // load it immediately after the construction
              load: true,
              onClose: function() {
                // Set cookie to avoid showing overlay twice to the same user.
                createCookie(cookiename, 'y', 365);
              },
            });
          },
          timeout);
      };
    });
  });
})(jQuery);
