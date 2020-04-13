(function() {
    var app = angular.module('loginMathgarage', []);

    // Actions when HTTP call is completed successfully.
    var LoginController = function($scope, $http, $window, $location) {
        console.log("Entering LoginController...");
        $scope.errorMessage = ""
        $scope.loginCredentials = {
            "username": "",
            "password": ""
        }

        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.loginInfo = response.data;
            console.log($scope.loginInfo)

            // Redirect to Home Page.
            $window.location.href = '/';

        }

        // Actions when HTTP call fails.
        var onError = function(reason) {
            console.log("Entering onError...");
            console.error("Error Details:" + JSON.stringify(reason));
            $window.alert("Error fetching data from the server.");
        }

        // Action from the HTML View
        $scope.login = function (loginCredentials, errorMessage) {
            console.log("Entering generateMultiplicationFacts...");
            $scope.errorMessage = ""

            // Validate Username
            if (loginCredentials.username === undefined) {
                $scope.errorMessage = "Username Cannot be blank.";
                $window.document.getElementById('inputUsername').focus();
                return
            }
            // Validate Password
            if (loginCredentials.password === undefined) {
                $scope.errorMessage = "Password Cannot be blank.";
                $window.document.getElementById('inputPassword').focus();
                return
            }

            // console.log(facts);
            calledURL = "/login"
            console.log("Calling " + calledURL + "...")
            
            $http.put(calledURL, $scope.loginCredentials)
                .then(onUserComplete, onError);
        };

        // Action from the HTML View    
        $scope.reset = function() {
            console.log("Entering reset...");
            $scope.loginCredentials = {
                "username": "",
                "password": ""
            }
            $window.document.getElementById('inputUsername').focus();
        };

    };

    // Register the Controller with the app
    app.controller('LoginController', ['$scope', '$http', '$window', '$location', LoginController]);

})();