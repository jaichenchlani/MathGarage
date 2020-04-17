(function() {
    var app = angular.module('googleSignIn', []);

    // Actions when HTTP call is completed successfully.
    var GoogleSignInController = function($scope, $http, $window, $location) {
        console.log("Entering GoogleSignInController...");
        console.log($scope.userProfile)

        $scope.onSignIn = function (googleUser) {
            console.log("Entering controller onSignIn...");
            console.log(googleUser)
            var profile = googleUser.getBasicProfile();
            console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
            console.log('Name: ' + profile.getName());
            console.log('Image URL: ' + profile.getImageUrl());
            console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
        };

        $scope.signOut = function() {
            console.log("Entering controller signOut...");
            var auth2 = gapi.auth2.getAuthInstance();
            auth2.signOut().then(function () {
              console.log('User signed out.');
            });
        };

    };


    // Register the Controller with the app
    app.controller('GoogleSignInController', ['$scope', '$http', '$window', '$location', GoogleSignInController]);

})();

function onSignIn(googleUser) {
    console.log("Entering C non-controller onSignIn...");
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

    console.log("Calling Utils function...");
    storeSignInInfo(googleUser);
    storeSignInInfo(profile)
  }

function signOut() {
  console.log("Entering D non-controller signOut...")  
  var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });
  }

