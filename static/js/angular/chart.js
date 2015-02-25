(function() {
    google.load('visualization', '1', {
        packages: ['corechart']
    });

    var app = angular.module("googleChart", []);

    // Example of using $scope.
    app.controller("GenericChartCtrl", ['$http', '$log', '$scope', '$rootScope', '$timeout', '$window', function ($http, $log, $scope, $rootScope, $timeout, $window) {
        $scope.raw_data = [];
        $scope.jsonObj = [];
        $scope.chart_data = [];

        $scope.bfSelected = true;
        $scope.btlSelected = true;
        $scope.pmpSelected = true;
        $scope.peeSelected = true;
        $scope.pooSelected = true;
        $scope.napSelected = true;
        $scope.nightSelected = true;

        $scope.$watch(function() {
            $scope.prepareChart($scope.jsonObj);
            return $scope.chart_data;
        }, function() {
            $scope.draw();
        },true); // true is for deep object equality checking

        // Redraw the chart if the window is resized
        var resizeHandler = $rootScope.$on('resizeMsg', function() {
           $timeout(function() {
              $scope.draw();
           });
        });

        //Cleanup resize handler.
        $scope.$on('$destroy', function () {
            resizeHandler();
        });

        $scope.prepareChart = function(jsonObj) {
            var array = [];
            var header = []
            header.push('Week');
            if ($scope.bfSelected) {
                header.push('Breastfeeding (Hr)');
            }

            if ($scope.btlSelected) {
                header.push('Bottle (L)');
            }

            if ($scope.pmpSelected) {
                header.push('Pump (L)');
            }

            if ($scope.peeSelected) {
                header.push('Pee (Ct)');
            }

            if ($scope.pooSelected) {
                header.push('Poo (Ct)');
            }

            if ($scope.napSelected) {
                header.push('Nap (Hr)');
            }

            if ($scope.nightSelected) {
                header.push('Night (Hr)');
            }
            array.push(header);

            //$log.log(array);

            jsonObj.sort(function(a, b) {
               return a.start_millis - b.start_millis;
            });

            for (var i = 0; i < jsonObj.length; i++) {
                var item = [];
                item.push(jsonObj[i].week_number);
                if ($scope.bfSelected) {
                    item.push(jsonObj[i].breastfeeding_dur_sec / 60 / 60);
                }
                if ($scope.btlSelected) {
                    item.push(jsonObj[i].bottle_ml / 1000);
                }
                if ($scope.pmpSelected) {
                    item.push(jsonObj[i].pump_ml / 1000);
                }
                if ($scope.peeSelected) {
                    item.push(jsonObj[i].pee_ct);
                }
                if ($scope.pooSelected) {
                    item.push(jsonObj[i].poo_ct);
                }
                if ($scope.napSelected) {
                    item.push(jsonObj[i].nap_dur_sec / 60 / 60);
                }
                if ($scope.nightSelected) {
                    item.push(jsonObj[i].nighttime_dur_sec / 60 / 60);
                }
                array.push(item);
            }

            //$log.log(array);
            $scope.chart_data = array;
        };

        $scope.draw = function() {
            var data = google.visualization.arrayToDataTable($scope.chart_data);

            var vAxisType = '';

            var options = {
                title: 'Baby\'s activities from week to week.',
                hAxis: {title: 'Week Number'},
                vAxis: {title: vAxisType},
                seriesType: "bars"//,
                //series: {5: {type: "line"}}
            };
            var chart = new google.visualization.ComboChart(document.getElementById('chartdiv'));

            chart.draw(data, options);
        };

        $http
            .get('/api/prepareChart')
            .success(function(data) {
                //$log.log(data);
                //$log.log(data.chart);
                $scope.raw_data = data.chart;
                $scope.jsonObj = $.parseJSON($scope.raw_data);
                //$log.log('json' + $scope.jsonObj);

                $scope.prepareChart($scope.jsonObj);

                $scope.draw();
            })
            .error(function(error) {
                $log.log(error);
            });
    }]);

    // Setup the listener to 'resize' event and calls our 'resizeMsg'
    app.run(['$rootScope', '$window', function ($rootScope, $window){
        angular.element($window).bind('resize', function(){
           $rootScope.$emit('resizeMsg');
        });
    }]);
})();