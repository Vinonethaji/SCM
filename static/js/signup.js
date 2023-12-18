

    
let container = document.getElementById('container')

toggle = () => {
	container.classList.toggle('sign-in')
	container.classList.toggle('sign-up')
}

setTimeout(() => {
	container.classList.add('sign-up')
}, 200)

function togglePasswordVisibility() {
        const passwordInput = document.getElementById('password');
        const togglePassword = document.getElementById('togglePassword');

        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            togglePassword.innerHTML = '&#128064;'; // Closed eye icon
        } else {
            passwordInput.type = 'password';
            togglePassword.innerHTML = '&#128065;'; // Open eye icon
        }
    } 

    
  

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
