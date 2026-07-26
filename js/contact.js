/*! MAA Footwear — Contact page form handling */
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("contactForm");
  if (!form) return;
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    MAA.addEnquiry({
      name: data.name,
      phone: data.phone,
      email: data.email || "",
      message: data.message,
      productId: null,
      productName: "General Enquiry",
    });
    form.innerHTML = `<div class="empty-state">
      <h3>Message sent, ${data.name.split(" ")[0]}!</h3>
      <p>Thanks for reaching out — our team will get back to you shortly. For a faster response, message us directly on WhatsApp.</p>
      <a href="https://wa.me/919876543210" target="_blank" rel="noopener" class="btn btn-whatsapp">WhatsApp Us Now</a>
    </div>`;
  });
});
