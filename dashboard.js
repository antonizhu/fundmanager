/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace()

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        '01/10/2019',
        '02/10/2019',
        '03/10/2019',
        '04/10/2019',
        '05/10/2019',
        '06/10/2019',
        '07/10/2019'
      ],
      datasets: [{
        data: [
          0.625,
          0.953,
          1.887,
          2.503,
          2.819,
          2.896,
          0
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
}())
