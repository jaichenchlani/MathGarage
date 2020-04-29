(function() {

    var mathgarageServices = function($http){
        console.log("Entering mathgarage service...")

        var generateMultiplicationFacts = function(calledURL) {
            console.log("Entering mathgarage.generateMultiplicationFacts...")
            $http.get(calledURL)
                .then(function(response){
                    return(response.data)
                });
        };
        return {
            generateMultiplicationFacts: generateMultiplicationFacts
        };

    };

    var module = angular.module("mathgarage",[]);
    module.factory("mathgarageServices", mathgarageServices);
})();