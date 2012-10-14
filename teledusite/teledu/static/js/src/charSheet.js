var csrfToken = $.cookie('csrftoken');
var rxID = /[^_]*_(\d+)/;

function updateAttributeValue(attributeId, newValue) {
  var element = document.getElementById("attr_" + attributeId);
  if (element == null) {
    return;
  }
  element.innerHTML = newValue;
}

function updateAttributes(attrValues) {
  $.each(attrValues, updateAttributeValue);
}

function editValue(value, settings) {
  var id = rxID.exec(this.id)[1];

  $.ajax({
    url: window.location + '/attribute/' + id,
    type: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    data: {'value': value},
    dataType: 'json'
  })
  .done(updateAttributes)
  .fail(function() {alert("Updating attribute failed");})
  ;

  return value;
}

function createEditables() {
  $('.char_attr').editable(editValue, {cssclass: "inline-edit"});
}

$(document).ready(function() {
  createEditables();
});