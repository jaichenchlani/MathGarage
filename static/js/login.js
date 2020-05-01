(function() {
    var app = angular.module('loginMathgarage', []);

    // Actions when HTTP call is completed successfully.
    var LoginController = function($scope, $http, $window, $location, $rootScope) {
        console.log("Entering LoginController...");
        $scope.errorMessage = ""
        $scope.loginCredentials = {
            "username": "",
            "password": ""
        }
        $scope.forgotPassword = undefined

        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.loginInfo = response.data;
            console.log($scope.loginInfo)
            $rootScope.loginInfo = $scope.loginInfo

            switch($scope.loginInfo.is_valid_login_response.result) {
                case 0:
                  // LOGIN_SUCCESS
                  $scope.errorMessage = $scope.loginInfo.is_valid_login_response.message
                  $window.location.href = '/'
                  break;
                case 1:
                  // LOGIN_FAILURE
                  $scope.errorMessage = $scope.loginInfo.is_valid_login_response.message
                  $window.document.getElementById('forgotPassword').focus();
                  break;
                case 2:
                  // LOGIN_USER_DOES_NOT_EXIST
                  $scope.errorMessage = $scope.loginInfo.is_valid_login_response.message
                  $window.document.getElementById('createAccount').focus();
                  break;
                case 3:
                  // LOGIN_SERVER_ERROR
                  $scope.errorMessage = $scope.loginInfo.is_valid_login_response.message
                  $window.document.getElementById('inputUsername').focus();
                  break;
                default:
                $scope.errorMessage = "Something unexpected occcured."
                  // SOMETHING ELSE WENT WRONG.
              }
        }

        // Actions when HTTP call fails.
        var onError = function(reason) {
            console.log("Entering onError...");
            console.error("Error Details:" + JSON.stringify(reason));
            $window.alert("Error fetching data from the server.");
        }

        // Action from the HTML View
        $scope.login = function () {
            console.log("Entering generateMultiplicationFacts...");
            $scope.errorMessage = ""

            // Validate Username
            if ($scope.loginCredentials.username === undefined) {
                $scope.errorMessage = "Username Cannot be blank.";
                $window.document.getElementById('inputUsername').focus();
                return
            }
            // Validate Password
            if ($scope.loginCredentials.password === undefined) {
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
    app.controller('LoginController', LoginController);

})();