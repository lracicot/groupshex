angular.module('groupsList', [], function ($interpolateProvider, $httpProvider, $routeProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');

    $routeProvider
      .when('/', {controller:ListCtrl, templateUrl:'groups-list.html'})
      .when('/edit/:groupId', {controller:EditCtrl, templateUrl:'groups-detail.html'})
      .when('/new', {controller:CreateCtrl, templateUrl:'groups-detail.html'})
    .otherwise({redirectTo:'/'});

    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
    $httpProvider.defaults.transformRequest = function(data) {
      if (typeof data != 'undefined') {
        return $.param(data);
      }
    }

  });
 
function ListCtrl($scope, $http) {
  $scope.groups = [{id: ''}];
  $http.get("/groups/get/", {headers: {"X-CSRFToken": csrftoken}, data:{}}).success(function(data) {
    $scope.groups = data;
  });
}
 
function CreateCtrl($scope, $http, $location, $timeout) {
  $scope.save = function() {
    group = {name:$scope.groupName};

    $http.post('/groups/add', group, {headers:{"X-CSRFToken": csrftoken}}).success(function(data) {
        $scope.group.push(data);
        $scope.name = '';
    });

    $timeout(function() { $location.path('/'); });
  }
}
 
function EditCtrl($scope, $location, $routeParams) {
  angularFire(fbURL + $routeParams.groupId, $scope, 'remote', {}).
  then(function() {
    $scope.group = angular.copy($scope.remote);
    $scope.group.$id = $routeParams.groupId;
    $scope.isClean = function() {
      return angular.equals($scope.remote, $scope.group);
    }
    $scope.destroy = function() {
      $scope.remote = null;
      $location.path('/');
    };
    $scope.save = function() {
      $scope.remote = angular.copy($scope.group);
      $location.path('/');
    };
  });
}