var csrfToken = $.cookie('csrftoken');
var rxID = /[^_]*_(\d+)/;

$(document).ready(function() {
  $('.char_attr').editable(window.location + '/setAttribute', {
      ajaxoptions: {headers: {'X-CSRFToken': csrfToken}},
      cssclass: "inline-edit",
      submitdata: function(value, settings) {
        return {id: rxID.exec(this.id)[1]};
      }
    }
  );
});