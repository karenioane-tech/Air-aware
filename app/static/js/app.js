// Mobile nav toggle — collapses the chart-tab nav behind a menu button
// below the responsive breakpoint. No-op on desktop widths (button is hidden).
document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("site-nav");

    if (!toggle || !nav) return;

    toggle.addEventListener("click", function () {
        var isOpen = nav.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    // Close the menu after navigating (so it doesn't stay open on return).
    nav.addEventListener("click", function (e) {
        if (e.target.tagName === "A") {
            nav.classList.remove("is-open");
            toggle.setAttribute("aria-expanded", "false");
        }
    });
});
