angular.module('expensesList', [], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
});

function ExpensesCtl($scope) {
  $scope.expenses = [
    {amount:'42'},
    {amount:'54.34'}];
}