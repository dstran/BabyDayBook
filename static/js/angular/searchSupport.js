(function(){
   var app = angular.module('searchSupport', []);

    app.directive('searchResults', function() {
       return {
           restrict: 'E',
           templateUrl: '/static/templates/search-results.html' // Must put 'partials' at static folder
       };
    });
})();