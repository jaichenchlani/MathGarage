(function() {
    var app = angular.module('sequencePuzzles', []);

    var SequencePuzzlesController = function($scope, $http, $window, $interval) {
        console.log("Entering SequencePuzzlesController...");
        
        // Actions when HTTP call is completed successfully.
        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.puzzle = response.data;
            // $scope.userAnswer = $scope.puzzle.question;
            console.log($scope.puzzle);
            if (!$scope.puzzle.validOutputReturned) {
                $scope.errorMessage = $scope.puzzle.message;
                $window.document.getElementById('checkboxEasy').focus();
            } else {
                $window.document.getElementById('getPuzzle').focus();
            }
        }

        var onSubmitComplete = function(response) {
            console.log("Entering onSubmitComplete...");
            $scope.submit_status = response.data;
            console.log($scope.submit_status);
            // Set the focus on the Submit Answer button.

            $scope.showSystemAnswer = true
            $window.document.getElementById('getPuzzle').focus();
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
                $scope.getPuzzle()        
            };
        };

        var startCountdown = function() {
            $interval(decrementCountdown, 1000, $scope.countdown);
        };

        // Action from the HTML View
        $scope.getPuzzle = function () {
            console.log("Entering getPuzzle...");
            // Re-initialize variables on every Generate Puzzle
            $scope.countdownMessage = undefined
            $scope.errorMessage = ""
            $scope.userAnswerFeedback = {
                "result": 0,
                "message": ""
            }
            $scope.showSystemAnswer = false
            $window.document.getElementById('getPuzzle').value = "Get New Puzzle";
            // console.log(puzzle);
            // $window.document.getElementById('user-answer').focus();
            calledURL = "/sequence-puzzles/get"
            console.log("Calling " + calledURL + "...")
            
            // console.log($scope.difficultyLevel);

            $http.put(calledURL, $scope.difficultyLevel)
                .then(onUserComplete, onError);
        };

        // Action from the HTML View
        $scope.submitAnswer = function () {
            console.log("Entering checkAnswer...");
            // console.log($scope.puzzle.missing_elements_list_question);
            // console.log($scope.puzzle.missing_elements_list_answer);
            userMessage = ""
            userResult = 1
            for (i = 0; i < $scope.puzzle.config.missing_elements_count; i++ ) {
                // console.log(i)
                // console.log($scope.puzzle.missing_elements[i])
                try {
                    user_answer = Number($scope.puzzle.missing_elements[i].user_answer);
                } catch(err) {
                    console.log(err)
                }
                system_answer = $scope.puzzle.missing_elements[i].system_answer;
                // console.log(question);
                // console.log(answer);
                if (user_answer === system_answer) {
                    userMessage += "Element # " + Number(i+1) + ": Correct.";
                    $scope.puzzle.missing_elements[i].isUserAnswerCorrect = 1
                } else {
                    userMessage += "Element # " + Number(i+1) + ": Incorrect.";
                    userResult = 0
                }
            }

            // messageAddendum = "Answers updated in Datastore. Check rationale below."
            messageAddendum = ""

            if (userResult) {
                $scope.userAnswerFeedback = {
                    "result": userResult,
                    "message": "Bravo. Correct Answer! " + messageAddendum
                };
            } else {
                $scope.userAnswerFeedback = {
                    "result": userResult,
                    "message": "Sorry. Incorrect Answer! See Rationale below." + messageAddendum
                };
            }

            $scope.showSystemAnswer = true
            $window.document.getElementById('getPuzzle').focus();

            // Update Backend Datastore with the user answers
            calledURL = "/sequence-puzzles/submit"
            console.log("Calling " + calledURL + "...")
            console.log($scope.puzzle)
            
            $http.put(calledURL, $scope.puzzle)
                .then(onSubmitComplete, onError);

        };

        $window.document.getElementById('getPuzzle').focus();
        $scope.errorMessage = ""
        $scope.userAnswerFeedback = {
            "result": 0,
            "message": ""
        }
        $scope.showSystemAnswer = false;
        $scope.difficultyLevel = {
            "easy": 0,
            "medium": 1,
            "hard": 0
        };
        // console.log($scope.difficultyLevel)
        $scope.userAnswerFeedback = {
            "result": 0,
            "message": ""
        }
        $scope.countdown = 5;
        $scope.countdownMessage = "Starting the default search in " + $scope.countdown + " secs."
        startCountdown();
    };

    // Register the Controller with the app
    app.controller('SequencePuzzlesController', SequencePuzzlesController);

})();