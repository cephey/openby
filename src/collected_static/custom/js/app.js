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
.controller('RegisterCtrl', ['$scope', '$http', function ($scope, $http) {

    /* привязываем лоудер к кнопке регистрации */
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

            $http.post(
                url,
                $.param($scope.user)
            ).success(function(data, status, headers, config) {
                if (data.success) {
                    $scope.message = data.message;
                    $scope.ajax_success = true;
                } else {
                    console.log(data.errors);
                }
            }).error(function(data, status, headers, config){
                $scope.message = 'Сервер временно не отвечает, попробуйте ещё раз чуть позже.';
                $scope.ajax_error = true;
            }).then(function() {
                /* скрываю лоудер */
                $scope.ajax_finish();
            });
        }
    };
}])
.controller('LoginCtrl', ['$scope', '$http', function ($scope, $http) {

    /* привязываем лоудер к кнопке аутентификации */
    $scope.reg_btn = Ladda.create(document.querySelector('#login_btn'));

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

        /* если указан адрес для аутентификации и форма не пустая */
        if (url && $scope.user) {
            /* показываю лоудер */
            $scope.ajax_start();

            $http.post(
                url,
                $.param($scope.user)
            ).success(function(data, status, headers, config) {
                if (data.success) {
                    $scope.message = data.message;
                    $scope.ajax_success = true;
                } else {
                    console.log(data.errors);
                }
            }).error(function(data, status, headers, config){
                $scope.message = 'Сервер временно не отвечает, попробуйте ещё раз чуть позже.';
                $scope.ajax_error = true;
            }).then(function() {
                /* скрываю лоудер */
                $scope.ajax_finish();
            });
        }
    };
}])
.directive('equalPassword', function () {
    return {
        require:'ngModel',
        link: function (scope, elem, attrs, ctrl) {

            /* поля для повтора ввода пароля следит за изменением первого поля пароля,
             и если оно меняется, запускаю валидатор заново */
            scope.$watch('user.password1', function(newVal, oldVal) {

                if (scope.user && newVal === scope.user.password2) {
                    ctrl.$setValidity('equalpassword', true);
                    return scope.user.password2;
                } else {
                    ctrl.$setValidity('equalpassword', false);
                    return undefined;
                }
            });

            ctrl.$parsers.unshift(function(viewValue) {

                /* перед валидацией проверяю что форма не пустая
                 и первое поле ввода пароля валидное */
                if (scope.user && scope.user.password1 !== undefined) {

                    /* если пользователь очистил поле,
                     присваиваю ему undefined */
                    if (viewValue == "") {
                        viewValue = undefined;
                    }

                    if (scope.user.password1 === viewValue) {
                        ctrl.$setValidity('equalpassword', true);
                        return viewValue;
                    } else {
                        ctrl.$setValidity('equalpassword', false);
                        return undefined;
                    }
                } else {
                    ctrl.$setValidity('equalpassword', true);
                    return viewValue;
                }

            });
        }
    };
});