$(document).ready(() => {
    // Get list of classes from API
    fetch('/api/v1/classes').then(response => response.text())
        .then(classes => console.log(classes));
});