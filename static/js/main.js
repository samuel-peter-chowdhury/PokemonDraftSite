$(document).ready(function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    $('#menu-toggle').click(function (e) {
        e.preventDefault();
        $('#sidebar').toggleClass('collapsed');
        $('#page-content-wrapper').toggleClass('collapsed');
    });

    htmx.on("htmx:beforeRequest", (e) => {
        if (e.detail.target.id == "pokemon-modal") {
            $('#page-spinner').show();
        }
    });
    
    htmx.on("htmx:afterSwap", (e) => {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl)
        });
        if (e.detail.target.id == "pokemon-modal") {
            $('#page-spinner').hide();
            $('#pokemon-modal-content').modal('show');
        }
    });
});