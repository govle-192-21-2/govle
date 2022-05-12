const DeadlineRow = (day, month, deadlineSetList) => `
    <div class="deadline">
        <div class="deadline-date">
            <h1>${day}</h1>
            <h6>${month}</h6>
        </div>
        <div class="deadline-detail">${deadlineSetList}</div>
    </div>
`;
const DeadlineSet = (courseName, courseLink, deadlineList) => `
    <div class="deadline-set">
        <h2>${courseName} <a href="${courseLink}" class="course-link" target="_blank" rel="noopener">Open...</a></h2>
        <ul>${deadlineList}</ul>
    </div>
`;
const Deadline = (deadlineName, deadlineLink) => `
    <li>
        <a href=${deadlineLink} target="_blank" rel="noopener">${deadlineName}</a>
    </li>
`;
const MonthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

$(document).ready(() => {
    // Update greeting with proper time of day
    const timeOfDayGreeting = $('#time-of-day');
    const currentHour = new Date().getHours();
    if (currentHour < 12) {
        timeOfDayGreeting.text('morning');
    } else if (currentHour < 18) {
        timeOfDayGreeting.text('afternoon');
    } else {
        timeOfDayGreeting.text('evening');
    }

    // Get list of deadlines from API
    fetch('/api/v1/moodle/deadlines').then(response => response.json())
        .then(moodle_deadlines => {
            // Empty container
            $('#deadlines-container').empty();

            // Iterate through each date
            let num_deadlines = 0;
            for (let date in moodle_deadlines) {
                // Parse YYYY-MM-DD date into MM and DD
                const date_split = date.split('-');
                const month = MonthNames[parseInt(date_split[1]) - 1];
                const day = date_split[2];

                // Iterate through each course
                const deadlineSetList = [];
                for (let course in moodle_deadlines[date]) {
                    // Iterate through each deadline
                    const deadlineList = [];
                    for (let deadline in moodle_deadlines[date][course]['deadlines']) {
                        // Add deadline to list
                        deadlineList.push(Deadline(
                            moodle_deadlines[date][course]['deadlines'][deadline]['name'],
                            moodle_deadlines[date][course]['deadlines'][deadline]['url']
                        ));

                        // Increment number of deadlines
                        num_deadlines++;
                    }

                    // Concat all deadline elements into one string
                    const deadlineSet = DeadlineSet(
                        course,
                        moodle_deadlines[date][course]['url'],
                        deadlineList.join('')
                    );
                    deadlineSetList.push(deadlineSet);
                }

                // Concat all deadline set elements into one string
                const deadlineRow = DeadlineRow(
                    day,
                    month,
                    deadlineSetList.join('')
                );

                $('#deadlines-container').append(deadlineRow);
            }

            // Update number of deadlines
            const with_s = num_deadlines === 1 ? '' : 's';
            $('#deadlines-overview').text(`${num_deadlines} assignment${with_s}`);
        });
    // fetch('/api/v1/google/coursework').then(response => response.json())
    //     .then(google_coursework => {
    //         const google_coursework_el = $('#classroom-deadlines');
    //         google_coursework_el.empty();
    //         google_coursework_el.text(google_coursework);
    //     });
});
