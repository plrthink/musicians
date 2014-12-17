'use strict';

angular.module('visualization')
  .controller('MainCtrl', ['$scope', 'firebaseService',
    function ($scope, firebaseService) {

      var musicians = firebaseService();
      musicians.$loaded().then(function() {
        $scope.musicians = musicians;
      });

      // for debugging purpose
      $scope.$watch('musicians', function(value) {
        console.log(value);
      });

  }]);
