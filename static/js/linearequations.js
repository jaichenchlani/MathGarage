(function() {
    // var app = angular.module('linearEquations', []);
    var app = angular.module('mathgarage', []);

    var LinearEquationsController = function($scope, $http, $window, $interval, $routeParams, $route) {
        console.log("Entering LinearEquationsController...");

        // Actions when HTTP call is completed successfully.
        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.puzzle = response.data;
            console.log($scope.puzzle);
            if (!$scope.puzzle.validOutputReturned) {
                $scope.errorMessage = $scope.puzzle.message;
                $window.document.getElementById('checkboxEasy').focus();
            } else {
                $window.document.getElementById('getEquations').focus();
            }
        }

        var onSubmitComplete = function(response) {
            console.log("Entering onSubmitComplete...");
            $scope.submit_status = response.data;
            console.log($scope.submit_status);
            // Set the focus on the Submit Answer button.

            $scope.showSystemAnswer = true
            $window.document.getElementById('getEquations').focus();
        }

        // Actions when HTTP call fails.
        var onError = function(reason) {
            console.log("Entering onError...");
            console.error("Error Details:" + JSON.stringify(reason));
            $window.alert("Error fetching data from the server.");
        }

        var decrementCountdown = function() {
            $scope.countdown -= 1;
            $scope.countdownMessage = "Starting the default search in " + $scope.countdown + " secs."
            if ($scope.countdown < 1) {
                $scope.getEquations()        
            };
        };

        var countdownInterval = null
        var startCountdown = function() {
            countdownInterval = $interval(decrementCountdown, 1000, $scope.countdown);
        };

        // Action from the HTML View
        $scope.getEquations = function () {
            console.log("Entering getEquations...");
            // Re-initialize variables on every Generate Puzzle
            $scope.countdownMessage = undefined
            $scope.errorMessage = ""
            $scope.userAnswerFeedback = {
                "result": 0,
                "message": ""
            }
            $scope.showSystemAnswer = false
            $window.document.getElementById('getEquations').value = "Get New Equation";
            // console.log(puzzle);
            calledURL = "/linear-equations/get"
            console.log("Calling " + calledURL + "...")

            requestData = {
                "difficultyLevel": $scope.difficultyLevel,
                "variableCount": $scope.variableCount
            }

            $http.put(calledURL, requestData)
                .then(onUserComplete, onError);
        };

        // Action from the HTML View
        $scope.submitAnswer = function (showSystemAnswer) {
            // console.log($scope.puzzle.user_answers_list);
            // console.log($scope.puzzle.answers_list);
            userMessage = ""
            userResult = 1
            for (i = 0; i < $scope.puzzle.config.number_of_variables; i++ ) {
                try {
                    user_answer = Number($scope.puzzle.answer[i].user_answer);
                } catch(err) {
                    console.log(err)
                }
                system_answer = $scope.puzzle.answer[i].system_answer;
                if (user_answer === system_answer) {
                    userMessage += "Element # " + Number(i+1) + ": Correct.";
                    $scope.puzzle.answer[i].isUserAnswerCorrect = 1
                } else {
                    userMessage += "Element # " + Number(i+1) + ": Incorrect.";
                    userResult = 0
                }

            }

            // databaseUpdatedMessage = "Answers updated in Datastore."
            databaseUpdatedMessage = ""

            if (userResult) {
                $scope.userAnswerFeedback = {
                    "result": userResult,
                    "message": "Bravo. Correct Answer! " + databaseUpdatedMessage
                };
            } else {
                $scope.userAnswerFeedback = {
                    "result": userResult,
                    // "message": userMessage + " " + databaseUpdatedMessage
                    "message": "Sorry. Incorrect Answer! See System Answer below." + databaseUpdatedMessage
                };
            }

            $scope.showSystemAnswer = true
            $window.document.getElementById('getEquations').focus();

            // Update Backend Datastore with the user answers
            console.log($scope.puzzle);
            calledURL = "/linear-equations/submit"
            console.log("Calling " + calledURL + "...")
            // console.log($scope.puzzle)
            
            $http.put(calledURL, $scope.puzzle)
                .then(onSubmitComplete, onError);

            // If the user performs the operation ahead of the 5 sec timer, cancel the timer to avoid running 2 requests
            if (countdownInterval) {
                $interval.cancel(countdownInterval)
            }
        };

        $window.document.getElementById('getEquations').focus();
        $scope.errorMessage = ""
        $scope.userAnswerFeedback = {
            "result": 0,
            "message": ""
        }
        $scope.showSystemAnswer = false;
        $scope.difficultyLevel = {
            "supereasy": 0,
            "easy": 1,
            "medium": 0,
            "hard": 0,
            "superhard": 0
        };
        // console.log($scope.difficultyLevel)
        $scope.variableCount = {
            "one": 0,
            "two": 1,
            "three": 0,
            "four": 0,
            "five": 0,
            "six": 0,
            "seven": 0,
            "eight": 0,
            "nine": 0,
            "ten": 0
        };
        // console.log($scope.variableCount)
        $scope.userAnswerFeedback = {
            "result": 0,
            "message": ""
        }
        $scope.countdown = 5;
        $scope.countdownMessage = "Starting the default search in " + $scope.countdown + " secs."
        startCountdown();
    };

    // Register the Controller with the app
    app.controller('LinearEquationsController', LinearEquationsController);

})();