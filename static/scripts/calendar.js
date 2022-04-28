const date = new Date();


//current month
const month = date.getMonth();
const year = date.getFullYear();
const days = new Date(year, month);

const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]




document.querySelector('h2').innerHTML = months[month] + " " + year;



var table = "";

//number of cells
for (let i = 0; i < days.getDay(); i++) {
    table += '<td></td>';
}

while (days.getMonth() == month) {
    table += '<td>' + days.getDate() + '</td>';

    if (days.getDay() % 6 == 0 && days.getDay() != 0) { 
      table += '</tr><tr>';
    }
    days.setDate(days.getDate() + 1);
}

if (days.getDay() != 0) {
    for (let i = days.getDay(); i < 7; i++) {
      table += '<td></td>';
    }
  }
  // close the table
table += '</tr></table>';

console.log(table);

document.querySelector('tbody').innerHTML = table;

