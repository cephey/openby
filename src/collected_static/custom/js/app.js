var App = angular.module('App', ['ngRoute']);

App.config(['$interpolateProvider', '$httpProvider', '$routeProvider', 
    function ($interpolateProvider, $httpProvider, $routeProvider) {

        /* задаю маркеры шаблонизатора */
        $interpolateProvider.startSymbol('[%');
        $interpolateProvider.endSymbol('%]');

        /* заголовки POST запроса для AJAX */
        var csrf = document.querySelector('input[name=csrfmiddlewaretoken]');
        var content_type = 'application/x-www-form-urlencoded; charset=UTF-8';
        if (csrf) {
            $httpProvider.defaults.headers.post['X-CSRFToken'] = csrf.getAttribute('value');
            $httpProvider.defaults.headers.post['Content-Type'] = content_type;
        }
    }])
.controller('RegisterCtrl', ['$scope', '$http', function ($scope, $http) {

    $scope.form = {
        /* поля формы регистрации */
        fields: ['username', 'email', 'password1', 'password2'],

        ajax: {
            /* привязываем лоудер к кнопке регистрации */
            btn: Ladda.create(document.querySelector('#reg_btn')),

            /* начало ajax запроса */
            start: function () {
                /* делаю форму недоступной для редактирования */
                $scope.loading = true;
                this.btn.start();
                /* скрываю все прошлые ошибки */
                $scope.form.errors.hide();
            },
            /* конец ajax запроса */
            finish: function () {
                $scope.loading = false;
                this.btn.stop();
            }
        },
        errors: {
            show: function (errors) {
                /* Выводит ошибки которые пришли с сервера после сабмита */
                var self = this;
                _.each(errors, function (val, key) {
                    self[key] = val[0];
                });
            },
            hide: function () {
                /* очистка ошибок формы */
                var self = this;
                _.each($scope.form.fields, function (key) {
                    self[key] = false;
                });
                self['__all__'] = false;
            }
        }
    };

    /* сабмит формы регистрации */
    $scope.submit = function (url) {

        /* если указан адрес для регистрации и форма не пустая */
        if (url && $scope.user) {

            /* если форма не валидна она не сабмитится */
            // if ($scope.reg_form.$invalid) return false;

            /* показываю лоудер */
            $scope.form.ajax.start();

            var post_params = {};
            _.each($scope.form.fields, function (i) {
                post_params[i] = $('[name="' + i + '"]').val();
            });

            $http.post(
                url,
                $.param(post_params)
            ).success(function (data, status, headers, config) {
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
                    $scope.form.errors.show(data.errors);
                }
            }).error(function (data, status, headers, config) {
                $scope.message = 'Сервер временно не отвечает, попробуйте ещё раз чуть позже.';
                $scope.ajax_error = true;
            }).then(function () {
                /* скрываю лоудер */
                $scope.form.ajax.finish();
            });
        }
    };
}])
.controller('LoginCtrl', ['$scope', '$http', function ($scope, $http) {

    $scope.form = {
        /* поля формы регистрации */
        fields: ['username', 'password'],

        ajax: {
            /* привязываем лоудер к кнопке регистрации */
            btn: Ladda.create(document.querySelector('#login_btn')),

            /* начало ajax запроса */
            start: function () {
                /* делаю форму недоступной для редактирования */
                $scope.loading = true;
                this.btn.start();
                /* скрываю все прошлые ошибки */
                $scope.form.errors.hide();
            },
            /* конец ajax запроса */
            finish: function () {
                $scope.loading = false;
                this.btn.stop();
            }
        },
        errors: {
            show: function (errors) {
                /* Выводит ошибки которые пришли с сервера после сабмита */
                var self = this;
                _.each(errors, function (val, key) {
                    self[key] = val[0];
                });
            },
            hide: function () {
                /* очистка ошибок формы */
                var self = this;
                _.each($scope.form.fields, function (key) {
                    self[key] = false;
                });
                self['__all__'] = false;
            }
        }
    };

    /* сабмит формы регистрации */
    $scope.submit = function (url) {

        /* если указан адрес для регистрации и форма не пустая */
        if (url && $scope.user) {

            /* если форма не валидна она не сабмитится */
            if ($scope.login_form.$invalid) return false;

            /* показываю лоудер */
            $scope.form.ajax.start();

            var post_params = {};
            _.each($scope.form.fields, function (i) {
                post_params[i] = $('[name="' + i + '"]').val();
            });

            $http.post(
                url,
                $.param(post_params)
            ).success(function (data, status, headers, config) {
                if (data.success) {
                    /* если все хорошо, редирект на страницу профиля */
                    window.location.href = data.next;
                } else {
                    /* если сервер вернул ошибки формы, то отображаю их */
                    $scope.form.errors.show(data.errors);
                }
            }).error(function (data, status, headers, config) {
                $scope.message = 'Сервер временно не отвечает, попробуйте ещё раз чуть позже.';
                $scope.ajax_error = true;
            }).then(function () {
                /* скрываю лоудер */
                $scope.form.ajax.finish();
            });
        }
    };
}])
.directive('serverError', function () {
    /* фейковый валидатор. Ничего не проверяет. Использую его только
     для вывода ошибок приходящих с сервера после сабмита */
    return {
        require:'ngModel',
        link: function (scope, elem, attrs, ctrl) {

            /* слежу за появлением ошибки в объекте form_errors
             относящейся к конкретному полю.
              Если оно не пустое выставляю валидатор в false */
            scope.$watch('form.errors.' + attrs.name, function (newVal, oldVal) {

                if (newVal) {
                    ctrl.$setValidity('servererror', false);
                    return undefined;
                } else {
                    ctrl.$setValidity('servererror', true);
                    return newVal;
                }
            });

            /* сам по себе валидатор ничего не проверяет,
             и всегда возвращает true (все OK) */
            ctrl.$parsers.unshift(function (viewValue) {

                ctrl.$setValidity('servererror', true);
                return viewValue;
            });
        }
    };
})
.directive('equalPassword', function () {
    /* валидатор для проверки равенства двух полей для ввода пароля */
    return {
        require:'ngModel',
        link: function (scope, elem, attrs, ctrl) {

            /* поля для повтора ввода пароля следит за изменением первого поля пароля,
             и если оно меняется, запускаю валидатор заново */
            scope.$watch('user.password1', function (newVal, oldVal) {

                if (scope.user && newVal === scope.user.password2) {
                    ctrl.$setValidity('equalpassword', true);
                    return scope.user.password2;
                } else {
                    ctrl.$setValidity('equalpassword', false);
                    return undefined;
                }
            });

            ctrl.$parsers.unshift(function (viewValue) {

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