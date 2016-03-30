(function($) {
  "use strict";
  $(document).ready(function() {
    $('.calltoaction-portlet-wrapper').each( function() {
      var timeout = $(this).attr('data-timeout');
      var el = $(this);
      el.hide();
      setTimeout(function(){ el.show();}, timeout);
    });
  });
})(jQuery);
