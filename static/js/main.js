(function() {
    var app = angular.module('homePage', []);

    // Actions when HTTP call is completed successfully.
    var MainController = function($scope, $http, $window, $location) {
        console.log("Entering MainController...");
        $scope.username = sessionStorage.getItem('username')
        console.log($scope.username)

        // Actions when HTTP call is completed successfully.
        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.dashboard = response.data;
            console.log($scope.dashboard);
        }

        // Actions when HTTP call fails.
        var onError = function(reason) {
            console.log("Entering onError...");
            console.error("Error Details:" + JSON.stringify(reason));
            $window.alert("Error fetching data from the server.");
        }

        $scope.logout = function() {
            // Clear the user info from session storage
            console.log("Entering logout...");
            sessionStorage.setItem('username',"")
            $window.location.href = '/';
        };

        $scope.getDashboard = function() {
            calledURL = "/get-dashboard"
            console.log("Calling " + calledURL + "...")
            requestData = {
                "username": $scope.username
            }
            console.log(requestData)
            $http.put(calledURL, requestData)
                .then(onUserComplete, onError);
        };

        if ($scope.username) {
            $scope.getDashboard()
        }
    };

    // Register the Controller with the app
    app.controller('MainController', MainController);

})();