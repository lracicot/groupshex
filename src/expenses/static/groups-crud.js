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
  $http.get(base_uri+"groups/get/", {headers: {"X-CSRFToken": csrftoken}, data:{}}).success(function(data) {
    $scope.groups = data;
  });
}
 
function CreateCtrl($scope, $http, $location, $timeout) {
  $scope.save = function() {
    group = {name:$scope.groupName};

    $http.post(base_uri+'groups/add', group, {headers:{"X-CSRFToken": csrftoken}}).success(function(data) {
        $scope.groups.push(data);
        $scope.name = '';
    });

    $timeout(function() { $location.path('/'); });
  }
}
 
function EditCtrl($scope, $location, $routeParams, $http) {

  $scope.members = [{id: ''}];
  $http.get(base_uri+"groups/get_members/"+$routeParams.groupId, {headers: {"X-CSRFToken": csrftoken}, data:{}}).success(function(data) {
    $scope.members = data;
  });

  $(document).ready(function(){
    $('#user_autocomplete').autocomplete({
      minLength: 2,
      source: function(req, add) {
          $.post(base_url+"groups/get_not_members/"+$routeParams.groupId, req, function(data) {
              var suggestions = [];

              $.each(data, function(i, val) {

                  suggestions.push({
                      label: val.name,
                      value: val.id
                  });
              });

              add(suggestions);
          }, 'json');
      },
      select: function(e, ui) {
        $.post(base_url+"groups/add_member/"+$routeParams.groupId+'/'+ui.item.value);
        $scope.$apply(function () {
          $scope.members.push({id:ui.item.value, name:ui.item.label});
        });
      },
      close: function(){
        $('#user_autocomplete').val('');
      }
    });
  });

  $http.get(base_uri+"groups/get/"+$routeParams.groupId, {headers: {"X-CSRFToken": csrftoken}, data:{}}).success(function(data) {
    $scope.groupName = data.name;
  });

  $scope.removeMember = function(member_id) {
    $.post(base_url+"groups/remove_member/"+$routeParams.groupId+'/'+member_id);
    $.each($scope.members, function(index, member){
      if (member.id == member_id) {
        $scope.members.splice(index, 1);
      }
    })
  }
  $scope.save = function() {
    $scope.remote = angular.copy($scope.group);
    $location.path(base_uri);
  };
}