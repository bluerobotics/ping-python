function replaceHeaderLinkContent() {
const headerLinks = document.querySelectorAll('.headerlink');
headerLinks.forEach(link => {
    link.textContent = '#';
});
}

document.addEventListener("DOMContentLoaded", () => {
replaceHeaderLinkContent();
});
