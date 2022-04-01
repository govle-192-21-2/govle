const LinkedAccount = (username, img_url, type, remove_param) => `
    <div class="col-md-2 mr-4">
        <img src="${img_url}" alt="${username}" width="125">
    </div>
    <div class="col-md-6">
        <h4>${username}</h4>
        <p class="text-dark">${type}</p>
        <a class="p" href="/settings/unlink?${remove_param}">Disconnect account...</a>
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
                account_list.append(LinkedAccount(
                    all_accounts['moodle']['username'],
                    'https://uvle.upd.edu.ph/pluginfile.php/1/core_admin/logocompact/300x300/1645818713/logo-uvle-min-1024x1024.png',
                    'Moodle',
                    'type=moodle'
                ));
            }

            // List all Google accounts
            for (const google_account of all_accounts['google']) {
                account_list.append(LinkedAccount(
                    google_account['email'],
                    google_account['gravatar'],
                    'Google Classroom',
                    'type=google&id=' + google_account['id']
                ));
            }
        });
});