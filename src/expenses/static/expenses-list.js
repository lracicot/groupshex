angular.module('expensesList', [], function ($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');

    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
    $httpProvider.defaults.transformRequest = function(data) {
        return $.param(data);
    }
});

function ExpensesCtl($scope, $http) {

    $scope.expenses = [{amount: ''}];
    $http.get("/expenses/get/1", {headers: {"X-CSRFToken": csrftoken}, data:{}}).success(function(data) {
        $scope.expenses = data;
    });

    $scope.addExpense = function() {
        expense = {group_id:$('#group_id').val(), amount:$scope.amountText, title:$scope.titleText};

        $http.post('/expenses/add', expense, {headers:{"X-CSRFToken": csrftoken}}).success(function(data) {
            data.amount = parseFloat(Math.round(data.amount * 100) / 100).toFixed(2);
            $scope.expenses.push(data);
            //$scope.productText = '';

            //$('#inv_product').focus();
        });
    };
}