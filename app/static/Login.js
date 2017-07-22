$(document).ready(function() {
		console.log($("#file-upload").value)
		
		//help use the validate function work with the other input buttons. 
		validate();
		$('#passcode, #email, #file-upload').change(validate);
		
		
	}

)

//This funtion validates the buttons where the buttons are disabled until there are text or file within them.	
function validate(){
    if ($('#passcode').val().length > 0 && $('#email').val().length > 0 || document.getElementById("file-upload").files.length >0) 
	{
        $("button[type=submit]").prop("disabled", false);
    }
	
    else 
	{
        $("button[type=submit]").prop("disabled", true);
    }
}

//function to send passcode and email to someplace P.s. I couldn't figure out how to send to server work with moon and other person on saturday to figure this out.
function sendPCEM()
{
    var inputPC = document.getElementById('passcode').value
	var inputEm = document.getElementById('email').value
}

//function to send file to someplace P.s. I couldn't figure out how to send to server work with moon and other person on saturday to figure this out.
function sendFile()
{
    var inputFile = document.getElementById('file-upload').value
}

