(function() {
    // var app = angular.module('mathgarage', []);
    var app = angular.module('mathgarage', []);

    // Actions when HTTP call is completed successfully.
    var MultiplicationFactsController = function($scope, $http, $window, $interval, $routeParams, $route, mathgarageServices) {
        console.log("Entering MultiplicationFactsController...");
        
        // var onUserComplete = function(response) {
        var onUserComplete = function(data) {
            console.log("Entering onUserComplete...");
            // $scope.facts = response.data;
            $scope.facts = data;
            $scope.facts.message = "Multiplication Facts for " 
                                    + $scope.facts.request.tableof + " upto a limt of " 
                                    + $scope.facts.request.limit + " generated.";
            console.log($scope.facts);
            // Set the focus on the Get Multiplication Facts button.
            $window.document.getElementById('getMultiplicationFacts').focus();
            $scope.showSystemAnswer = true
            $scope.gotoResultSection();
        }

        // Actions when HTTP call fails.
        var onError = function(reason) {
            console.log("Entering onError...");
            console.error("Error Details:" + JSON.stringify(reason));
            $window.alert("Error fetching data from the server.");
        }

        var decrementCountdown = function() {
            $scope.countdown -= 1;
            $scope.countdownMessage = "Starting the default search in " + $scope.countdown + " secs."
            if ($scope.countdown < 1) {
                $scope.generateMultiplicationFacts()        
            };
        };

        var countdownInterval = null
        var startCountdown = function() {
            countdownInterval = $interval(decrementCountdown, 1000, $scope.countdown);
        };

        // Action from the HTML View
        $scope.generateMultiplicationFacts = function () {
            console.log("Entering generateMultiplicationFacts...");
            $scope.errorMessage = ""
            $scope.countdownMessage = undefined
            console.log($scope.facts)

            // Validate Inputs
            if ($scope.facts.request.tableof === undefined) {
                $scope.errorMessage = "Table Of Input Cannot be blank.";
                $window.document.getElementById('inputTableof').focus();
                return
            }
            if ($scope.facts.request.tableof < 0) {
                $scope.errorMessage = "Table Of Input Cannot be negative.";
                $window.document.getElementById('inputTableof').focus();
                return
            }
            if ($scope.facts.request.limit === undefined) {
                $scope.errorMessage = "Limit Input Cannot be blank.";
                $window.document.getElementById('inputLimit').focus();
                return
            }
            if ($scope.facts.request.limit < 1) {
                $scope.errorMessage = "Limit Input Cannot be zero or negative.";
                $window.document.getElementById('inputLimit').focus();
                return
            }

            // console.log(facts);
            calledURL = "/get-multiplication-facts/" + $scope.facts.request.tableof + "/" + $scope.facts.request.limit
            console.log("Calling " + calledURL + "...")
            
            // $http.get(calledURL)
            mathgarage.generateMultiplicationFacts(calledURL)
                .then(onUserComplete, onError);

            // If the user performs the operation ahead of the 5 sec timer, cancel the timer to avoid running 2 requests
            if (countdownInterval) {
                $interval.cancel(countdownInterval)
            }
        };

        // Action from the HTML View    
        $scope.reset = function() {
            console.log("Entering reset...");
            $scope.facts.result = {}
            $scope.countdownMessage = undefined
            $scope.showSystemAnswer = false
            $window.document.getElementById('inputTableof').focus();
        };

        $scope.gotoResultSection = function() {
            console.log("Entering gotoResultSection...");
            var newHash = 'resultsection';
            if ($location.hash() !== newHash) {
                $location.hash(newHash);
            }
        };

        $window.document.getElementById('inputTableof').focus();
        $scope.errorMessage = ""
        $scope.showSystemAnswer = false
        $scope.facts = {}
        $scope.facts.request = {
            "tableof": 131,
            "limit": 50
        }
        $scope.countdown = 5;
        $scope.countdownMessage = "Starting the default search in " + $scope.countdown + " secs."
        startCountdown();
    };

    // Register the Controller with the app
    app.controller('MultiplicationFactsController', MultiplicationFactsController);

})();