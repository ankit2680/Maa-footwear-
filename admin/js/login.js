/*! MAA Footwear — Admin login handling */
document.addEventListener("DOMContentLoaded", function () {
  if (MAA.isLoggedIn()) {
    window.location.href = "dashboard.html";
    return;
  }
  const form = document.getElementById("loginForm");
  const errorEl = document.getElementById("loginError");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const username = form.username.value.trim();
    const password = form.password.value;
    if (MAA.login(username, password)) {
      window.location.href = "dashboard.html";
    } else {
      errorEl.textContent = "Incorrect username or password. Please try again.";
      errorEl.style.display = "block";
    }
  });
});
