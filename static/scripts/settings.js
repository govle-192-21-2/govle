const LinkedAccount = (username, img_url, type) => `
    <div class="row linked-account mb-4">
        <div class="col-4">
            <img src="${img_url}" alt="${username}" class="w-100">
        </div>
        <div class="col-8">
            <h4>${username}</h4>
            <p class="text-dark">${type}</p>
            <a class="p" href="#">Disconnect account...</a>
        </div>
    </div>
</div>
`;

$(document).ready(() => {
    // Get list of accounts from API
    fetch('/api/v1/accounts').then(response => response.json())
        .then(all_accounts => {
            const account_list = $('#linked-accounts');

            // Empty container
            account_list.empty();

            // Check if Moodle account is present
            if (all_accounts['moodle'] !== null) {
                const linked_moodle = $.parseHTML(LinkedAccount(
                    all_accounts['moodle']['username'],
                    'https://uvle.upd.edu.ph/pluginfile.php/1/core_admin/logocompact/300x300/1645818713/logo-uvle-min-1024x1024.png',
                    all_accounts['moodle']['server']
                ));
                $(linked_moodle).find('a').click(() => unlink_account('moodle', ''));
                account_list.append(linked_moodle);
            }

            // List all Google accounts
            for (const google_account of all_accounts['google']) {
                const linked_google = $.parseHTML(LinkedAccount(
                    google_account['email'],
                    google_account['gravatar'],
                    'Google Classroom'
                ));
                $(linked_google).find('a').click(() => unlink_account('google', google_account['id']));
                account_list.append(linked_google);
            }
        });
    
    // Listen to account deletion click event
    $('#confirm-delete').click(() => {
        fetch('/api/v1/settings/delete_account', { 'method': 'POST' })
            .then(response => response.json())
            .then(response => {
                if (response.success === true) {
                    window.location.href = '/';
                } else {
                    alert(response.error);
                }
            });
    });
});

const unlink_account = (type, id) => {
    fetch('/api/v1/settings/unlink', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            type: type,
            id: id
        })
    }).then(response => response.json())
        .then(response => {
            if (response['success'] === true) {
                window.location.reload();
            } else {
                alert('Failed to unlink account. Error: ' + response['error']);
            }
        });
}
