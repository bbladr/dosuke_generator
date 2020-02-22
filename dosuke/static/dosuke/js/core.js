var djangoEvent= angular.module('djangoEvent', []);

function mainController($scope, $http) {

    $scope.readEvents = function() {
        $http.get('/api/Events/')
            .success(function(data) {
                $scope.formData = {};
                $scope.events = data;
                console.log(data);
            })
            .error(function(data) {
                console.log('Error: ' + data);
            });
    };

    $scope.createEvent = function() {
        $http.post('/api/Events/', $scope.formData)
            .success(function(data) {
                console.log(data);
                $scope.readEvents();
            })
            .error(function(data) {
                console.log('Error: ' + data);
            });
    };

    $scope.deleteEvent = function(id) {
        $http.delete('/api/Events/' + id + '/')
            .success(function(data) {
                console.log(data);
                $scope.readEvents();
            })
            .error(function(data) {
                console.log('Error: ' + data);
            });
    };

    $scope.readEvents();

}