function insertCountryInList(country) {
  var list = $('select#mselect');
  var newOption = 
      $('<option></option>')
      .attr('value', country.code)
      .text(country.name);
  
  list.append(newOption);
  
}

var CSV_PATH = './data/test.csv';

//Note: the above CSV has the format Country Code,Country name

$.get(CSV_PATH, function (data) {
  var lines = data.split("\n");
  // Skip first row since it contains the CSV header
  lines.shift();
  
  //Transform each line of the form Country code, Country name into an object {code: xx, name: xx}

  var countries = lines.map(function (line) {
    var fields = line.split(",");
    return {
      code: fields[1], 
      name: fields[0]
    };
  });
  
  // Then append every country to our list
  countries.forEach(insertCountryInList);
});