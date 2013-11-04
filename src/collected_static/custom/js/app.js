var App = angular.module('App', [], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[%');
    $interpolateProvider.endSymbol('%]');
})
.config(['$interpolateProvider', '$httpProvider', '$routeProvider', 
    function($interpolateProvider, $httpProvider, $routeProvider) {

        $interpolateProvider.startSymbol('[%');
        $interpolateProvider.endSymbol('%]');

        $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
    }])
.controller('MainCtrl', ['$scope', function ($scope) {

}])
.controller('RegLoginCtrl', ['$scope', '$http', '$location', function ($scope, $http, $location) {

    $scope.loading = false;

    $scope.submit = function(url) {

        if (url) {

            $scope.loading = true;

            $http.post(url, $.param($scope.user))
            .success(
                function(data, status, headers, config) {
                    $scope.loading = false;
                    if (data.success) {
                        if (data.next) {
                            window.location = data.next;
                        } else {
                            alert(data.message);
                        }
                    } else {
                        alert('bad');
                    }
                })
            .error(
                function(data, status, headers, config){
                    $scope.loading = false;
                });
        }
    }
}]);
