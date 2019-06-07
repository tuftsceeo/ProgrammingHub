function PressEnter(e,FormID) {
    // If Enter is Pressed
    if ( (window.event ? event.keyCode : e.which) == 13) {
    	// Submit the Form
        document.getElementById(FormID).submit();
    }
}