angular.module('groupsList', [], function ($interpolateProvider, $httpProvider, $routeProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');

    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
    //$httpProvider.defaults.transformRequest = function(data) {
    //  return $.param(data);
    //}

    $routeProvider.
      when('/', {controller:ListCtrl, templateUrl:'fb-groups-list.html'}).
      when('/edit/:groupId', {controller:EditCtrl, templateUrl:'fb-groups-detail.html'}).
      when('/new', {controller:CreateCtrl, templateUrl:'fb-groups-detail.html'}).
      otherwise({redirectTo:'/'});
  });
 
function ListCtrl($scope, $http) {
  $scope.groups = [{id: ''}];
  $http.get("/groups/get/", {headers: {"X-CSRFToken": csrftoken}, data:{}}).success(function(data) {
        $scope.groups = data;
    });
}
 
function CreateCtrl($scope, $location, $timeout, Groups) {
  $scope.save = function() {
    Groups.add($scope.group, function() {
      $timeout(function() { $location.path('/'); });
    });
  }
}
 
function EditCtrl($scope, $location, $routeParams, angularFire, fbURL) {
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