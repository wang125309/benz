require("../../../bower_components/angular/angular.js");
app = angular.module('app',['ngRoute']);
var rankCtrl = angular.module('app').controller('rankCtrl',['$scope','$q',function($scope,$q){
    console.log('???')
}]);
rankCtrl.$inject = ['$scope','rankCtrl'];
