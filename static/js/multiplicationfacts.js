(function() {
    var app = angular.module('multiplicationFacts', []);

    // Actions when HTTP call is completed successfully.
    var MultiplicationFactsController = function($scope, $http, $window, $location, $interval) {
        console.log("Entering MultiplicationFactsController...");
        
        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.facts = response.data;
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

        var startCountdown = function() {
            $interval(decrementCountdown, 1000, $scope.countdown);
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
            
            $http.get(calledURL)
                .then(onUserComplete, onError);
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
            // console.log($location.hash());
            // console.log(newHash);
            if ($location.hash() !== newHash) {
                // console.log($location.hash());
                // console.log(newHash);
                // set the $location.hash to `newHash` and
                // $anchorScroll will automatically scroll to it
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