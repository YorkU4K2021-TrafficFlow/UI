function initialize() {
  var input1 = document.getElementById('from');
  new google.maps.places.Autocomplete(input1);
  var input2 = document.getElementById('to');
  new google.maps.places.Autocomplete(input2);
}

google.maps.event.addDomListener(window, 'load', initialize);
