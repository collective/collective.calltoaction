(function($) {
  "use strict";
  $(document).ready(function() {
    $('.calltoaction-portlet-wrapper').each( function() {
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
            load: true
          });
        },
        timeout);
    });
  });
})(jQuery);
