'use strict';

angular.module('visualization')
  .factory('firebaseService', ['$firebase', function($firebase){

    return function(){
      var ref = new Firebase('https://musicians.firebaseio.com/').child('musicians');
      return $firebase(ref).$asArray();
    };

  }]);
