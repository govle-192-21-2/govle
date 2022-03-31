const GoogleClass = (email, url, title, description) => `
<div class="row row-cols-1 row-cols-md-3">
    <div class="col mb-4">
        <div class="card " style="width:15rem;">
            <div class="card-body">
                <a class="govle-class" href="${url}" rel="noopener" target="_blank">
                    <h3 class="text-dark">${title} &#8599</h3>
                    <p class="text-dark">${description}</p>
                    <p class="text-dark">${email}</p>
                </a>
            </div>
        </div>
    </div>
</div>
`;

$(document).ready(() => {
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