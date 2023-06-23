const modal = document.getElementById('modal');
const openSettings = document.getElementById('settings-btn');

openSettings.addEventListener('click', () => {
    modal.showModal();
})

document.querySelectorAll(".nav-link").forEach((link) => {
    if (link.href === window.location.href) {
        link.classList.add("active-nav");
        link.setAttribute("aria-current", "page");
    }
});