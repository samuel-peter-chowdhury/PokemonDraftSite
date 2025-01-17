$(document).ready(function () {
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
        if (e.detail.target.id == "pokemon-modal") {
            $('#page-spinner').hide();
            $('#pokemon-modal-content').modal('show');
        }
    });
});