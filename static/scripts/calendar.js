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

var uvle_deadlines_list = []


function getPreviousMonth(days){
  days.setMonth(days.getMonth()-2);
  //change year if ganito
  getCalendarCurrent(days);
 }
 
function getNextMonth(days){
   days.setMonth(days.getMonth());
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
    for (let dates of uvle_deadlines_list){
      console.log(dates);
      //if (days.getMonth() == month && days.getDate() == dates[0]){
        //for (deadline_for_the_day in dates){
        //table += `<div class = "uvle-box"> <b>${dates[1]}</b> ${deadline_for_the_day}</div>`;
        //table += '<br>'
      //}
      
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

$(document).ready(() => {
  fetch('/api/v1/moodle/deadlines').then(response => response.json())
    .then(uvle_deadlines => {
      for (let date in uvle_deadlines){
        const date_split = date.split('-');
        const deadline_month = months[parseInt(date_split[1]) - 1];
        const day = date_split[2];
        list = [];
        list.push(day);
        if (deadline_month == months[days.getMonth()-1]){;
        for (let subjects in uvle_deadlines[date]){
          list.push(subjects);
          for (let deadline_names in uvle_deadlines[date][subjects].deadlines){
            deadline_list = [];
            deadline_list.push(((uvle_deadlines[date][subjects].deadlines)[deadline_names]).name);
            
          }
          
          list.push(deadline_list);
        }
        uvle_deadlines_list.push(list);
        }
      }

 
      });
  
  
  
  fetch('/api/v1/google/coursework').then(response => response.json())
    .then(google_deadlines => {
        //console.log(google_deadlines);
    });

    getCalendarCurrent(days); 
  
  });