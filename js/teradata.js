const app = angular.module('teradata.module', []);

function fixTooltips($timeout) {

  $timeout(() => $('.tagsinput').each((i, x) => {
    const title = $(x).prev().data('original-title') + '<br><br><b>(Press ENTER to add to list)</b>'
    $(x)
      .attr('data-toggle', 'tooltip')
      .attr('data-container', 'body')
      .attr('data-placement', 'right')
      .attr('data-html', 'true')
      .attr('data-title', title)
      .attr('data-original-title', title)
      .tooltip()
  }))

}

app.controller('TeradataController', function ($scope, $timeout) {

  let functionMetadata;

  $scope.getFunctionMetadata = function (selectedFunction) {

    if (typeof selectedFunction === 'undefined') return;

    $http.get('/plugins/AsterAnalytics/resource/data/' + selectedFunction + '.json')
      .success(function (data) {
        $scope.contents = data;
        functionMetadata = data;
      }).error(function (data, status, error, config) {
        $scope.contents = [{
          heading: "Error",
          description: "Could not load json data"
        }];
      });
  }

  $scope.getFunctionDescription = function () {
    return functionMetadata && ('long_description' in functionMetadata) ?
      functionMetadata.long_description :
      '';
  }

  $scope.getArgumentDescription = function (selectedFunction, functionArgument) {
    let description = '';
    if (functionMetadata && functionMetadata.argument_clauses) {

      const functionargumententry = functionMetadata.argument_clauses.filter(function (item) {
        if ('alternateNames' in item) {
          return item.alternateNames
            .map(x => x.toUpperCase())
            .indexOf(functionArgument.toUpperCase()) > -1;
        } else {
          return item.name.toUpperCase() === functionArgument.toUpperCase();
        }
      });

      if (functionargumententry && functionargumententry.length > 0) {
        description = functionargumententry[0].description;
      }

    }

    return description;
  };

  // temporary code to not show partition and order by fields when there are no unaliased input dataset
  $scope.shouldShowPartitionOrderFields = function(unaliasedInputsList)
  { 
	  return unaliasedInputsList && 0 < unaliasedInputsList.counts;
  }
  
  $scope.getSchema = function(functionArgument, aliasedInputsList, unaliasedInputsList, argumentsList)
  {
	  let targetTableName = ""
	  if ('targetTable' in functionArgument)
	  {
		  let targetTableAlias = functionArgument.targetTable;
		  let targetTableName = ""
		  if ("INPUTTABLE" === targetTableAlias.toUpperCase()) {
			  if (0 > unaliasedInputsList.count) {
				  if (unaliasedInputsList.values && 0 == unaliasedInputsList.values.length) {
					  targetTableName = unaliasedInputsList.values[0];
				  }
			  } else {
				  inputtableargument = (argumentsList || []).filter(arg => "INPUTTABLE" === arg.name.toUpperCase());
				  if (0 < inputtableargument.length) {
					  targetTableName = inputtableargument[0].value;
				  }
			  }
		  }
		  else {
			  let inputslist = (aliasedInputsList || []).filter(n => targetTableAlias.toUpperCase() === n.name.toUpperCase());
			  if (0 < inputslist.length) {
				  targetTableName = inputslist[0].value;
			  }
		  } 
	  }
	  else if (unaliasedInputsList.values && 0 == unaliasedInputsList.values.length) {
		  targetTableName = unaliasedInputsList.values[0]
	  }
	  if (!targetTableName)
	  {
		  return [];
	  }
	  if (targetTableName && targetTableName in $scope.inputschemas) {
		  return $scope.inputschemas[targetTableName];
	  }
	  return $scope.schemas;
  }

  $scope.callPythonDo({}).then(
    data => {
      $scope.choices = data.choices;
      $scope.schema = data.schema;
      $scope.inputs = data.inputs;
      $scope.inputschemas = data.inputschemas;
      console.log(data);

      $('select:first').change(() => {
        $timeout(() => {
          try {
            $('#tabs').tabs('destroy')
          } catch (e) {}

          $('#tabs').tabs();
          setTimeout(() => {
            $('input.teradata-tags').tagsInput({
              'onChange': x => $(x).trigger('change'),
              'defaultText': 'add param',
            });
            fixTooltips($timeout);
          }, 500);
        });
      });

      $('select:first, select:first > option').css('text-transform', 'capitalize');
    },
    data => {
      $scope.choices = [];
      $scope.schema = [];
      $scope.inputs = [];
      $scope.inputschemas;
      console.log(data);
    }

  );

  $scope.hasRequiredArguments = function () {
    if (!$scope.config.function.arguments || !$scope.config.function.arguments.length) {
      return false
    }

    return $scope.config.function.arguments.filter(x => x.isRequired).length > 0
  }

  $scope.hasOptionalArguments = function () {
    if (!$scope.config.function.arguments || !$scope.config.function.arguments.length) {
      return false
    }

    return $scope.config.function.arguments.filter(x => !x.isRequired).length > 0
  }

  $timeout(() => {

    const $a = $('.mainPane > div:first > div:first > div.recipe-settings-section2 > a');
    $a.text('Learn more about Teradata Aster');
    $a.css('color', 'orange');
    $a.parent().css('text-align', 'center');
    $a.attr('target', '_blank');

    $('#main-container > div > div:nth-child(1) > div > select')[0].value = '';
    $('.dss-page,#main-container').css('display', 'block');
    $('#main-container').tooltip();
    $('#tabs').tabs();
    setTimeout(() => {
      $('input.teradata-tags').tagsInput({
        'onChange': x => $(x).trigger('change'),
        'defaultText': 'add param',
      });
      fixTooltips($timeout);
    }, 500);

  });

});
