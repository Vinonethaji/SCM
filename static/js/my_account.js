const sidebar = document.querySelector('.sidebar');
const navItems = document.querySelectorAll('nav .nav-item');
const toggle = document.querySelector('.sidebar .toggle');

toggle.addEventListener('click', () => {
  sidebar.classList.toggle('open');
});

navItems.forEach(navItem => {
  navItem.addEventListener('click', () => {
    navItems.forEach(item => {
      item.classList.remove('active');
    });
    navItem.classList.add('active');

    const pageURL = navItem.getAttribute('data-page');
    if (pageURL) {
      // Update the URL to navigate to the respective page
      window.location.href = pageURL;
    }
  });
});

// Add the following code to set the active button based on the current page
const currentPage = window.location.pathname.split('/').pop();
navItems.forEach(navItem => {
  const pageURL = navItem.getAttribute('data-page');
  if (pageURL === currentPage) {
    navItem.classList.add('active');
  } else {
    navItem.classList.remove('active');
  }
});


       

        //logout....

        function clearAccessToken() {
            console.log('Clearing access token');

// Make a request to your logout endpoint
fetch('/logout')
    .then(response => {
        if (response.ok) {
            // Redirect to the home page after successful logout
            window.location.href = '/';
        } else {
            console.error('Failed to logout');
        }
    })
    .catch(error => console.error('Error during logout:', error));
}

///user name/////
// Get the first letter of the username
document.addEventListener('DOMContentLoaded', function() {
  // Get the first letter of the username
  const usernameElement = document.querySelector('.username');
  if (usernameElement) {
    const username = usernameElement.textContent.trim();
    const firstLetter = username.charAt(10).toUpperCase(); // Adjust the index based on your HTML structure

    // Set the first letter as the content of the span element
    const profilePhotoSpan = document.querySelector("#profilePhoto .p-p");
    if (profilePhotoSpan) {
      profilePhotoSpan.textContent = firstLetter;
    }
  }
});