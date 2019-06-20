<!DOCTYPE html>
<html>
<body style="width:960px; margin: 20px auto;">
<aside style="float:right;width:525px;">
 <br><br><br>
 <textarea rows="20" cols="80" id="TerminalWindow" name="TerminalWindow" spellcheck="false" style = "resize:none" placeholder="Terminal Window Will Activate When Device is Connected" readonly>%s</textarea><br>
<script type="text/javascript">
function loadXMLDoc() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      xmlDoc = this.responseText;
      document.getElementById("TerminalWindow").innerHTML =
      xmlDoc.split("terminalContent>")[2].split("</")[0];
    }
  };
  xhttp.open("GET", "note.xml", true);
  xhttp.send();
  console.log("Reload"); 
}
    setInterval(loadXMLDoc, 1000); // Time in milliseconds
</script>
<!-- <script>
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    myFunction(this);
    }
};
xhttp.open("GET", "note.xml", true);
xhttp.send();

function myFunction(xml) {
    var xmlDoc = xml.responseXML;
    document.getElementById("TerminalWindow").innerHTML =
    xmlDoc//.getElementsByTagName("TITLE")[0].childNodes[0].nodeValue;
    console.log("Reload"); 
}
</script> -->
 <form id="command" action="/EnterCommand" method="POST" onkeydown="PressEnter(event,'command')">
<input type="text" name="SendCommand" value="" spellcheck="false" placeholder="Enter Command" size="65"
autocomplete="off" autofocus="autofocus">
<input type="submit" id="SendCommand" name="SendCommand" value="Send Command">
 <input type="text" name="SendCommand" value="" hidden="hidden">
 </form>
<form action="/" method="POST">
     <input type="submit" name="Clear" value="Clear Terminal">
     <input type="submit" name="Refresh" value="Refresh Terminal">
 </form>
 <script> // Automatically scroll the textbox to the bottom
    var textarea = document.getElementById("TerminalWindow");
    textarea.scrollTop = textarea.scrollHeight;
 </script>
</aside>
<h1>Programming Hub</h1>
<h4 hidden id = "page">%s</h4>
<h4 hidden id = "connected">%s</h4> 
<form action="/" method="POST">
     <span id="dot"></span> <!-- Blink red  -->
     <span id="connectionStatus"></span>
     <input id="return" class="buttonRed" style="display:none;" type="submit" name="Return" value="Return to Connection Page">
 </form>
<script>
  var connected = document.getElementById('connected').innerHTML;
    if (connected == 'True') {
    document.getElementById("dot").className = "dotGreen";
    document.getElementById("connectionStatus").className = "green";
    document.getElementById("connectionStatus").innerHTML = 'Device Connected';
    document.getElementById("return").style.display = "none";
  } else {
    document.getElementById("dot").className = "dotRed";
    document.getElementById("connectionStatus").className = "red";
    document.getElementById("connectionStatus").innerHTML = 'No Device Connected';
    document.getElementById("return").style.display = "initial";
  }
</script>
<form id = "pageForm" action="/Page" method="POST" onchange="submit('pageForm')">
  <span>Select a page: </span>
  <select id="pageSelect" name = "page">
    <option value="simplePage">Welcome Page</option>
    <option value="page2">EV3 Example Code</option>
  </select>
  <input id="submitpage" type="submit" hidden="hidden">
 </form>
<script> // Changes the selected item in dropdown menu based on current page being served
// Same as fcn setValue() but runs every reload
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
</script>
<script src="BaseScripts.js"></script>
<script>
  function PressEnter(e,FormID) { // Submit form if Enter Key is pressed
    if ( (window.event ? event.keyCode : e.which) == 13) {
      document.getElementById(FormID).submit();
    }
  }
</script>