var app = angular.module('characterManager', [], function ($interpolateProvider) {
    $interpolateProvider.startSymbol("{[{");
    $interpolateProvider.endSymbol("}]}");
});

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.factory("flash", function(){
	var currentMessage = "";

	return {
		setMessage: function(message) {
			currentMessage = message;
		},
		getMessage: function(){
			return currentMessage;
		}
	};
});

app.controller('CharactersController', function($scope, $http, flash){

	$scope.flash = flash;
	var api_url = "/api/";

	$scope.num_chars = 0;
	$scope.characters = [];
	$scope.user = "";
	$scope.characters_url = "";

	$scope.load_characters = function(){
		$http.get($scope.characters_url).success(function(data){
			$scope.num_chars = data.count;
			$scope.characters = data.results;
		}).error(function(data){
			console.log("Error: " + data);
		});
	};

	$http.get(api_url + "current").success(function(data){
		$scope.user = data.username;
		$scope.characters_url = api_url + "users/" + $scope.user + "/charactersheets";
		$scope.load_characters();
	}).error(function(data){
		console.log("Error: " + data);
	});


	$scope.deleteChar = function(c){
		if (confirm('Are you sure you want to delete this characer: ' + c.name + '?')) {
    		// Delete it!
    		var url = api_url + "characters/" + c.slug;
    		$http.delete(url).success(function(data, status, headers, config) {
				flash.setMessage("Successfully deleted character " + c.name);	
				$scope.load_characters();
			}).error(function(data, status, headers, config) {
				alert("Create returned: " + status);
				console.log(data);
			});
		} 
	};

	var create_api_url = "/api/characters/create";
	$scope.char = {};
	$scope.createChar = function(){

		$http.post(create_api_url, $scope.char).success(function(data, status, headers, config) {
			flash.setMessage("Successfully created character " + $scope.char.name);
			var character_slug = data.slug;
			$scope.char = {};
			$scope.load_characters();
		}).error(function(data, status, headers, config) {
			alert("Create returned: " + status);
			console.log(data);
		});
	};
	
});
