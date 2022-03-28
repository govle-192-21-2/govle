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
});
