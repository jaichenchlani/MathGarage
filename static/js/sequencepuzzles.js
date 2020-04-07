(function() {
    var app = angular.module('sequencePuzzles', []);

    var SequencePuzzlesController = function($scope, $http, $window) {
        console.log("Entering SequencePuzzlesController...");
        $window.document.getElementById('getPuzzle').focus();
        $scope.errorMessage = ""
        $scope.userAnswerFeedback = {
            "result": 0,
            "message": ""
        }
        $scope.showSystemAnswer = false;
        $scope.difficultyLevel = {
            "easy": 1,
            "medium": 1,
            "hard": 1
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
            $scope.userAnswer = $scope.puzzle.question;
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
            // $window.document.getElementById('user-answer').focus();
            calledURL = "/sequence-puzzles/get"
            console.log("Calling " + calledURL + "...")
            
            // console.log($scope.difficultyLevel);

            $http.put(calledURL, $scope.difficultyLevel)
                .then(onUserComplete, onError);
        };

        // Action from the HTML View
        $scope.checkAnswer = function (showSystemAnswer) {
            console.log("Entering checkAnswer...");
            // console.log($scope.puzzle.missing_elements_list_question);
            // console.log($scope.puzzle.missing_elements_list_answer);
            userMessage = ""
            userResult = 1
            for (i = 0; i < $scope.puzzle.config.missing_elements_count; i++ ) {
                // console.log(i)
                try {
                    question = Number($scope.puzzle.missing_elements[i].question);
                } catch(err) {
                    console.log(err)
                }
                answer = $scope.puzzle.missing_elements[i].answer;
                // console.log(question);
                // console.log(answer);
                if (question === answer) {
                    userMessage += "Element # " + Number(i+1) + ": Correct.";
                    $scope.puzzle.missing_elements[i].isUserAnswerCorrect = 1
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
    app.controller('SequencePuzzlesController', ['$scope', '$http', '$window', SequencePuzzlesController]);

})();