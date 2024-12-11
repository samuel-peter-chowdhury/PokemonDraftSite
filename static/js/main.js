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


    if (localStorage.getItem('team-matchup-speed-tiers-expansion') === null) {
        localStorage.setItem('team-matchup-speed-tiers-expansion', 'open');
    }
    let speedTierState = localStorage.getItem('team-matchup-speed-tiers-expansion');
    if (speedTierState == 'closed') {
        $('#speedTierCollapse').removeClass('show');
    }
    $('#speedTierCollapseButton').click(function (e) {
        e.preventDefault();
        let speedTierState = localStorage.getItem('team-matchup-speed-tiers-expansion');
        if (speedTierState == 'open') {
            localStorage.setItem('team-matchup-speed-tiers-expansion', 'closed');
        } else {
            localStorage.setItem('team-matchup-speed-tiers-expansion', 'open');
        }
    });


    if (localStorage.getItem('team-matchup-user-table-expansion') === null) {
        localStorage.setItem('team-matchup-user-table-expansion', 'open');
    }
    let userTableState = localStorage.getItem('team-matchup-user-table-expansion');
    if (userTableState == 'open') {
        $('#userTeamTableCollapse').addClass('show');
    }
    $('#userTeamTableCollapseButton').click(function (e) {
        e.preventDefault();
        let userTableState = localStorage.getItem('team-matchup-user-table-expansion');
        if (userTableState == 'open') {
            localStorage.setItem('team-matchup-user-table-expansion', 'closed');
        } else {
            localStorage.setItem('team-matchup-user-table-expansion', 'open');
        }
    });


    if (localStorage.getItem('team-matchup-opponent-table-expansion') === null) {
        localStorage.setItem('team-matchup-opponent-table-expansion', 'open');
    }
    let opponentTableState = localStorage.getItem('team-matchup-opponent-table-expansion');
    if (opponentTableState == 'open') {
        $('#opponentTeamTableCollapse').addClass('show');
    }
    $('#opponentTeamTableCollapseButton').click(function (e) {
        e.preventDefault();
        let opponentTableState = localStorage.getItem('team-matchup-opponent-table-expansion');
        if (opponentTableState == 'open') {
            localStorage.setItem('team-matchup-opponent-table-expansion', 'closed');
        } else {
            localStorage.setItem('team-matchup-opponent-table-expansion', 'open');
        }
    });
});