(function() {
    // var app = angular.module('homePage', []);
    var app = angular.module('mathgarage');

    // Actions when HTTP call is completed successfully.
    var MainController = function($scope, $http, $window, $interval, $routeParams, $route, $rootScope) {
        console.log("Entering MainController...");
        $scope.testMessage = $scope.loginInfo
        console.log($rootScope)
    };

    // Register the Controller with the app
    app.controller('MainController', MainController);

})();