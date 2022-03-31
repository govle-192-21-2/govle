const GoogleClass = (email, url, title, description) => `
    <div class="col-12 mb-4 col-lg-4 col-md-6 col-xs-12">
        <div class="card">
            <div class="card-body">
                <a class="govle-class" href="${url}" rel="noopener" target="_blank">
                    <h3 class="text-dark mb-3"><span>${title}</span><span>&#8599;</span></h3>
                    <p class="text-dark mb-0">${description}</p>
                    <p class="text-dark mb-0">${email}</p>
                </a>
            </div>
        </div>
    </div>
`;

$(document).ready(() => {
    // Generate dummy data
    // const google_classes = $('#classes-classroom');
    // google_classes.empty();
    // for (let i = 0; i < 10; i++) {
    //     google_classes.append(GoogleClass(
    //         "acdantis@up.edu.ph",
    //         "https://google.com",
    //         "Google Class",
    //         "This is a dummy description"
    //     ));
    // }
    return;

    // Get list of classes from API
    fetch('/api/v1/classes').then(response => response.json())
        .then(all_classes => {
            const google_classes = $('#classes-classroom');

            // Empty container
            google_classes.empty();

            // Iterate over each account in response data
            for (const [account_email, classes] of Object.entries(all_classes)) {
                // Create a new div for each class
                for (const class_data of classes) {
                    // Create a new class element
                    const class_element = GoogleClass(
                        account_email,
                        class_data.url,
                        class_data.name,
                        class_data.description
                    );

                    // Add the class element to the page
                    google_classes.append(class_element);
                }
            }
        });
});