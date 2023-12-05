let container = document.getElementById('container')

toggle = () => {
	container.classList.toggle('sign-in')
	container.classList.toggle('sign-up')
}

setTimeout(() => {
	container.classList.add('sign-in')
}, 200)



document.getElementById('signinform').addEventListener('submit', function(event) {
	event.preventDefault();
	const username = document.getElementById('username').value;
	const password = document.getElementById('password').value;
  
	// Check if username and password are valid
	if (username === 'admin' && password === 'password') {
	  // Successful login
	  alert('Login Successful');
	} else {
	  // Invalid login
	  alert('Invalid username or password');
	}
  });
  
  document.getElementById('signupform').addEventListener('submit', function(event) {
	event.preventDefault();
	const username = document.getElementById('username').value;
	const email = document.getElementById('email').value;
	const password = document.getElementById('password').value;
	const confirmPassword = document.getElementById('confirmpassword').value;
  
	// Check if all fields are filled
	if (username && email && password && confirmPassword) {
	  // Check if passwords match
	  if (password === confirmPassword) {
		// Successful registration
		alert('Registration Successful');
		// Reset the form
		document.getElementById('signupform').reset();
	  } else {
		// Passwords don't match
		alert('Passwords do not match');
	  }
	} else {
	  // Missing fields
	  alert('Please fill in all fields');
	}
  });

  document.getElementById("myForm").addEventListener("submit", function(event) {
	event.preventDefault(); // Prevent form submission
  
	// Get the email input value
	var emailInput = document.getElementById("email");
	var email = emailInput.value;
  
	// Use a regular expression to validate the email syntax
	var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	if (!emailRegex.test(email)) {
	  // Show an alert message if the email syntax is incorrect
	  alert("Please enter a valid Gmail address");
	  return;
	}
  
	// Submit the form if the email syntax is correct
	this.submit();
  });
  