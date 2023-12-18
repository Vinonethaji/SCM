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

