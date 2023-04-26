function myFunction() {
    $('#myDropdown').toggleClass('show');
  }
  
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

function toggleNotifications() {
    var menu = document.getElementById("notificationMenu");
    if (menu.classList.contains("show")) {
        menu.classList.remove("show");
    } else {
        menu.classList.add("show");
    }
}

function showNotifications() {
    var menu = document.getElementById("notificationMenu");
    menu.classList.add("show");
}

function hideNotifications() {
    var menu = document.getElementById("notificationMenu");
    menu.classList.remove("show");
}

