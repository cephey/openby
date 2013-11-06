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
.controller('RegisterCtrl', ['$scope', '$http', '$location', function ($scope, $http, $location) {

    /* привязываем к кнопке регистрации лоудер */
    $scope.reg_btn = Ladda.create(document.querySelector('#reg_btn'));

    // начало ajax запроса
    $scope.ajax_start = function () {
        $scope.loading = true;
        $scope.reg_btn.start();
    };
    // конец ajax запроса
    $scope.ajax_finish = function () {
        $scope.loading = false;
        $scope.reg_btn.stop();
    };

    /* сабмит формы регистрации */
    $scope.submit = function(url) {

        /* если указан адрес для регистрации и форма не пустая */
        if (url && $scope.user) {
            /* показываю лоудер */
            $scope.ajax_start();

            $http.post(url, $.param($scope.user))
            .success(
                function(data, status, headers, config) {
                    if (data.success) {
                        $scope.message = data.message;
                        $scope.ajax_success = true;
                    } else {
                        console.log(data.errors);
                    }
                }
            ).error(
                function(data, status, headers, config){
                    $scope.message = 'Сервер временно не отвечает, попробуйте ещё раз чуть позже.';
                    $scope.ajax_error = true;
                }
            ).then(
                function() {
                    /* скрываю лоудер */
                    $scope.ajax_finish();
                }
            );
        }
    }
}])
.controller('RegLoginCtrl', ['$scope', '$http', '$location', function ($scope, $http, $location) {

    $scope.reg_btn = Ladda.create(document.querySelector('#action_btn')),
    $scope.loading = false,

    // начало ajax запроса
    $scope.ajax_start = function () {
        $scope.loading = true;
        $scope.reg_btn.start();
    };
    // конец ajax запроса
    $scope.ajax_finish = function () {
        $scope.loading = false;
        $scope.reg_btn.stop();
    };

    $scope.submit = function(url) {

        if (url) {
            $scope.ajax_start();

            $http.post(url, $.param($scope.user)).success(
                function(data, status, headers, config) {
                    if (data.success) {
                        if (data.next) {
                            window.location = data.next;
                        } else {
                            alert(data.message);
                        }
                    } else {
                        alert('bad');
                    }
                }).error(
                function(data, status, headers, config){
                    // TODO: show error
                }).then(
                function() {
                    $scope.ajax_finish();
                });
        }
    }
}]);
