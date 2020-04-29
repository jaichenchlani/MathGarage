(function() {
    var app = angular.module('homePage', []);

    // Actions when HTTP call is completed successfully.
    var MainController = function($scope, $http, $window, $location, $rootScope) {
        console.log("Entering MainController...");
        $scope.testMessage = $scope.loginInfo
        console.log($rootScope)
    };

    // Register the Controller with the app
    app.controller('MainController', ['$scope', '$http', '$window', '$location', '$rootScope', MainController]);

})();