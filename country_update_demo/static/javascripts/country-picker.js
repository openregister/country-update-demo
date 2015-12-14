//Copied from widgets demo https://raw.githubusercontent.com/openregister/widgets-demo/master/widgets/static/javascripts/country-picker.js
var initAutoComplete = function() {
    $('.auto-suggest').selectToAutocomplete();
};

var renderCountries = function(countries) {
    var template = $.templates("#country-template");
    $.each(countries, function(index, country) {
        var html = template.render({
                    'country': country.country,
                    'name': country.name
        });
        $('#country-selector').append(html);
    });
    initAutoComplete();
};

var loadCountries = function() {
    $.ajax({
      type: 'GET',
      url: '/countries.json',
      contentType: 'application/json',
      success: function(data) {
        renderCountries(data['entries']);
      },
      error: function(xhr, options, error) {
            console.log(error);
      }
    });
};

$(document).ready(function() {
    loadCountries();
});
