(function() {
  
    var app = angular.module("mathgarage", ["ngRoute"]);
   console.log("From App.js....");
    
    app.config(function($routeProvider) {
      $routeProvider
    //  Home Page Form  
      .when("/", {
          templateUrl: "../templates/main.html",
          controller: "MainController"
        })
    //  Multiplication Facts Form  
    .when("/multiplication-facts", {
        templateUrl: "multiplication-facts.html",
        controller: "MultiplicationFactsController"
      })
    //    Sequence Puzzles Form  
      .when("/sequence-puzzles", {
          templateUrl: "sequence-puzzles.html",
          controller: "SequencePuzzlesController"
        })
    //    Number Wiki Form  
    .when("/number-wiki", {
        templateUrl: "number-wiki.html",
        controller: "NumberWikiController"
      })
    //    Login Form  
    .when("/login-initial-load", {
        templateUrl: "login.html",
        controller: "LoginController"
      })
    //    Linear Equations Form  
    .when("/linear-equations", {
        templateUrl: "linear-equations.html",
        controller: "LinearEquationsController"
      })
    //    Basic Arithematic Operations Search Form  
    .when("/basic-arithematic-operations-initial-load", {
        templateUrl: "basic-arithematic-operations.html",
        controller: "BasicArithematicOperationsController"
      })
        .otherwise({redirectTo:"/"});
    });
    
  }());