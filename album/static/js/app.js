/**
 * The main JS file containing controller for our angula JS app.
 */

function albumController($scope, $http)
{
		$scope.url = '/api/v1/medias?format=json&offset=0&limit=100&order_by=-id';
	    $scope.mediaObjs = [];
	    
	    $scope.get = function () {
	    	$http.get($scope.url).success($scope.parseData);
	    }
	    
	    $scope.parseData = function(data, status){
	    	$scope.mediaObjs = data.objects;
	    }

	    $scope.get();
}