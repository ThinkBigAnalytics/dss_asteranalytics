var app = angular.module('teradata.module', []);

app.controller('TeradataController', function($scope) {
    var updateChoices = function() {
        // the parameter to callPythonDo() is passed to the do() method as the payload
        // the return value of the do() method comes back as the data parameter of the fist function()
        $scope.callPythonDo({}).then(function(data) {
            // success
            $scope.choices = data.choices;
        }, function(data) {
            // failure
            $scope.choices = [];
        });
    };
    
    updateChoices();

    //$scope.$watch('function', updateChoices);
    $scope.items = updateChoices
    
    $scope.checkResult = {};
    $scope.check = function() {
        var hasAuthentication = function(config) {
            return config.function;
        };
        $scope.checkResult = {
            hasAuthentication : hasAuthentication($scope.config)
        };
    };
    $scope.check();
 
});
