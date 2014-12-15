'use strict';

angular.module('visualization')
  .controller('MainCtrl', ['$scope', 'firebaseService',
    function ($scope, firebaseService) {
      $scope.musicians = firebaseService() || [];
  }]);
