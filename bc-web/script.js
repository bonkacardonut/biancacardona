// Highlight the current page in the nav
const here = (location.pathname.split("/").pop() || "index.html").toLowerCase();
document.querySelectorAll(".nav-links a").forEach((a) => {
  const target = a.getAttribute("href").toLowerCase();
  if (target === here || (here === "" && target === "index.html")) {
    a.setAttribute("aria-current", "page");
  }
});

// If the receipt image hasn't been added yet, fall back to the colored block
document.querySelectorAll(".card-img img").forEach((img) => {
  img.addEventListener("error", () => img.remove());
});
