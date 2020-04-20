(function() {
    var app = angular.module('multiplicationFacts', []);

    // Actions when HTTP call is completed successfully.
    var MultiplicationFactsController = function($scope, $http, $window, $location) {
        console.log("Entering MultiplicationFactsController...");
        $window.document.getElementById('inputTableof').focus();
        $scope.errorMessage = ""
        $scope.showSystemAnswer = false
        $scope.facts = {}
        $scope.facts.request = {
            "tableof": 131,
            "limit": 50
        }


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

        // Action from the HTML View
        $scope.generateMultiplicationFacts = function () {
            console.log("Entering generateMultiplicationFacts...");
            $scope.errorMessage = ""

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

        // Call the function on page load.
        $scope.generateMultiplicationFacts($scope.facts, $scope.errorMessage);

    };

    // Register the Controller with the app
    app.controller('MultiplicationFactsController', ['$scope', '$http', '$window', '$location', MultiplicationFactsController]);

})();