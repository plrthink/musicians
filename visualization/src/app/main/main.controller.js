'use strict';

angular.module('visualization')
  .controller('MainCtrl', ['$scope', 'dataService',
    function ($scope, dataService) {

      // var musicians = dataService();
      // musicians.$loaded().then(function() {
      //   $scope.musicians = musicians;
      // });

      $scope.loaded = false;
      dataService().then(function(result) {
        console.log(result.data);
        $scope.musicians = result.data[2];
        $scope.loaded = true;
      });

      // dataService().then(function(result) {
      //   console.log(result.data);
      //   var musicians = {
      //         "name": "musicians",
      //         "children": result.data
      //       };
      //   $scope.musicians = musicians;
      // });

      // for debugging purpose
      $scope.$watch('musicians', function(value) {
        console.log(value);
      });

  }]);
