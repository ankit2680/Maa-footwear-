/*! MAA Footwear — Admin: Customer Enquiries */
document.addEventListener("DOMContentLoaded", function () {
  const tbody = document.getElementById("enquiriesBody");
  const countEl = document.getElementById("enqCount");

  function render() {
    const list = MAA.getEnquiries();
    countEl.textContent = `${list.length} enquir${list.length === 1 ? "y" : "ies"}`;
    tbody.innerHTML = list.length
      ? list
          .map(
            (e) => `<tr data-id="${e.id}">
        <td>${new Date(e.date).toLocaleString("en-IN")}</td>
        <td><b>${e.name}</b></td>
        <td><a href="tel:${e.phone}">${e.phone}</a></td>
        <td>${e.productName || "General"}</td>
        <td style="max-width:260px;">${e.message}</td>
        <td><span class="status-pill ${e.status === "new" ? "new" : "read"}">${e.status}</span></td>
        <td class="table-actions">
          <button class="btn btn-ghost btn-sm mark-btn">${e.status === "new" ? "Mark Read" : "Mark New"}</button>
          <button class="btn btn-danger btn-sm delete-btn">Delete</button>
        </td>
      </tr>`
          )
          .join("")
      : `<tr><td colspan="7" style="text-align:center;padding:30px;color:var(--muted);">No customer enquiries yet.</td></tr>`;
  }

  tbody.addEventListener("click", function (e) {
    const row = e.target.closest("tr[data-id]");
    if (!row) return;
    const id = row.dataset.id;
    if (e.target.classList.contains("delete-btn")) {
      if (confirm("Delete this enquiry?")) {
        MAA.deleteEnquiry(id);
        render();
      }
    }
    if (e.target.classList.contains("mark-btn")) {
      const current = MAA.getEnquiries().find((x) => String(x.id) === String(id));
      MAA.updateEnquiry(id, { status: current.status === "new" ? "read" : "new" });
      render();
    }
  });

  render();
});
