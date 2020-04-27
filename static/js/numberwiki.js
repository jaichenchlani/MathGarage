(function() {
    var app = angular.module('numberWiki', []);

    var NumberWikiController = function($scope, $http, $window) {
        console.log("Entering NumberWikiController...");
        $window.document.getElementById('numberInput').focus();
        $scope.errorMessage = ""
        $scope.userMessage = "Input number should be less than 10 Million i.e. Max 9,999,999."
        
        // Actions when HTTP call is completed successfully.
        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.number = response.data;
            $window.document.getElementById('reset').focus();
            console.log($scope.number);
        }

        // Actions when HTTP call fails.
        var onError = function(reason) {
            console.log("Entering onError...");
            console.error("Error Details:" + JSON.stringify(reason));
            $window.alert("Error fetching data from the server.");
        }

        // Action from the HTML View
        $scope.getNumberWikiData = function () {
            console.log("Entering getNumberWikiData...");
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

            console.log($scope.n);
            calledURL = "/number-wiki/" + $scope.n
            console.log("Calling " + calledURL + "...")
    
            $http.get(calledURL)
                .then(onUserComplete, onError);
        };

         // Action from the HTML View    
         $scope.reset = function() {
            console.log("Entering reset...");
            $scope.number = {}
            $scope.showSystemAnswer = false
            $window.document.getElementById('numberInput').focus();
        };

    };

    // Register the Controller with the app
    app.controller('NumberWikiController', ['$scope', '$http', '$window', NumberWikiController]);

})();