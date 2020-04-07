(function() {
    var app = angular.module('linearEquations', []);

    var LinearEquationsController = function($scope, $http, $window) {
        console.log("Entering LinearEquationsController...");
        $window.document.getElementById('getPuzzle').focus();
        $scope.errorMessage = ""
        $scope.userAnswerFeedback = {
            "result": 0,
            "message": ""
        }
        $scope.showSystemAnswer = false;
        $scope.difficultyLevel = {
            "supereasy": 1,
            "easy": 1,
            "medium": 0,
            "hard": 0,
            "superhard": 0
        };
        // console.log($scope.difficultyLevel)
        $scope.userAnswerFeedback = {
            "result": 0,
            "message": ""
        }

        // Actions when HTTP call is completed successfully.
        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.puzzle = response.data;
            console.log($scope.puzzle);
            if (!$scope.puzzle.validOutputReturned) {
                $scope.errorMessage = $scope.puzzle.message;
                $window.document.getElementById('checkboxEasy').focus();
            } else {
                $window.document.getElementById('getPuzzle').focus();
            }
        }

        // Actions when HTTP call fails.
        var onError = function(reason) {
            console.log("Entering onError...");
            console.error("Error Details:" + JSON.stringify(reason));
            $window.alert("Error fetching data from the server.");
        }

        // Action from the HTML View
        $scope.getPuzzle = function (puzzle, errorMessage) {
            console.log("Entering getPuzzle...");
            // Re-initialize variables on every Generate Puzzle
            $scope.errorMessage = ""
            $scope.showSystemAnswer = false
            $window.document.getElementById('getPuzzle').value = "Get New Puzzle";
            // console.log(puzzle);
            calledURL = "/linear-equations/get"
            console.log("Calling " + calledURL + "...")

            $http.put(calledURL, $scope.difficultyLevel)
                .then(onUserComplete, onError);
        };

        // Action from the HTML View
        $scope.checkAnswer = function (showSystemAnswer) {
            // console.log($scope.puzzle.user_answers_list);
            // console.log($scope.puzzle.answers_list);
            userMessage = ""
            userResult = 1
            for (i = 0; i < $scope.puzzle.config.number_of_variables; i++ ) {
                try {
                    question = Number($scope.puzzle.answer[i].user_answer);
                } catch(err) {
                    console.log(err)
                }
                answer = $scope.puzzle.answer[i].system_answer;
                // console.log(question);
                // console.log(answer);
                if (question === answer) {
                    userMessage += "Element # " + Number(i+1) + ": Correct.";
                    $scope.puzzle.answer[i].isUserAnswerCorrect = 1
                } else {
                    userMessage += "Element # " + Number(i+1) + ": Incorrect.";
                    userResult = 0
                }

            }

            if (userResult) {
                $scope.userAnswerFeedback = {
                    "result": userResult,
                    "message": "Bravo. Correct Answer!"
                };
            } else {
                $scope.userAnswerFeedback = {
                    "result": userResult,
                    "message": userMessage
                };
            }

            $scope.showSystemAnswer = true
            $window.document.getElementById('getPuzzle').focus();
        };

        // Call the function on page load.
        $scope.getPuzzle($scope.puzzle, $scope.errorMessage);
    };

    // Register the Controller with the app
    app.controller('LinearEquationsController', ['$scope', '$http', '$window', LinearEquationsController]);

})();