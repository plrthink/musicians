'use strict';

angular.module('visualization')
  .directive('chart', [function () {

      var link = function(scope) {
      };
      return {
        template: '<div id="chart">\
                    <div ng-repeat="musician in musicians">\
                      <h3>{{musician.name}}</h3>\
                      <p>{{musician.id}}</p>\
                    </div>\
                  </div>',
        replace: true,
        scope: {musicians: '=musicians'},
        link: link,
        restrict: 'EA'
      };

  }]);
