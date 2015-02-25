var app = angular.module('babyDayBookFilters',[]);

app.filter('weight', function() {
  return function(input) {
      pounds = Math.floor(input / 16);
      ounces = input % 16;
      return pounds + ' lb ' + ounces + ' oz';
  };
});

app.filter('height', function() {
  return function(input) {
      feet = Math.floor(input / 12);
      inches = input % 12;

      if (input == 0)
      {
          return 'N/A';
      }
      else if (feet < 3)
      {
          return input + ' in';
      }
      else {
          return feet + ' ft ' + inches + ' in';
      }
  };
});

app.filter('percent', function() {
  return function(input) {
      if (input === 0) {
          return 'N/A';
      }
      else {
          return input + '%';
      }
  };
});

app.filter('time', function () {
   return function(input) {
       if (input.start_millis === 0)
       {
           return 'N/A';
       }
       else {
           if (input.end_millis === 0) {
               return new Date(input.start_millis).toLocaleString();
           }
           else
           {
               combine = new Date(input.start_millis).toLocaleString();
               seconds = (input.end_millis - input.start_millis)/1000;
               return combine + " (" + Math.floor(seconds / 60) + " min " + Math.floor(seconds % 60) + " sec)";
           }
       }
   };
});