(function() {
    var app = angular.module('createAccountMathgarage', []);

    // Actions when HTTP call is completed successfully.
    var CreateAccountController = function($scope, $http, $window, $location, $rootScope) {
        console.log("Entering CreateAccountController...");
        $scope.username = sessionStorage.getItem('username')
        
        $scope.errorMessage = ""
        $scope.user = {
            "username": "",
            "password": "",
            "first_name": "",
            "last_name": "",
            "email": ""
        }

        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.user = response.data;
            // console.log($scope.user)
            if ($scope.user.created_userInfo.result) {
                // All good. User got created in Data Store. Redirect to Home Page.
                sessionStorage.setItem('username',$scope.user.userInfo.username)
                $window.location.href = '/';
            } else {
                $scope.errorMessage = $scope.user.created_userInfo.message
            }
        }

        // Actions when HTTP call fails.
        var onError = function(reason) {
            console.log("Entering onError...");
            console.error("Error Details:" + JSON.stringify(reason));
            $window.alert("Error fetching data from the server.");
        }

        // Action from the HTML View
        $scope.createAccount = function () {
            console.log("Entering createAccount...");
            $scope.errorMessage = ""

            // Validate Username
            if ($scope.user.userInfo.username === undefined) {
                $scope.errorMessage = "Username Cannot be blank.";
                $window.document.getElementById('inputUsername').focus();
                return
            }
            // Validate Password
            if ($scope.user.userInfo.password === undefined) {
                $scope.errorMessage = "Password Cannot be blank.";
                $window.document.getElementById('inputPassword').focus();
                return
            }

            // Validate First Name
            if ($scope.user.userInfo.first_name === undefined) {
              $scope.errorMessage = "First Name Cannot be blank.";
              $window.document.getElementById('inputFirstName').focus();
              return
            }

            // Validate Last Name
            if ($scope.user.userInfo.last_name === undefined) {
              $scope.errorMessage = "Last Name Cannot be blank.";
              $window.document.getElementById('inputLastName').focus();
              return
            }

            // Validate Email
            if ($scope.user.userInfo.email === undefined) {
              $scope.errorMessage = "Email Cannot be blank.";
              $window.document.getElementById('inputEmail').focus();
              return
            }

            // console.log(facts);
            calledURL = "/create-account"
            console.log("Calling " + calledURL + "...")
            
            $http.put(calledURL, $scope.user.userInfo)
                .then(onUserComplete, onError);
        };

        // Action from the HTML View    
        $scope.reset = function() {
            console.log("Entering reset...");
            $scope.errorMessage = ""
            $scope.user.userInfo = {
                "username": "",
                "password": "",
                "first_name": "",
                "last_name": "",
                "email": ""
            }
            $window.document.getElementById('inputUsername').focus();
        };

    };

    // Register the Controller with the app
    app.controller('CreateAccountController', CreateAccountController);

})();