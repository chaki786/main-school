document.addEventListener('click', (event)=>{
    if (event.target.id == 'add-more') {
        add_new_form(event)
    }
})
function add_new_form(event) {
    if (event) {
        event.preventDefault()
    }
    const totalNewForms = document.getElementById('id_form-TOTAL_FORMS')
    const currentIngredientForms = document.getElementsByClassName('ingredient-form')
    const currentFormCount = currentIngredientForms.length // + 1
    const formCopyTarget = document.getElementById('ingredient-form-list')
    const copyEmptyFormEl = document.getElementById('empty-form').cloneNode(true)
    copyEmptyFormEl.setAttribute('class', 'ingredient-form')
    copyEmptyFormEl.setAttribute('id', `form-${currentFormCount}`)
    const regex = new RegExp('__prefix__', 'g')
    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount)
    totalNewForms.setAttribute('value', currentFormCount + 1)
    // now add new empty form element to our html form
    formCopyTarget.append(copyEmptyFormEl)
}

var countryStateInfo = {
    "India": { "Delhi": ["new Delhi"],
    "Kerala": ["Thiruvananthapuram"],
    "Andhra Pradesh": ["Hyderabad"],
    "Arunachal Pradesh": ["Itanagar"],
    "Assam": ["Guwahati"],
    "Bihar": ["Patna"],
    "Chhattisgarh": ["Naya Raipur"],
    "Goa": ["Panaji"],
    "Himachal Pradesh": ["Shimla"],
    "Jammu and Kashmir": ["Srinagar; Jammu"],
    "Jharkhand": ["Rnachi"],
    "Karnataka": ["Bengaluru"],
    "Madhya Pradesh": ["Bhopal"],
    "Maharashtra": ["Mumbai"],
    "Manipur": ["Imphal"],
    "Meghalaya": ["Shilong"],
    "Mizoram": ["Aizwal"],
    "Nagaland": ["Kohima"],
    "Odisha": ["Bhubaneswar"],
    "Punjab": ["Chandigarh"],
    "Rajasthan": ["Jaipur"],
    "Sikkim": ["Gangtok"],
    "Tamil Nadu": ["Chennai"],
    "Telangana": ["Hyderabad"],
    "Tripura": ["Agartala"],
    "Uttar Pradesh": ["Lucknow"],
    "Uttarakhand": ["Dehradun"],
    "West Bengal": ["Kolkata"],
    },
};



window.onload = function () {
var selectCountry = document.getElementById("country"),
selectState = document.getElementById("state"),
countrystatecitySelect = document.getElementById("city");
for (var country in countryStateInfo) {
selectCountry.options[selectCountry.options.length] = new Option(country, country);
}
selectCountry.onchange = function () {
selectState.length = 1; // delete all options bar earliest
countrystatecitySelect.length = 1; // delete all options bar earliest
if (this.selectedIndex < 1) return; // done 
for (var state in countryStateInfo[this.value]) {
selectState.options[selectState.options.length] = new Option(state, state);
}
}
selectCountry.onchange(); // reset in case page is reloaded
selectState.onchange = function () {
countrystatecitySelect.length = 1; // delete all options bar earliest
if (this.selectedIndex < 1) return; // done 
var region = countryStateInfo[selectCountry.value][this.value];
for (var i = 0; i < region.length; i++) {
countrystatecitySelect.options[countrystatecitySelect.options.length] = new Option(region[i], region[i]);
}
}
}


$("#profileImage").click(function() {
    $("#imageUpload").click();});
    function fasterPreview( uploader ) {
        if ( uploader.files && uploader.files[0] ){
            $('#profileImage').attr('src', 
            window.URL.createObjectURL(uploader.files[0]) );}}
            $("#imageUpload").change(function(){
                fasterPreview( this );}); 


