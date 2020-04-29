(function() {
    // var app = angular.module('numberWiki', []);
    var app = angular.module('mathgarage', []);

    var NumberWikiController = function($scope, $http, $window, $interval, $routeParams, $route) {
        console.log("Entering NumberWikiController...");
        
        
        // Actions when HTTP call is completed successfully.
        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.number = response.data;
            $window.document.getElementById('reset').focus();
            console.log($scope.number);
        };

        // Actions when HTTP call fails.
        var onError = function(reason) {
            console.log("Entering onError...");
            console.error("Error Details:" + JSON.stringify(reason));
            $window.alert("Error fetching data from the server.");
        };

        var decrementCountdown = function() {
            $scope.countdown -= 1;
            $scope.countdownMessage = "Starting the default search in " + $scope.countdown + " secs."
            if ($scope.countdown < 1) {
                $scope.getNumberWikiData()        
            };
        };

        var countdownInterval = null
        var startCountdown = function() {
            countdownInterval = $interval(decrementCountdown, 1000, $scope.countdown);
        };

        // Action from the HTML View
        $scope.getNumberWikiData = function () {
            console.log("Entering getNumberWikiData...");
            $scope.countdownMessage = undefined;
            $scope.errorMessage = ""
            // Validate Inputs
            if ($scope.n === undefined) {
                $scope.errorMessage = "Input Cannot be blank.";
                $window.document.getElementById('numberInput').focus();
                return
            }
            if ($scope.n < 0) {
                $scope.errorMessage = "Number Input Cannot be negative.";
                $window.document.getElementById('numberInput').focus();
                return
            }
            if ($scope.n > 9999999) {
                $scope.errorMessage = "Number Input must be less than 10 Million.";
                $window.document.getElementById('numberInput').focus();
                return
            }
            
            $scope.showSystemAnswer = true

            // console.log($scope.n);
            calledURL = "/number-wiki/" + $scope.n
            console.log("Calling " + calledURL + "...")
    
            $http.get(calledURL)
                .then(onUserComplete, onError);
            
            // If the user performs the operation ahead of the 5 sec timer, cancel the timer to avoid running 2 requests
            if (countdownInterval) {
                $interval.cancel(countdownInterval)
            }
        };

         // Action from the HTML View    
         $scope.reset = function() {
            console.log("Entering reset...");
            $scope.number = {}
            $scope.showSystemAnswer = false
            $window.document.getElementById('numberInput').focus();
            $scope.countdownMessage = undefined;
        };

        $window.document.getElementById('numberInput').focus();
        $scope.errorMessage = "";
        $scope.userMessage = "Input number should be less than 10 Million i.e. Max 9,999,999.";
        $scope.countdown = 5;
        $scope.countdownMessage = "Starting the default search in " + $scope.countdown + " secs."
        startCountdown();
    };

    // Register the Controller with the app
    // app.controller('NumberWikiController', ['$scope', '$http', '$window', '$interval', NumberWikiController]);
    app.controller('NumberWikiController', NumberWikiController);

})();