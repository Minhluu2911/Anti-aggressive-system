// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

// Area Chart Example
//var maxEmo = 100;
//var maxWater = 4;
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["8h - 9h", "9h - 10h", "10h - 11h", "11h - 12h", "13h - 14h", "14h - 15h", "15h - 16h", "16h - 17h"],
    datasets: [{
      label: "Emotion",
      lineTension: 0.3,
      backgroundColor: "rgba(0,0,0,0)",
      borderColor: "rgba(231, 74, 59, 1)",
      pointRadius: 3,
      pointBackgroundColor: "rgba(231, 74, 59, 1)",
      pointBorderColor: "rgba(231, 74, 59, 1)",
      pointHoverRadius: 3,
      pointHoverBackgroundColor: "rgba(231, 74, 59, 1)",
      pointHoverBorderColor: "rgba(231, 74, 59, 1)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      //data: [0.8, 0.7, 0.5, 0.65, 0.9, 0.3, 0.15, 0.6],
      data: emotionData,
    }, {
      label: "Water",
      lineTension: 0.3,
      backgroundColor: "rgba(78, 115, 223, 0)",
      borderColor: "rgba(78, 115, 223, 1)",
      pointRadius: 3,
      pointBackgroundColor: "rgba(78, 115, 223, 1)",
      pointBorderColor: "rgba(78, 115, 223, 1)",
      pointHoverRadius: 3,
      pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
      pointHoverBorderColor: "rgba(78, 115, 223, 1)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      //data: [0, 0.2, 0.25, 0.22, 0.4, 0.1, 0.05, 0.15],
      data: waterData,
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 6,
          padding: 10,
          callback: function(value, index, values) {
            return value * maxEmo + ' / ' + value * maxWater + 'l';
          }
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          if (datasetLabel == 'Emotion') {
            return datasetLabel + ': ' + (tooltipItem.yLabel * maxEmo).toFixed(2);
          }
          return datasetLabel + ': ' + (tooltipItem.yLabel * maxWater).toFixed(2) + 'l';
        }
      }
    }
  }
});
