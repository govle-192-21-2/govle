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
    fetch('/api/v1/google/coursework').then(response => response.json())
        .then(google_coursework => {
            const google_coursework_el = $('#classroom-deadlines');
            google_coursework_el.empty();
            google_coursework_el.text(google_coursework);
        });
});
