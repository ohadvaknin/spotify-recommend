document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("artistForm");
    const loading = document.getElementById("loading");

    form.addEventListener("submit", function() {
        loading.style.display = "block";
    });
});
