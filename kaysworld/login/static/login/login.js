/* Javascript Code for Login Authentication
Author: Kayla D. Coleman
Author URI: github.com/kdcoleman
*/

// LOGIN
let loginLink = document.getElementById('loginLink');
let loginButton = document.getElementById('loginButton');
let loginAlert = document.getElementById('loginAlert');
let closeLogin = document.getElementById('closeLogin');
let loginEmailMsg = document.getElementById('loginEmailErrMsg');
let loginPasswdMsg = document.getElementById('loginPasswdErrMsg');
let loginForm = document.forms['loginForm'];
let emailPattern = "[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+([\.-]?[A-Za-z0-9!#$%&'*+/=?^_`{|}~]+)*@[A-Za-z0-9]+([\-]?[A-Z-a-z0-9]+)*(\.[A-Za-z]{2,3})+";

// Mock data for an authenticated user
let returningUser = {firstName: "Lola", lastName: "Bunny", email: "lola@lolainthecity.com", password: "H@ppyG!rl"};

// Set email pattern
loginForm.elements.emailAddress.pattern = emailPattern;

// Show login alert onclick of login link
loginLink.addEventListener('click', function(){
  signupAlert.classList.remove('active');
  resetSignupForm();
  loginAlert.classList.toggle('active');
})

// Close login alert onclick of close button
closeLogin.addEventListener('click', function(){
  loginAlert.classList.toggle('active');
  resetLoginForm();
})


// Update validation message method
function updateMessage(element, value) {
  element.textContent = value;
}

// Reset login form
function resetLoginForm() {
  loginForm.reset();
  updateMessage(loginEmailMsg, "");
  updateMessage(loginPasswdMsg, "");
}

// Email validation method
function validateEmail(inputElement, messageElement, formElement) {
  let validityState = inputElement.validity;

  if (validityState.valueMissing) {
    inputElement.setCustomValidity('Required');
    updateMessage(messageElement, inputElement.validationMessage);
    return false;
  }
  else if (validityState.typeMismatch) {
    inputElement.setCustomValidity('Email must be in the format: you@example.com');
    updateMessage(messageElement, inputElement.validationMessage);
    return false;
  }
  else if (validityState.patternMismatch) {
    inputElement.setCustomValidity('Email address is invalid');
    updateMessage(messageElement, inputElement.validationMessage);
    return false;
  } else {
    return true;
  }

}


// Password validation method
function validatePassword(inputElement, messageElement, formElement) {
  let validityState = inputElement.validity;

  if (validityState.valueMissing) {
    inputElement.setCustomValidity('Required');
    updateMessage(messageElement, inputElement.validationMessage);
    return false;
  }
  else if (validityState.tooShort) {
    inputElement.setCustomValidity('Password must be at least 8 characters');
    updateMessage(messageElement, inputElement.validationMessage);
    formElement.elements.passwd.value = "";
    return false;
  } else {
    return true;
  }
}

//URL to pass the login form data
fileURL = "kaysWorld.html";
loginForm.method = "get";
loginForm.action = fileURL;


// Login form validation method
function validateLoginForm() {
  emailInput =  document.getElementById('emailAddress');
  passwdInput =  document.getElementById('passwd');

  updateMessage(loginEmailMsg, "");
  updateMessage(loginPasswdMsg, "");

  emailValidity = validateEmail(emailInput, loginEmailMsg, loginForm);
  passwordValidity = validatePassword(passwdInput, loginPasswdMsg, loginForm);

  // Login authentication
  if (emailValidity && passwordValidity) {
    if (emailInput == returningUser.email && passwdInput == returningUser.password){
      return true;
    } else if (emailInput.value != returningUser.email) {
      updateMessage(loginEmailMsg, "Account not found");
      return false;
    } else if (passwdInput.value != returningUser.password) {
      updateMessage(loginPasswdMsg, "Incorrect password");
      return false;
    }
  } else {
    return false;
  }
}


// Validate credentials onsubmit of login button on login alert
document.getElementById('loginForm').onsubmit = function() {
  return validateLoginForm();
};

// Validate credentials when press enter in input fields on login alert
document.getElementById('emailAddress').addEventListener('keypress', function (event) {
  if (event.keyCode == 13) {
    return validateLoginForm();
  }
});
document.getElementById('passwd').addEventListener('keypress', function (event) {
  if (event.keyCode == 13) {
    return validateLoginForm();
  }
});


// SIGN UP
let signupLink = document.getElementById('signupLink');
let signupButton = document.getElementById('signupButton');
let signupAlert = document.getElementById('signupAlert');
let closeSignup = document.getElementById('closeSignup');
let firstNameMsg = document.getElementById('signupFirstNameErrMsg');
let lastNameMsg = document.getElementById('signupLastNameErrMsg');
let signupEmailMsg = document.getElementById('signupEmailErrMsg');
let signupPasswdMsg = document.getElementById('signupPasswdErrMsg');
let confirmPasswdMsg = document.getElementById('signupConfirmPasswdErrMsg');
let signupForm = document.forms['signupForm'];
let namePattern = "[A-Za-z-\']+";

// Set first and last name pattern
signupForm.elements.firstName.pattern = namePattern;
signupForm.elements.lastName.pattern = namePattern;

// Show signup alert onclick of signup link
signupLink.addEventListener('click', function(){
  loginAlert.classList.remove('active');
  resetLoginForm();
  signupAlert.classList.toggle('active');
})

// Close signup alert onclick of close button
closeSignup.addEventListener('click', function(){
  signupAlert.classList.toggle('active');
  resetSignupForm();
})

// Reset signup form
function resetSignupForm() {
  signupForm.reset();
  updateMessage(firstNameMsg, "");
  updateMessage(lastNameMsg, "");
  updateMessage(signupEmailMsg, "");
  updateMessage(signupPasswdMsg, "");
  updateMessage(confirmPasswdMsg, "");
}


// First name validation method
function validateFirstName(inputElement, messageElement, formElement) {
  let validityState = inputElement.validity;

  if (validityState.valueMissing) {
    inputElement.setCustomValidity('Required');
    updateMessage(messageElement, inputElement.validationMessage);
    return false;
  }
  else if (validityState.patternMismatch) {
    inputElement.setCustomValidity('First name must not contain (!@#$%^&*?.,_)');
    updateMessage(messageElement, inputElement.validationMessage);
    formElement.elements.firstName.value = "";
    return false;
  } else {
    return true;
  }
}


// Last name validation method
function validateLastName(inputElement, messageElement, formElement) {
  let validityState = inputElement.validity;

  if (validityState.valueMissing) {
    inputElement.setCustomValidity('Required');
    updateMessage(messageElement, inputElement.validationMessage);
    return false;
  }
  else if (validityState.patternMismatch) {
    inputElement.setCustomValidity('Last name must only contain letters');
    updateMessage(messageElement, inputElement.validationMessage);
    formElement.elements.lastName.value = "";
    return false;
  } else {
    return true;
  }
}


// Confirm password method
function confirmPassword(inputElement, inputElementMatch, messageElement, formElement) {
  let validityState = inputElement.validity;

  if (validityState.valueMissing) {
    inputElement.setCustomValidity('Required');
    updateMessage(messageElement, inputElement.validationMessage);
    return false;
  }
  else if (inputElement.value != inputElementMatch.value) {
    inputElement.setCustomValidity('Does not match password');
    updateMessage(messageElement, inputElement.validationMessage);
    formElement.elements.lastName.value = "";
    return false;
  } else {
    return true;
  }
}

//URL to pass the signup form data
fileURL = "kaysWorld.html";
signupForm.method = "post";
signupForm.action = fileURL;


// Signup form validation method
function validateSignupForm() {
  firstNameInput =  document.getElementById('firstName');
  lastNameInput =  document.getElementById('lastName');
  signupEmailInput = document.getElementById('signupEmail');
  signupPasswdInput = document.getElementById('signupPasswd');
  confirmPasswdInput = document.getElementById('confirmPasswd');

  updateMessage(firstNameMsg, "");
  updateMessage(lastNameMsg, "");
  updateMessage(signupEmailMsg, "");
  updateMessage(signupPasswdMsg, "");
  updateMessage(confirmPasswdMsg, "");

  firstNameValidity = validateFirstName(firstNameInput, firstNameMsg, signupForm);
  lastNameValidity = validateLastName(lastNameInput, lastNameMsg, signupForm);
  emailValidity = validateEmail(signupEmailInput, signupEmailMsg, signupForm);
  passwordValidity = validatePassword(signupPasswdInput, signupPasswdMsg, signupForm);
  confirmValidity = confirmPassword(confirmPasswdInput, signupPasswdInput, confirmPasswdMsg, signupForm);

  if (firstNameValidity && lastNameValidity && emailValidity && passwordValidity && confirmValidity) {
    if (signupEmailInput.value != returningUser.email) {
      return true;
    } else {
      updateMessage(signupEmailMsg, "Sorry, this email is already in use");
      return false;
    }
  } else {
    return false;
  }
}


// Validate credentials onsubmit of signup button on signup alert
document.getElementById('signupForm').onsubmit = function() {
  return validateSignupForm();
};

// Validate credentials when press enter in input fields on signup alert
document.getElementById('firstName').addEventListener('keypress', function (event) {
  if (event.keyCode == 13) {
    return validateSignupForm();
  }
});
document.getElementById('lastName').addEventListener('keypress', function (event) {
  if (event.keyCode == 13) {
    return validateSignupForm();
  }
});
document.getElementById('signupEmail').addEventListener('keypress', function (event) {
  if (event.keyCode == 13) {
    return validateSignupForm();
  }
});
document.getElementById('signupPasswd').addEventListener('keypress', function (event) {
  if (event.keyCode == 13) {
    return validateSignupForm();
  }
});
