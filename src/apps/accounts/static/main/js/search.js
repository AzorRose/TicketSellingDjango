const form = document.querySelector('form');
const input = document.querySelector('input[name="q"]');
const button = document.querySelector('button[type="submit"]');

form.addEventListener('submit', e => {
  if(!input.value) {
    e.preventDefault();
    button.disabled = true; 
  } 
});
input.addEventListener('input', () => {
  button.disabled = !input.value;  
});
