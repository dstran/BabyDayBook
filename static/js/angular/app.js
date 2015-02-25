(function() {
    var app = angular.module('babyDayBook', ['babyDayBookFilters', 'checkupSummary', 'searchSupport', 'googleChart']);

    app.controller('GrowthSummaryController', ['$http', '$log', function($http, $log) {
        this.entry = {};
        this.entries = [];
        var summaryCtrl = this;

        $http
            .get('/api/summary') // This string needs to match exactly with the 'route' string in flask! The extra slash at the end matters!!!
            .success(function(data) {
                //$log.log(data);
                //$log.log(data.summary);
                summaryCtrl.entries = data.summary;

                // uncomment when using mongodb
                //summaryCtrl.entries = data;
            })
            .error(function(error) {
                $log.log(error);
            });

        this.addCheckupResults = function(list) {
            list.push(this.entry);
            $http
                .post('/api/summaryAdd', {
                    item: this.entry
                })
                .success(function(data) {
                    //$log.log(data);
                })
                .error(function(error) {
                   $log.log(error);
                });
            this.entry = {}; // This will allow us to add multiple ones.
        };
    }]);

    app.controller('SearchController', ['$http', '$log', function($http, $log) {
        this.searchText = ''
        this.results = []
        var searchCtrl = this;

        this.searchResults = function(text) {
            this.searchText = text;
            $http
                .post('/api/search', {
                    item: this.searchText
                })
                .success(function(data) {
                    //$log.log(data.results);
                    searchCtrl.results = JSON.parse(data.results)
                })
                .error(function(error) {
                    $log.log(error);
                });
            this.results = []
            this.searchText = ''
        };
    }]);

    app.controller('LoginController', ['$log', function($log) {
        this.credentials = {
            email: '',
            password: ''
        }

        this.signin = function(credentials) {
            $log.log(credentials);
        };
    }]);
})();