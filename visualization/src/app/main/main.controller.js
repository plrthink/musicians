'use strict';

angular.module('visualization')
  .controller('MainCtrl', ['$scope', 'firebaseService',
    function ($scope, firebaseService) {

      var musicians = firebaseService();
      musicians.$loaded().then(function() {
        console.log(musicians.length);
        $scope.musicians = musicians;
      });

  }]);
