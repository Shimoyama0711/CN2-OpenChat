$(function() {
    const emailInput = $("#email-input");
    const usernameInput = $("#username-input");
    const passwordInput = $("#password-input");

    emailInput.on("input", check);
    usernameInput.on("input", check);
    passwordInput.on("input", check);
});

function check() {
    const emailInput = $("#email-input");
    const usernameInput = $("#username-input");
    const passwordInput = $("#password-input");

    const signupButton = $("#signup-button");

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const b1 = emailRegex.test(emailInput.val());
    const b2 = usernameInput.val().length > 0;
    const b3 = passwordInput.val().length >= 6;

    if (b1 && b2 && b3) {
        signupButton.removeClass("disabled");
    } else {
        signupButton.addClass("disabled");
    }
}