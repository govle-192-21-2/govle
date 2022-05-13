const date = new Date();



//current month
var month = date.getMonth();
var year = date.getFullYear();
var days = new Date(year, month);

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

fetch('/api/v1/moodle/deadlines').then(response => response.json())
  .then(uvle_deadlines => {
      console.log(uvle_deadlines);
  });


fetch('/api/v1/google/coursework').then(response => response.json())
  .then(google_deadlines => {
      console.log(google_deadlines);
  });


getCalendarCurrent(days);


function getPreviousMonth(days){
  days.setMonth(days.getMonth()-2);
  //change year if ganito
  console.log(days);
  getCalendarCurrent(days);
 }
 
function getNextMonth(days){
   days.setMonth(days.getMonth()+1);
   console.log(days);
   //change year if ganito
   getCalendarCurrent(days);
 }

function getCalendarCurrent(days){
document.querySelector('h2').innerHTML = months[days.getMonth()] + " " + days.getFullYear();
month = days.getMonth();
var table = ""; 
//number of cells
//gets kung pang-ilang day yung simula nung calendar
for (let i = 0; i < days.getDay(); i++) {
    table += '<td></td>';
}

while (days.getMonth() == month) {
    table += '<td>' + '<div class = "calendar-numbers">' + days.getDate() + '</div>';
    if (days.getMonth() == 4 && days.getDate() == 30){
      table += '<div class = "uvle-box"> <b>CS 150</b> Deadline</div>';
    }
    table += '</td>';
    if (days.getDay() % 6 == 0 && days.getDay() != 0) { 
      table += '</tr><tr>';
    }
    //iterate
    days.setDate(days.getDate() + 1);
}

if (days.getDay() != 0) {
    for (let i = days.getDay(); i < 7; i++) {
      table += '<td></td>';
    }
  }
  // close the table
table += '</tr></table>';



document.querySelector('tbody').innerHTML = table;
}

//get classes from UVLE and google classroom
//if UVLE red if GClass green
//