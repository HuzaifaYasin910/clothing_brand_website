function showCustomAlert(message){
    var customAlert=document.getElementById("customAlert"); 
    var alertMessage=customAlert.querySelector(".alert-message"); 
    alertMessage.textContent=message; 
    customAlert.style.display="flex"} 
    function closeCustomAlert(){
    document.getElementById("customAlert").style.display="none"
    }