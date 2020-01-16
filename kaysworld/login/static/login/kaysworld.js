/* Javascript Code for Login Authentication
Author: Kayla D. Coleman
Author URI: github.com/kdcoleman
*/

// Welcome
let welcomeAlert = document.getElementById('welcomeAlert');
let welcomeMsg = document.getElementById('welcomeMsg');
let closeWelcome = document.getElementById('closeWelcome');
let firstName = getUrlVariable('firstName') ? getUrlVariable('firstName') : null;
let lastName = getUrlVariable('lastName') ? getUrlVariable('lastName') : null;
let email = getUrlVariable('emailAddress') ? getUrlVariable('emailAddress'): getUrlVariable('signupEmail');
let password = getUrlVariable('passwd') ? getUrlVariable('passwd'):getUrlVariable('signupPasswd');
let newUser = {firstName: firstName, lastName: lastName, email: email, password: password};

// Mock data for an authenticated user
let returningUser = {firstName: "Lola", lastName: "Bunny", email: "lola@lolainthecity.com", password: "H@ppyG!rl"};

// Close welcome alert onclick of close button
closeWelcome.addEventListener('click', function(){
  welcomeAlert.classList.remove('active');
})

window.addEventListener('load', function() {
  showWelcomeMessage();
});

// Get url variables
function getUrlVariable(variable) {
  let query = window.location.search.substring(1);
  let vars = query.split("&");
  for (var i = 0; i < vars.length; i++) {
   let pair = vars[i].split("=");

   if (pair[0] == variable){
     if (pair[1].includes("%40")) {
       newPair = pair[1].replace("%40","@");
       return newPair
     } else {
       return pair[1];
     }
   }
  }
  return false;
}

// Update welcome message method
function updateMessage(element, value) {
  element.textContent = value;
}

function showWelcomeMessage() {
  if (newUser.firstName) {
    newUserMsg = "Welcome " + newUser.firstName +
    "! We're so glad you decided to explore the land of Kay. We sent a confirmation email to " + newUser.email +
    ". <br><br> Please confirm your account."
    welcomeMsg.innerHTML = newUserMsg;
  } else if (returningUser.firstName){
    returningUserMsg = "Welcome back " + returningUser.firstName +
    "! Check out what's new since your last time here. Happy exploring!"
    updateMessage(welcomeMsg,returningUserMsg);
  }
}
