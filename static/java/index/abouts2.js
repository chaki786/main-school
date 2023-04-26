// Add options for grade dropdown
var gradeSelect = document.getElementById("grade");
for (var i = 1; i <= 12; i++) {
  var option = document.createElement("option");
  option.text = i;
  option.value = i;
  gradeSelect.add(option);
}

// Add options for section dropdown
var sectionSelect = document.getElementById("section");
var sections = ["A", "B", "C", "D", "E", "F"];
for (var i = 0; i < sections.length; i++) {
  var option = document.createElement("option");
  option.text = sections[i];
  option.value = sections[i];
  sectionSelect.add(option);
}

// Add options for roll number dropdown
var rollnoSelect = document.getElementById("rollno");
for (var i = 1; i <= 100; i++) {
  var option = document.createElement("option");
  option.text = i;
  option.value = i;
  rollnoSelect.add(option);
}
