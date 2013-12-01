var App = angular.module('App', ['ngRoute'], function ($interpolateProvider) {
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
    $scope.btn = Ladda.create(document.querySelector('#reg_btn'));

    // начало ajax запроса
    $scope.ajax_start = function () {
        $scope.loading = true;
        $scope.btn.start();
    };
    // конец ajax запроса
    $scope.ajax_finish = function () {
        $scope.loading = false;
        $scope.btn.stop();
    };

    /* сабмит формы регистрации */
    $scope.submit = function(url) {

        /* если указан адрес для регистрации и форма не пустая */
        if (url && $scope.user) {

            /* если форма не валидна она не сабмитится */
            // if ($scope.reg_form.$invalid) return false;

            $scope.form_errors.hide();
            /* показываю лоудер */
            $scope.ajax_start();

            var post_params = {};
            _.each($scope.fields, function(i){ post_params[i] = $('[name="' + i + '"]').val(); });

            console.log(post_params);

            $http.post(
                url,
                $.param(post_params)
            ).success(function(data, status, headers, config) {
                if (data.success) {
                    if (data._type === 'email') {
                        /* если включена активация через почту,
                         то просим пользователя активировать аккаунт */
                        $scope.message = data.message;
                        $scope.ajax_success = true;
                    } else {
                        /* иначе просто редиректим на страницу профиля */
                        window.location.href = data.next;
                    }
                } else {
                    // если сервер вернул ошибки формы, то отображаю их
                    $scope.form_errors.show(data.errors);
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

    $scope.fields = ['username', 'email', 'password1', 'password2'];

    // _.each($scope.fields, function(elem){
    //     $scope.$watch('user.' + elem, function(newVal, oldVal) {
    //         delete $scope['for_' + elem].$error.server;
    //     });
    // });

    /* объект для хранения ошибок формы */
    $scope.form_errors = {
        show: function(errors) {
            /* Выводит ошибки которые пришли с сервера после сабмита */
            // _.each(errors, function(val, key){ self[key] = val; });
            var self = this;
            _.each(errors, function(val, key){
                // $scope.$apply(
                //     $scope['for_' + key].$error.server = val
                // );
                // $scope['for_' + key].$invalid = true;
                $scope['for_' + key].$error.server = val;
            });
        },
        hide: function() {
            /* очистка ошибок формы */
            var self = this;
            _.each($scope.fields, function(elem){
                self[elem] = false;
            });
            self['__all__'] = false;
        }
    };
}])
.controller('LoginCtrl', ['$scope', '$http', function ($scope, $http) {

    /* привязываем лоудер к кнопке аутентификации */
    $scope.btn = Ladda.create(document.querySelector('#login_btn'));

    // начало ajax запроса
    $scope.ajax_start = function () {
        $scope.loading = true;
        $scope.btn.start();
    };
    // конец ajax запроса
    $scope.ajax_finish = function () {
        $scope.loading = false;
        $scope.btn.stop();
    };

    /* сабмит формы регистрации */
    $scope.submit = function(url) {

        /* если указан адрес для аутентификации и форма не пустая */
        if (url && $scope.user) {

            /* если форма не валидна она не сабмитится */
            if ($scope.login_form.$invalid) return false;

            /* показываю лоудер */
            $scope.ajax_start();

            $http.post(
                url,
                $.param($scope.user)
            ).success(function(data, status, headers, config) {
                if (data.success) {
                    /* если все хорошо, редирект на страницу профиля */
                    window.location.href = data.next;
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
.directive('server', function () {
    return {
        require:'ngModel',
        link: function (scope, elem, attrs, ctrl) {

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
})
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