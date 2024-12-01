$(document).ready(function () {
    if (localStorage.getItem('menu-toggle-state') === null) {
        localStorage.setItem('menu-toggle-state', 'closed');
    }
    let menuToggleState = localStorage.getItem('menu-toggle-state');
    if (menuToggleState === 'open') {
        $('#sidebar').removeClass('collapsed');
        $('#page-content-wrapper').removeClass('collapsed');
    } else {
        $('#sidebar').addClass('collapsed');
        $('#page-content-wrapper').addClass('collapsed');
    }

    $('#menu-toggle').click(function (e) {
        e.preventDefault();
        let menuToggleState = localStorage.getItem('menu-toggle-state');
        if (menuToggleState === 'open') {
            localStorage.setItem('menu-toggle-state', 'closed');
        } else {
            localStorage.setItem('menu-toggle-state', 'open');
        }
        $('#sidebar').toggleClass('collapsed');
        $('#page-content-wrapper').toggleClass('collapsed');
    });
});