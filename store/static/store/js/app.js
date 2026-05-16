const drawer = document.querySelector(".cart-drawer");
const overlay = document.querySelector(".cart-overlay");
const openers = document.querySelectorAll("[data-cart-open]");
const closers = document.querySelectorAll("[data-cart-close]");
const sidebar = document.querySelector(".sidebar-shell");
const mobileOverlay = document.querySelector(".mobile-nav-overlay");
const navOpen = document.querySelector("[data-nav-open]");
const navClose = document.querySelectorAll("[data-nav-close]");

function setCart(open) {
  if (!drawer || !overlay) return;
  drawer.classList.toggle("open", open);
  overlay.classList.toggle("open", open);
  drawer.setAttribute("aria-hidden", String(!open));
  openers.forEach((button) => button.setAttribute("aria-expanded", String(open)));
}

function setNav(open) {
  if (!sidebar || !mobileOverlay) return;
  sidebar.classList.toggle("open", open);
  mobileOverlay.classList.toggle("open", open);
  navOpen?.setAttribute("aria-expanded", String(open));
}

openers.forEach((button) => button.addEventListener("click", () => setCart(true)));
closers.forEach((button) => button.addEventListener("click", () => setCart(false)));
navOpen?.addEventListener("click", () => setNav(true));
navClose.forEach((button) => button.addEventListener("click", () => setNav(false)));

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    setCart(false);
    setNav(false);
    closePreview();
  }
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add("is-visible");
    });
  },
  { threshold: 0.14 }
);
document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));

document.querySelectorAll(".tilt-card").forEach((card) => {
  card.addEventListener("pointermove", (event) => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const rect = card.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - 0.5;
    const y = (event.clientY - rect.top) / rect.height - 0.5;
    card.style.transform = `perspective(900px) rotateX(${y * -3}deg) rotateY(${x * 4}deg) translateY(-4px)`;
  });
  card.addEventListener("pointerleave", () => {
    card.style.transform = "";
  });
});

const previewModal = document.querySelector(".quick-preview-modal");
const previewTitle = document.querySelector("[data-preview-title-target]");
const previewAuthor = document.querySelector("[data-preview-author-target]");
const previewDesc = document.querySelector("[data-preview-desc-target]");
const previewCover = document.querySelector("[data-preview-cover-target]");

function closePreview() {
  previewModal?.classList.remove("open");
  previewModal?.setAttribute("aria-hidden", "true");
}

document.querySelectorAll("[data-preview-title]").forEach((button) => {
  button.addEventListener("click", () => {
    if (!previewModal) return;
    previewTitle.textContent = button.dataset.previewTitle || "";
    previewAuthor.textContent = button.dataset.previewAuthor || "";
    previewDesc.textContent = button.dataset.previewDesc || "";
    previewCover.src = button.dataset.previewCover || "";
    previewCover.alt = `${button.dataset.previewTitle || "Book"} cover`;
    previewModal.classList.add("open");
    previewModal.setAttribute("aria-hidden", "false");
  });
});

document.querySelector("[data-preview-close]")?.addEventListener("click", closePreview);
previewModal?.addEventListener("click", (event) => {
  if (event.target === previewModal) closePreview();
});

document.querySelectorAll("[data-tabs]").forEach((tabs) => {
  const buttons = tabs.querySelectorAll("[data-tab]");
  const panels = tabs.querySelectorAll("[data-panel]");
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((item) => item.classList.toggle("active", item === button));
      panels.forEach((panel) => panel.classList.toggle("active", panel.dataset.panel === button.dataset.tab));
    });
  });
});

document.querySelector("[data-filter-jump]")?.addEventListener("click", () => {
  document.querySelector("#genres")?.scrollIntoView({ behavior: "smooth", block: "start" });
});
