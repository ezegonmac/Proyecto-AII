// select the navbar element
const navbar = document.querySelector('nav');

// get the height of the navbar
const navbarHeight = navbar.offsetHeight * 2;

// set the navbar's initial background color to transparent
navbar.style.backgroundColor = 'rgba(31, 31, 31, 0)';

// add an event listener to listen for scroll events
window.addEventListener('scroll', () => {
  // get the current scroll position
  const scrollPosition = window.scrollY;

  // calculate the opacity as a value between 0 and 1
  const navbarOpacity = scrollPosition / navbarHeight;

  // set the navbar's background color using rgba, with the opacity value
  navbar.style.backgroundColor = `rgba(31, 31, 31, ${navbarOpacity})`;
});

// add an event listener to listen for load events
window.addEventListener('load', () => {
  // set the navbar's initial background color to transparent
  navbar.style.backgroundColor = 'rgba(31, 31, 31, 0)';
});