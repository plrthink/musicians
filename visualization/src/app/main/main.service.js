'use strict';

// angular.module('visualization')
//   .factory('dataService', ['$firebase', function($firebase){

//     return function() {
//       var ref = new Firebase('https://musicians.firebaseio.com/').child('musicians');
//       return $firebase(ref).$asObject();
//     };

//   }]);
angular.module('visualization')
  .factory('dataService', ['$http', function($http){

    return function() {
      return $http.get('../../data/cluster_data.json');
    };

  }]);
