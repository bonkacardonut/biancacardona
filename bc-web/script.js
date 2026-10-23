// If the receipt image hasn't been added yet, fall back to the colored block
document.querySelectorAll(".card-img img").forEach((img) => {
  img.addEventListener("error", () => img.remove());
});
