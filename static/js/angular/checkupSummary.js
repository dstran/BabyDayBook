(function(){
   var app = angular.module('checkupSummary', []);

    app.directive('growthSummary', function() {
       return {
           restrict: 'E',
           templateUrl: '/static/templates/growth-summary.html' // Must put 'partials' at static folder
       };
    });

    app.directive('summaryInput', function() {
       return {
           restrict: 'E',
           templateUrl: '/static/templates/summary-input.html'
       };
    });
})();