var csrfToken = $.cookie('csrftoken');
var rxID = /[^_]*_(\d+)/;

$(document).ready(function() {
  $('.char_attr').editable(window.location + '/attribute', {
      ajaxoptions: {headers: {'X-CSRFToken': csrfToken}},
      cssclass: "inline-edit",
      submitdata: function(value, settings) {
        var id = rxID.exec(this.id)[1];
        settings.target += '/' + id
      }
    }
  );
});