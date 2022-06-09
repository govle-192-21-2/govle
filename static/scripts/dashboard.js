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
const buildDeadlineList = (rawDeadlineList) => {
    let mergedDeadlineList;
    if (rawDeadlineList.length === 1) {
        mergedDeadlineList = rawDeadlineList[0];

        // Uncenter container contents
        $('#deadlines-container').removeClass('text-center');
    } else {
        // Merge both deadline lists
        mergedDeadlineList = Object.assign({}, rawDeadlineList[0], rawDeadlineList[1]);
    
        // Remove spinner
        $('#deadlines-container .spinner-border').remove();
    }

    // Iterate through each date
    let num_deadlines = 0;
    for (let date in mergedDeadlineList) {
        // Parse YYYY-MM-DD date into MM and DD
        const date_split = date.split('-');
        const month = MonthNames[parseInt(date_split[1]) - 1];
        const day = date_split[2];

        // Iterate through each course
        const deadlineSetList = [];
        for (let course in mergedDeadlineList[date]) {
            // Iterate through each deadline
            const deadlineList = [];
            for (let deadline in mergedDeadlineList[date][course]['deadlines']) {
                // Add deadline to list
                deadlineList.push(Deadline(
                    mergedDeadlineList[date][course]['deadlines'][deadline]['name'],
                    mergedDeadlineList[date][course]['deadlines'][deadline]['url']
                ));

                // Increment number of deadlines
                num_deadlines++;
            }

            // Concat all deadline elements into one string
            const deadlineSet = DeadlineSet(
                course,
                mergedDeadlineList[date][course]['url'],
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
};

$(document).ready(() => {
    // Update greeting with proper time of day
    const timeOfDayGreeting = $('#time-of-day');
    const currentHour = new Date().getHours();
    let timeOfDay = 'day';
    if (currentHour < 12) {
        timeOfDayGreeting.text('morning');
    } else if (currentHour < 18) {
        timeOfDayGreeting.text('afternoon');
    } else {
        timeOfDayGreeting.text('evening');
        timeOfDay = 'night';
    }

    // Get weather from API
    fetch(`/api/v1/weather?timeOfDay=${timeOfDay}`).then(response => response.json())
        .then(weather => {
            $('#weather-icon').addClass(`wi-${weather.icon}`);
            $('#weather-temp').html(`${weather.temperature}&deg;C`);
            $('#weather-desc').text(`${weather.condition} in ${weather.place}`);
            $('#weather-fl').html(`Feels like ${weather.feels_like}&deg;C`);
        });

    // Get list of deadlines from API
    let deadlines = [];
    fetch('/api/v1/moodle/deadlines').then(response => response.json())
        .then(moodle_deadlines => {
            // If the dict is empty, display a message saying so.
            if (Object.keys(moodle_deadlines).length === 0) {
                $('#deadlines-container').append(`<p class="text-center">No deadlines from UVL&#234;.</p>`);
            }
            deadlines.push(moodle_deadlines);
        })
        .then(() => buildDeadlineList(deadlines));
    fetch('/api/v1/google/coursework').then(response => response.json())
        .then(google_deadlines => {
            // If the list is empty, display a message saying so.
            if (Object.keys(google_deadlines).length === 0) {
                $('#deadlines-container').append(`<p class="text-center">No deadlines from Google Classroom.</p>`);
            }
            deadlines.push(google_deadlines)
        })
        .then(() => buildDeadlineList(deadlines));
});
