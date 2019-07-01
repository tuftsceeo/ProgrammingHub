function PressEnter(e,FormID) { // Submit form if Enter Key is pressed
  if ( (window.event ? event.keyCode : e.which) == 13) {
    document.getElementById(FormID).submit();
  }
}
function submit(FormID) { // Submit form based on form ID
    document.getElementById(FormID).submit();
}
function setValue() { // setValue changes the selected item in dropdown menu based on current page being served
    var x = document.getElementById('page').innerHTML;
    var index = "0";
    if (x == 'simplePage') {
      index="0";
    } else if (x == 'page2') {
      index="1";
    } else {
      index="0";
    }
    document.getElementById("pageSelect").selectedIndex = index;
}
function getValue() { // getValue used to test the ability to get the value of the selected page
   var x = document.getElementById("pageSelect").selectedIndex;
   alert(document.getElementsByTagName("option")[x].value);
}