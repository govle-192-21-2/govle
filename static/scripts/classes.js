const GoogleClass = (email, url, title, description) => `
    <div class="col-12 mb-4 col-lg-4 col-md-6 col-xs-12">
        <div class="card">
            <div class="card-body">
                <a class="govle-class" href="${url}?authuser=${email}" rel="noopener" target="_blank">
                    <h4 class="text-dark mb-3"><span>${title}</span><span>&#8599;</span></h4>
                    <p class="text-dark mb-0">${description}</p>
                    <p class="text-secondary mb-0">${email}</p>
                </a>
            </div>
        </div>
    </div>
`;

const MoodleClass = (url, title, description, progress) => `
    <div class="col-12 mb-4 col-lg-4 col-md-6 col-xs-12">
        <div class="card">
            <div class="card-body">
                <a class="govle-class" href="${url}" rel="noopener" target="_blank">
                    <h4 class="text-dark mb-3"><span>${title}</span><span>&#8599;</span></h4>
                    <p class="text-dark mb-0">${description}</p>
                    <div class="progress mt-2">
                        <div class="progress-bar bg-success" role="progressbar"
                            aria-valuemin="0" aria-valuemax="100"
                            style="width: ${progress}%" aria-valuenow="${parseInt(progress)}">
                            ${parseInt(progress)}%
                        </div>
                    </div>
                </a>
            </div>
        </div>
    </div>
`;

$(document).ready(() => {
    // Get list of classes from API
    fetch('/api/v1/moodle/courses').then(response => response.json())
        .then(moodle_classes => {
            const moodle_classes_el = $('#classes-moodle');

            // Empty container
            moodle_classes_el.empty();

            // Create a new div for each class
            moodle_classes.forEach(moodle_class => {
                // Round completion status to 1 decimal place
                const progress = Math.round(moodle_class.completion_status * 10) / 10;

                // Create a new class element
                const class_element = MoodleClass(
                    moodle_class.url,
                    moodle_class.name,
                    moodle_class.description,
                    progress
                )

                // Add the class element to the page
                moodle_classes_el.append(class_element);
            });
        });
    fetch('/api/v1/google/classes').then(response => response.json())
        .then(google_classes => {
            const google_classes_el = $('#classes-classroom');

            // Empty container
            google_classes_el.empty();

            // Iterate over each account in response data
            for (const [account_email, classes] of Object.entries(google_classes)) {
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
                    google_classes_el.append(class_element);
                }
            }
        });
});