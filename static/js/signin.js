

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

let container = document.getElementById('container')

toggle = () => {
	container.classList.toggle('sign-in')
	container.classList.toggle('sign-up')
}

setTimeout(() => {
	container.classList.add('sign-in')
}, 200)

//captcha
let captchaText = document.getElementById('captcha');
// captchaText.width = 400; 
// captchaText.height = 200;

var ctx = captchaText.getContext("2d");
ctx.font = "40px Roboto";
ctx.fillStyle = "#08e5ff";

let userText = document.getElementById('textBox');
let submitButton = document.getElementById('submitButton');
let output = document.getElementById('output');
let refreshButton = document.getElementById('refreshButton');
// To generate the CAPTCHA text

var captchaStr = "";

let alphaNums = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
                 'H', 'I', 'J', 'K', 'L', 'M', 'N', 
                 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 
                 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 
                 'c', 'd', 'e', 'f', 'g', 'h', 'i', 
                 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
                 'q', 'r', 's', 't', 'u', 'v', 'w', 
                 'x', 'y', 'z', '0', '1', '2', '3', 
                 '4', '5', '6', '7', '8', '9'];

function generate_captcha() {
    let emptyArr = [];
                 
    for (let i = 1; i <= 7; i++) {
        emptyArr.push(alphaNums[Math.floor(Math.random() * alphaNums.length)]);
    }
                 
    captchaStr = emptyArr.join('');
                 
    ctx.clearRect(0, 0, captchaText.width, captchaText.height);
    ctx.fillText(captchaStr, captchaText.width/4, captchaText.height/2);
                 
    output.innerHTML = "";
}
                 
generate_captcha();

//
let signInButton = document.getElementById('sign-inbutton');

                 
function check_captcha() {
    if (userText.value === captchaStr) {
        output.className = "correctCaptcha";
        output.innerHTML = "Correct!";
        signInButton.disabled = false;
        
        // Add a class for flickering only when the button is enabled
        signInButton.classList.add("enable-flicker");
    } else {
        output.className = "incorrectCaptcha";
        output.innerHTML = "Incorrect, please try again!";
        signInButton.disabled = true;
        // Remove the class to stop flickering when the button is disabled
        signInButton.classList.remove("enable-flicker");
    }
}


userText.addEventListener('keyup', function(e) {
    if (e.key === 'Enter') {
       check_captcha();
    }
});

submitButton.addEventListener('click', check_captcha);
refreshButton.addEventListener('click', function (event) {
            generate_captcha();
            event.preventDefault(); // Prevent the default button click behavior
        });

        
// Function to show and hide messages with a delay
function showMessage(message, className, delay) {
    const messageContainer = document.getElementById('message-container');
    
    // Clear previous messages
    messageContainer.innerHTML = '';

    // Show the new message
    const newMessage = document.createElement('p');
    newMessage.className = className;
    newMessage.textContent = message;
    messageContainer.appendChild(newMessage);

    // Hide the message after the specified delay
    setTimeout(() => {
        messageContainer.style.display = 'none';
    }, delay);
}

 // Remove the error message after 5 seconds (5000 milliseconds)
 setTimeout(function() {
    var messageContainer = document.getElementById("message-container");
    if (messageContainer) {
        messageContainer.innerHTML = "";
    }
}, 5000);