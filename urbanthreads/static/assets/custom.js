$("#add_to_cart").click(function(event){ 
    console.log("Card link clicked"); 
    event.preventDefault();  
    var url="{% url 'accounts:add_to_cart_ajax' 0 %}".replace('0', product.uid); 
    $.ajax({ 
        type: "POST", 
        url: url, 
        data:{ csrfmiddlewaretoken: "{{csrf_token}}"}, 
        success: function (data){ 
            if (data.course_added){ 
            showCustomAlert("added!")} 
            else{ 
                showCustomAlert("Course removed!")}
            }, 
        error: function (xhr, textStatus, errorThrown){ 
            console.log(xhr); 
            console.log(textStatus); 
            console.log(errorThrown); 
            alert("Module Completed - Error")
            },
    })}); 
    function showCustomAlert(message){ 
        var customAlert=document.getElementById("customAlert"); 
        var alertMessage=customAlert.querySelector(".alert-message"); 
        alertMessage.textContent=message; 
        customAlert.style.display="block"} 
    function closeCustomAlert(){ 
        document.getElementById("customAlert").style.display="none"
    } 
    
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        window.location.reload();
        }
    });