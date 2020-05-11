(function() {
    var app = angular.module('homePage', []);

    // Actions when HTTP call is completed successfully.
    var MainController = function($scope, $http, $window, $location) {
        console.log("Entering MainController...");
        $scope.username = sessionStorage.getItem('username')
        console.log($scope.username)
        $scope.logout = function() {
            // Clear the user info from session storage
            console.log("Entering logout...");
            sessionStorage.setItem('username',"")
            $window.location.href = '/';
        }
    };

    // Register the Controller with the app
    app.controller('MainController', ['$scope', '$http', '$window', '$location', '$rootScope', MainController]);

})();