(function() {
    var app = angular.module('loginMathgarage', []);

    // Actions when HTTP call is completed successfully.
    var LoginController = function($scope, $http, $window, $location, $rootScope) {
        console.log("Entering LoginController...");
        $scope.errorMessage = ""
        $scope.resetPasswordErrorMessage = ""
        $scope.loginCredentials = {}
        $scope.showForgotPasswordSection = false

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
                    // SOMETHING ELSE WENT WRONG.
                    $scope.errorMessage = "Something unexpected occcured. Please try again later."
                    $window.document.getElementById('inputUsername').focus();
              }
        }

        // Actions when HTTP call fails.
        var onError = function(reason) {
            console.log("Entering onError...");
            console.error("Error Details:" + JSON.stringify(reason));
            $window.alert("Error fetching data from the server.");
        }

        // Actions when HTTP call fails.
        var onResetPasswordComplete = function(response) {
            console.log("Entering onResetPasswordComplete...");
            $scope.loginInfo = response.data;
            console.log($scope.loginInfo)

            switch($scope.loginInfo.is_valid_login_response.result) {
                case 0:
                  // LOGIN_SUCCESS
                  $scope.resetPasswordErrorMessage = undefined
                  $window.alert("Password Reset Successful. An email with the correct passwoard has been sent to your registered email id.");
                  $window.location.href = '/'
                  break;
                case 1:
                  // LOGIN_FAILURE
                  $scope.resetPasswordErrorMessage = "Incorrect Forgot Password Answer. Please try again."
                  $window.document.getElementById('inputForgotPasswordAnswer').focus();
                  break;
                case 2:
                  // LOGIN_USER_DOES_NOT_EXIST
                  $scope.resetPasswordErrorMessage = $scope.loginInfo.is_valid_login_response.message
                  $window.document.getElementById('inputForgotPasswordAnswer').focus();
                  break;
                case 3:
                  // LOGIN_SERVER_ERROR
                  $scope.resetPasswordErrorMessage = $scope.loginInfo.is_valid_login_response.message
                  $window.document.getElementById('inputForgotPasswordAnswer').focus();
                  break;
                default:
                    // SOMETHING ELSE WENT WRONG.
                    $scope.resetPasswordErrorMessage = "Server error. Please try again later."
                    $window.document.getElementById('inputForgotPasswordAnswer').focus();
              }
        }

        // Actions when HTTP call fails.
        var onGetForgotPasswordQuestionComplete = function(response) {
            console.log("Entering onForgotPasswordComplete...");
            $scope.loginCredentials = response.data;
            if (!$scope.loginCredentials.validOutputReturned) {
                // System Error.
                $scope.errorMessage = "Error fetching forgot password question from the server. Please try again..";
                return
            }
            if (!$scope.loginCredentials.isValidUser) {
                // Not a valid user.
                $scope.errorMessage = $scope.loginCredentials.message;
                $window.document.getElementById('inputUsername').focus();
                $scope.showForgotPasswordSection = false
                return
            }

            $window.document.getElementById('inputForgotPasswordAnswer').focus();
            console.log($scope.loginCredentials)
        }
        
        // Action from the HTML View
        $scope.login = function () {
            console.log("Entering generateMultiplicationFacts...");
            $scope.errorMessage = ""

            // Validate Username
            if ($scope.loginCredentials.username === undefined) {
                $scope.errorMessage = "Username cannot be blank.";
                $window.document.getElementById('inputUsername').focus();
                return
            }
            // Validate Password
            if ($scope.loginCredentials.password === undefined) {
                $scope.errorMessage = "Password cannot be blank.";
                $window.document.getElementById('inputPassword').focus();
                return
            }

            calledURL = "/login"
            console.log("Calling " + calledURL + "...")
            
            $http.put(calledURL, $scope.loginCredentials)
                .then(onUserComplete, onError);
        };

        $scope.forgotPassword = function() {
            console.log("Entering forgotPassword...");
            console.log($scope.loginCredentials.username)
            // Validate Username
            if ($scope.loginCredentials.username === undefined) {
                $scope.errorMessage = "Username cannot be blank.";
                $window.document.getElementById('inputUsername').focus();
                return
            }

            calledURL = "/get-forgot-password-question"
            console.log("Calling " + calledURL + "...")
            
            $http.put(calledURL, $scope.loginCredentials)
                .then(onGetForgotPasswordQuestionComplete, onError);

            $scope.showForgotPasswordSection = true
        };

        $scope.resetPassword = function() {
            console.log("Entering getPassword...");
            // Validate Username
            if ($scope.loginCredentials.username === undefined) {
                $scope.errorMessage = "Username cannot be blank.";
                $window.document.getElementById('inputUsername').focus();
                return
            }
            // Validate Forgot Password Answer
            if ($scope.loginCredentials.forgot_password_answer === undefined) {
                $scope.errorMessage = "Forgot Password Answer cannot be blank.";
                $window.document.getElementById('inputForgotPasswordAnswer').focus();
                return
            }
            // Validate Forgot Password Answer
            if ($scope.loginCredentials.forgot_password_answer === "") {
                $scope.errorMessage = "Forgot Password Answer cannot be blank.";
                $window.document.getElementById('inputForgotPasswordAnswer').focus();
                return
            }

            calledURL = "/reset-password"
            console.log("Calling " + calledURL + "...")
            
            $http.put(calledURL, $scope.loginCredentials)
                .then(onResetPasswordComplete, onError);
        };

        // Action from the HTML View    
        $scope.reset = function() {
            console.log("Entering reset...");
            $scope.loginCredentials = {}
            $scope.showForgotPasswordSection = false
            $window.document.getElementById('inputUsername').focus();
        };

    };

    // Register the Controller with the app
    app.controller('LoginController', LoginController);

})();