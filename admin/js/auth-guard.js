/*! MAA Footwear — Admin auth guard. Include on every protected admin page. */
(function () {
  if (!window.MAA || !MAA.isLoggedIn()) {
    window.location.href = "login.html";
  }
})();

document.addEventListener("DOMContentLoaded", function () {
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", function (e) {
      e.preventDefault();
      MAA.logout();
      window.location.href = "login.html";
    });
  }
});
