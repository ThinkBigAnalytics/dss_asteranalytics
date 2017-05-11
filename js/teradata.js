const app = angular.module('teradata.module', []);

app.controller('TeradataController', function ($scope) {
	
  var functionMetadata;
	
  $scope.getFunctionMetadata = function(selectedFunction)
  {
	  console.log('getfunctionmetadata');
	  $http.get('/plugins/AsterAnalytics/resource/data/' + selectedFunction + '.json')
      .success(function(data) {
          $scope.contents=data;
          functionMetadata = data;
      })
      .error(function(data,status,error,config){
          $scope.contents = [{heading:"Error",description:"Could not load json data"}];
          console.log($scope.contents);
      });
	  
  }
  
  $scope.getFunctionDescription = function()
  {
	  if (functionMetadata && 'long_description' in functionMetadata)
	  {
		  return functionMetadata.long_description;
	  }
	  return "";
  }
	
  $scope.getArgumentDescription = function(selectedFunction, functionArgument)
  {
	  var description = "";
	      if (functionMetadata && functionMetadata.argument_clauses)
	    	  {
	    	  
	          var functionargumententry = functionMetadata.argument_clauses.filter(function(item) {
	        	  if ('alternateNames' in item)
	        	  {
	        		  return (item.alternateNames.map(function(x){ return x.toUpperCase() }).indexOf(functionArgument.toUpperCase()) > -1)  
	        	  }
	        	  return (item.name.toUpperCase() === functionArgument.toUpperCase());
	        	});
	          if (functionargumententry && 0 < functionArgument.length)
	          {
	            
	            description = functionargumententry[0].description;
	          }
	          
	      }
	      
		  return description;
  };

  $scope.callPythonDo({}).then(
    data => {
      $scope.choices = data.choices;
      $scope.schema = data.schema;
      $scope.inputs = data.inputs;
      console.log(data);
      console.log(window.location.pathname);
      
      

      $('select:first').change(() => $('#tabs').tabs());
      $('select:first, select:first > option').css('text-transform', 'capitalize');
    },
    data => {
      $scope.choices = [];
      $scope.schema = [];
      $scope.inputs = [];
      console.log(data);
    }
    
    
  );
  
  

  setTimeout(() => {

    const $a = $('.mainPane > div:first > div:first > div.recipe-settings-section2 > a');
    $a.text('Learn more about Teradata Aster');
    $a.css('color', 'orange');
    $a.parent().css('text-align', 'center');
    $a.attr('target', '_blank');

    $('#main-container > div > div:nth-child(1) > div > select')[0].value = '';
    $('.dss-page,#main-container').css('display', 'block');
    $('#main-container').tooltip();
    $('#tabs').tabs()

  });

});