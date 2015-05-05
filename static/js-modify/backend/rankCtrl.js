require("../../../bower_components/angular/angular.js");
function getQueryParams(name,url) {
        if(!url)url = location.href;
        name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
         var regexS = "[\\?&]"+name+"=([^&#]*)";
         var regex = new RegExp( regexS );
         var results = regex.exec( url );
         return results == null ? null : results[1];
    };
var app = angular.module('app',[]);
app.config(function($interpolateProvider){
   $interpolateProvider.startSymbol('{[{');
   $interpolateProvider.endSymbol('}]}');     
});
rankCtrl = app.controller('rankCtrl',['$scope','$http','$q',function($scope,$http,$q){
    $http.get("/benz/backend/getSignWall/?id="+getQueryParams('id',location.href)).success(function(d){
        $scope.users = d;
    });
    setInterval(function(){
        $http.get("/benz/backend/getSignWall/?id="+getQueryParams('id',location.href)).success(function(d){
            users = d;
            flag = false;
            for (i in $scope.users.user) {
                if ($scope.users.user[i].headimgurl != d.user[i].headimgurl || $scope.users.user[i].nickname != d.user[i].nickname || $scope.users.user[i].id != d.user[i].id) {
                    console.log($scope.users.user[i]);
                    console.log(d.user[i]);
                    flag = true;
                }
            }
            if( flag || ! $scope.users.user.length ) {
                $scope.users = d;
            }
            console.log($scope.users.user);
        });
        
    },7000);
}]);
rankCtrl.$inject = ['$scope','rankCtrl'];
