let container = document.getElementById('container')

toggle = () => {
	container.classList.toggle('sign-in')
	container.classList.toggle('sign-up')
}

setTimeout(() => {
	container.classList.add('sign-in')
}, 200)



////.................password visibility............////

function togglePasswordVisibility() {
    var passwordField = document.getElementById("password");
    var showPasswordCheckbox = document.getElementById("showPasswordCheckbox");
  
    if (showPasswordCheckbox.checked) {
      passwordField.type = "text";
    } else {
      passwordField.type = "password";
    }
  }
  


  // Wait for the page to load
  document.addEventListener("DOMContentLoaded", function() {
    // Get the success message element
    var successMessage = document.getElementById("success-message");
    
    // Check if the success message element exists
    if (successMessage) {
        // Set a timeout to redirect after 3 seconds (adjust the delay as needed)
        setTimeout(function() {
            window.location.href = "/signin";
        }, 3000); // 3 seconds
    }
});



// Get the error message element
const errorMessage = document.getElementById('error-message');

// Function to hide the error message after a delay
function hideErrorMessage() {
    errorMessage.style.display = 'none';
}

// Delay in milliseconds (e.g., 3000 for 3 seconds)
const delay = 3000;

// Hide the error message after the delay
setTimeout(hideErrorMessage, delay);

