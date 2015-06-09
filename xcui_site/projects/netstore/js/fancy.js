$(document).ready(function(){
  function myFunction() {
    var x = document.lastModified;
    document.getElementById("last_modified_at").innerHTML = "&nbsp; last modified at " + x;
  }
  myFunction();
});
