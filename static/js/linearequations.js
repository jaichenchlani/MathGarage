(function() {
    var app = angular.module('linearEquations', []);

    var LinearEquationsController = function($scope, $http, $window, $interval) {
        console.log("Entering LinearEquationsController...");
        $scope.username = sessionStorage.getItem('username')
        $scope.showTimer = false

        // Actions when HTTP call is completed successfully.
        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.puzzle = response.data;
            console.log($scope.puzzle);
            $window.document.getElementById('getEquations').value = "Get New Equation";
            if (!$scope.puzzle.validOutputReturned) {
                $scope.errorMessage = $scope.puzzle.message;
                $window.document.getElementById('checkboxEasy').focus();
            } else {
                $window.document.getElementById('submitAnswer').focus();
                // Start Timer
                $scope.timer = 0
                $scope.showTimer = true
                startTimer();
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

        var startCountdown = function() {
            $interval(decrementCountdown, 1000, $scope.countdown);
        };

        var startTimer = function() {
            $interval(incrementTimer, 1, $scope.timer);
        };
        var stopTimer = function() {
            console.log("Entering stopTimer...")
            $scope.timer = 0
            $scope.timerSec = 0
            $interval.cancel(startTimer())
        };
        var incrementTimer = function() {
            $scope.timer += 1;
            $scope.timerSec = $scope.timer / 1000;
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
            // console.log(puzzle);
            calledURL = "/linear-equations/get"
            console.log("Calling " + calledURL + "...")

            requestData = {
                "username": $scope.username,
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
            $scope.showTimer = false
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
            timeTakenMessage = "Time Taken(Secs): "
            $scope.puzzle.timeTaken = $scope.timerSec
            if (userResult) {
                $scope.userAnswerFeedback = {
                    "result": userResult,
                    "message": "Bravo. Correct Answer! " + timeTakenMessage
                };
                $scope.puzzle.userAnswerCorrect = true
            } else {
                $scope.userAnswerFeedback = {
                    "result": userResult,
                    "message": "Sorry. Incorrect Answer! See System Answer below." + timeTakenMessage
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
        // $scope.countdown = 5;
        // $scope.countdownMessage = "Starting the default search in " + $scope.countdown + " secs."
        // startCountdown();
    };

    // Register the Controller with the app
    app.controller('LinearEquationsController', LinearEquationsController);

})();