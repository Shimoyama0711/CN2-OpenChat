$(function() {
    const emailInput = $("#email-input");
    const passwordInput = $("#password-input");

    emailInput.on("input", check);
    passwordInput.on("input", check);
});

function check() {
    const emailInput = $("#email-input");
    const passwordInput = $("#password-input");

    const loginButton = $("#login-button");

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const b1 = emailRegex.test(emailInput.val());
    const b2 = passwordInput.val().length >= 6;

    if (b1 && b2) {
        loginButton.removeClass("disabled");
    } else {
        loginButton.addClass("disabled");
    }
}