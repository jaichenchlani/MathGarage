(function() {
    // var app = angular.module('basicArithematicOperations', []);
    var app = angular.module('mathgarage', []);

    // Actions when HTTP call is completed successfully.
    var BasicArithematicOperationsController = function($scope, $http, $window, $location, $interval) {
        console.log("Entering BasicArithematicOperationsController...");

        var onUserComplete = function(response) {
            console.log("Entering onUserComplete...");
            $scope.operation = response.data;
            console.log($scope.operation);
            // Set the focus on the Submit Answer button.
            $scope.showResultSection = true
            $scope.gotoResultSection();
            $window.document.getElementById('submitAnswer').focus();
        }

        var onSubmitComplete = function(response) {
            console.log("Entering onSubmitComplete...");
            $scope.submit_status = response.data;
            console.log($scope.submit_status);
            // Set the focus on the Submit Answer button.

            $scope.showSystemAnswer = true
            $window.document.getElementById('getBasicArithematicOperations').focus();
        }

        // Actions when HTTP call fails.
        var onError = function(reason) {
            console.log("Entering onError...");
            console.error("Error Details:" + JSON.stringify(reason));
            $window.alert("Error fetching data from the server.");
        }

        var decrementCountdown = function() {
            console.log("Entering decrementCountdown...");
            $scope.countdown -= 1;
            $scope.countdownMessage = "Starting the default search in " + $scope.countdown + " secs."
            if ($scope.countdown < 1) {
                $scope.getBasicArithematicOperations()        
            };
        };

        var countdownInterval = null
        var startCountdown = function() {
            console.log("Entering startCountdown...");
            countdownInterval = $interval(decrementCountdown, 1000, $scope.countdown);
        };

        // Action from the HTML View
        $scope.getBasicArithematicOperations = function () {
            console.log("Entering getBasicArithematicOperations...");
            $scope.countdownMessage = undefined;
            $scope.errorMessage = "";
            $scope.showSystemAnswer = false

            requestData = {
                "difficultyLevel": $scope.difficultyLevel,
                "operator": $scope.operator,
                "number_of_questions": $scope.number_of_questions
            }
            
            calledURL = "/basic-arithematic-operations"
            console.log("Calling " + calledURL + "...")
            console.log(requestData)
            
            $http.put(calledURL, requestData)
                .then(onUserComplete, onError);
        };

        // Action from the HTML View
        $scope.submitAnswer = function (showSystemAnswer) {
            console.log($scope.operation);
            userMessage = ""
            userResult = 1
            countCorrectAnswers = 0
            totalQuestions = $scope.operation.number_of_questions

            // If the user performs the operation ahead of the 5 sec timer, cancel the timer to avoid running 2 requests
            if (countdownInterval) {
                $interval.cancel(countdownInterval)
            }

            for (i = 0; i < totalQuestions; i++ ) {
                try {
                    userAnswer = Number($scope.operation.questions[i].user_answer);
                } catch(err) {
                    console.log(err)
                }
                answer = $scope.operation.questions[i].answer;
                // console.log(userAnswer);
                // console.log(answer);
                if (userAnswer === answer) {
                    $scope.operation.questions[i].is_user_answer_correct = 1
                    countCorrectAnswers += 1
                } else {
                    userResult = 0
                }

            }

            if (userResult) {
                $scope.userAnswerFeedback = {
                    "result": userResult,
                    "message": "Bravo! All " + countCorrectAnswers + " of " + totalQuestions + " answers are correct."
                };
            } else {
                $scope.userAnswerFeedback = {
                    "result": userResult,
                    "message": countCorrectAnswers + " of " + totalQuestions + " answers are correct."
                };
            }

            $scope.showSystemAnswer = true
            $window.document.getElementById('getBasicArithematicOperations').focus();

            // Update Backend Datastore with the user answers
            console.log($scope.operation);
            calledURL = "/basic-arithematic-operations/submit"
            console.log("Calling " + calledURL + "...")
            // console.log($scope.operation)
            
            $http.put(calledURL, $scope.operation)
                .then(onSubmitComplete, onError);

        };

        $scope.reset = function() {
            $scope.operation = {}
            $window.document.getElementById('getBasicArithematicOperations').focus();
            $scope.errorMessage = ""
            $scope.showSystemAnswer = false
            $scope.showResultSection = false
            $scope.countdownMessage = undefined;
            $scope.operation_request = {
                "operator": "+",
                "number_of_questions": 8
            };
            $scope.difficultyLevel = {
                "supereasy": 0,
                "easy": 1,
                "medium": 0,
                "hard": 0,
                "superhard": 0
            };
            $scope.userAnswerFeedback = {
                "result": 1,
                "message": ""
            };
        };

        $scope.gotoResultSection = function() {
            console.log("Entering gotoResultSection...");
            var newHash = 'resultsection';
            // console.log($location.hash());
            // console.log(newHash);
            if ($location.hash() !== newHash) {
                console.log($location.hash());
                console.log(newHash);
                // set the $location.hash to `newHash` and
                // $anchorScroll will automatically scroll to it
                $location.hash(newHash);
            }
        };

        $window.document.getElementById('getBasicArithematicOperations').focus();
        $scope.errorMessage = ""
        $scope.showSystemAnswer = false
        $scope.showResultSection = false
        $scope.operator = "+";
        $scope.number_of_questions = "8";
        $scope.difficultyLevel = {
            "supereasy": 0,
            "easy": 1,
            "medium": 0,
            "hard": 0,
            "superhard": 0
        };

        $scope.userAnswerFeedback = {
            "result": 1,
            "message": ""
        };
        $scope.countdown = 5;
        $scope.countdownMessage = "Starting the default search in " + $scope.countdown + " secs."
        startCountdown();
    };

    // Register the Controller with the app
    app.controller('BasicArithematicOperationsController', BasicArithematicOperationsController);

})();