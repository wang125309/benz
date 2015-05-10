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
    $http.get("/benz/backend/getSignNum/?id="+getQueryParams("id",location.href)).success(function(num){
        $scope.num = num.num;   
        console.log($scope.num);
    });
    setInterval(function(){
        $http.get("/benz/backend/getSignWall/?id="+getQueryParams('id',location.href)).success(function(d){
            users = d;
            flag = false;
            for (i in $scope.users.user) {
                if ($scope.users.user[i].headimgurl != d.user[i].headimgurl || $scope.users.user[i].nickname != d.user[i].nickname || $scope.users.user[i].id != d.user[i].id) {
                    flag = true;
                }
            }
            if( flag || ! $scope.users.user.length ) {
                $scope.users = d;
            }
            console.log($scope.users.user);
        });
        $http.get("/benz/backend/getSignNum/?id="+getQueryParams("id",location.href)).success(function(num){
            $scope.num = num.num;   
        console.log($scope.num);
        });
    },7000);
}]);
rankCtrl.$inject = ['$scope','rankCtrl'];
