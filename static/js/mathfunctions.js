(function() {
    var app = angular.module('mathFunctions', []);

    var MathFunctionsController = function($scope, $http, $window) {
        console.log("Entering MathFunctionsController...");
        $window.document.getElementById('inputDecimalInput').focus();
        $scope.errorMessage = ""
        
        // Actions when HTTP call is completed successfully.
        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.binaryOutput = response.data.answer;
            $window.document.getElementById('inputDecimalInput').focus();
            // console.log($scope.binaryOutput);
        }

        // Actions when HTTP call fails.
        var onError = function(reason) {
            console.log("Entering onError...");
            console.error("Error Details:" + JSON.stringify(reason));
            $window.alert("Error fetching data from the server.");
        }

        // Action from the HTML View
        $scope.getDecimalToBinary = function (decimalInput, errorMessage) {
            console.log("Entering getDecimalToBinary...");
            $scope.errorMessage = ""
            // Validate Inputs
            if (decimalInput === undefined) {
                $scope.errorMessage = "Decimal Input Cannot be blank.";
                $window.document.getElementById('inputDecimalInput').focus();
                return
            }
            if (decimalInput < 0) {
                $scope.errorMessage = "Decimal Input Cannot be negative.";
                $window.document.getElementById('inputDecimalInput').focus();
                return
            }
            
            // console.log(decimalInput);
            calledURL = "/math-functions/d2b/" + decimalInput
            console.log("Calling " + calledURL + "...")
    
            $http.get(calledURL)
                .then(onUserComplete, onError);
        };

    };

    // Register the Controller with the app
    app.controller('MathFunctionsController', ['$scope', '$http', '$window', MathFunctionsController]);

})();