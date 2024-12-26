$(document).ready(function () {
    $('#menu-toggle').click(function (e) {
        e.preventDefault();
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


    if (localStorage.getItem('team-matchup-user-type-effective-expansion') === null) {
        localStorage.setItem('team-matchup-user-type-effective-expansion', 'open');
    }
    let userTypeEffectiveState = localStorage.getItem('team-matchup-user-type-effective-expansion');
    if (userTypeEffectiveState == 'open') {
        $('#userTypeEffectiveCollapse').addClass('show');
    }
    $('#userTypeEffectiveCollapseButton').click(function (e) {
        e.preventDefault();
        let userTypeEffectiveState = localStorage.getItem('team-matchup-user-type-effective-expansion');
        if (userTypeEffectiveState == 'open') {
            localStorage.setItem('team-matchup-user-type-effective-expansion', 'closed');
        } else {
            localStorage.setItem('team-matchup-user-type-effective-expansion', 'open');
        }
    });


    if (localStorage.getItem('team-matchup-opponent-type-effective-expansion') === null) {
        localStorage.setItem('team-matchup-opponent-type-effective-expansion', 'open');
    }
    let opponentTypeEffectiveState = localStorage.getItem('team-matchup-opponent-type-effective-expansion');
    if (opponentTypeEffectiveState == 'open') {
        $('#opponentTypeEffectiveCollapse').addClass('show');
    }
    $('#opponentTypeEffectiveCollapseButton').click(function (e) {
        e.preventDefault();
        let opponentTypeEffectiveState = localStorage.getItem('team-matchup-opponent-type-effective-expansion');
        if (opponentTypeEffectiveState == 'open') {
            localStorage.setItem('team-matchup-opponent-type-effective-expansion', 'closed');
        } else {
            localStorage.setItem('team-matchup-opponent-type-effective-expansion', 'open');
        }
    });
    
    
    htmx.on("htmx:afterSwap", (e) => {
        if (e.detail.target.id == "pokemon-modal") {
            $('#pokemon-modal-content').modal('show');
        }
    });
});