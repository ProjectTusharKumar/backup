let ready = false;
let polling = false;

function showPopup(msg) {
    $('#popup').text(msg).fadeIn(200).delay(1200).fadeOut(400);
}

$(function() {
    // Check server status button
    $('#checkServerBtn').click(function() {
        $.get('https://laughing-space-goldfish-q7vvqxgvw4vrcxgr6-8000.app.github.dev/status', function(data) {
            if (data.running) {
                showPopup('Server is running!');
                $('#checkServerBtn').css('background', '#4caf50').text('Server is Running');
            } else {
                showPopup('Server is NOT running!');
                $('#checkServerBtn').css('background', '#f44336').text('Server is NOT Running');
            }
        }).fail(() => {
            showPopup('Server not reachable.');
            $('#checkServerBtn').css('background', '#f44336').text('Server is NOT Running');
        });
    });

    // Create backup button
    $('#backupBtn').click(function() {
        $.ajax({
            url: 'https://laughing-space-goldfish-q7vvqxgvw4vrcxgr6-8000.app.github.dev/run_bat',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ name: 'create_backup' }),
            success: function(res) {
                showPopup('Backup created!');
            },
            error: function() {
                showPopup('Failed to create backup!');
            }
        });
    });
});
