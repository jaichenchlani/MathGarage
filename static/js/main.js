(function() {
    var app = angular.module('homePage', []);

    // Actions when HTTP call is completed successfully.
    var MainController = function($scope, $http, $window, $location) {
        console.log("Entering MainController...");
        $scope.username = sessionStorage.getItem('username')

        // Actions when HTTP call is completed successfully.
        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.dashboard = response.data;
            console.log($scope.dashboard);
            console.log($scope.showDashboard)
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
            $scope.userMessage = "Thank you for being a Math Mechanic. Here's your Dashboard."
            $scope.showDashboard = true
        } else {
            $scope.userMessage = "Hi there Math Mechanic! Please login to see your dashboard."
            $scope.showDashboard = false
        }
    };

    // Register the Controller with the app
    app.controller('MainController', MainController);

})();