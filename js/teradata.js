(function (window, document, angular, $) {

  if (typeof window === 'undefined' || !window) {
    throw new Error('DOM Window not present!')
  } else if (typeof document === 'undefined' || !document) {
    throw new Error('DOM Document not present!')
  } else if (typeof angular === 'undefined' || !angular) {
    throw new Error('Angular library not present!')
  } else if (typeof $ === 'undefined' || !$) {
    throw new Error('jQuery library not present!')
  }

  const app = angular.module('teradata.module', ['selectize']);

  app.controller('TeradataController', function ($scope, $timeout) {


    $scope.myModel;
  
  $scope.myOptions = [{value: '1', text: 'Jordy'}];
  
  $scope.changeOptions = function(){
    $scope.myOptions = [{value: '1', text: 'Kirk'}];
  }
  
  $scope.changeValue = function(){
    $scope.myModel = '2';
  }
  
  $scope.myConfig = {
    create: true,
    onChange: function(value){
      console.log('onChange', value)
    },
    // maxItems: 1,
    // required: true,
  }
  
  //simulate async option loading
  $timeout(function(){
    $scope.myOptions.push({value: '2', text: 'Crusher'})
  }, 2000);

    /**
     * A wrapper function that delays execution so that
     * the Angular rendering cycle will have finished before
     * running the given function f.
     */
    const $delay = f => $timeout(f, 100);

    /**
     * Default separator for list-like objects.
     */
    const SEPARATOR = String.fromCharCode(0);

    /**
     * A private variable containing the function metadata.
     */
    let functionMetadata;

    /**
     * A private variable containing the function metadata.
     */
    let functionVersion = '';
    let functionType = '';

    /**
     * A private variable containing the function to run the given recipe.
     */
    let runFunction;

    /**
     * Dialog container.
     */
    const $dialog = $('#dialog');

    /**
     * Validation dialog container.
     */
    const $validationDialog = $('#dialog-validation');

    /**
     * Function metadata path - this path contains the JSON metadata of each function.
     */
    const FUNCTION_METADATA_PATH = '/plugins/AsterAnalytics/resource/data/';

    /**
     * Parameters to use for the dialog box.
     */
    const DIALOG_PARAMETERS = {
      modal: true,
      width: '33%',
      minHeight: 250,
    }

    /**
     * Parameters to use for the dialog box CSS.
     */
    const DIALOG_CSS_PARAMETERS = {
      'max-height': '70vh',
      overflow: 'auto'
    }

    /**
     * Number of milliseconds per listen interval.
     */
    const LISTEN_INTERVAL = 50;

    /**
     * Object keys that are repeatedly used in this script.
     */
    const KEYS = {
      LONG_DESCRIPTION: 'long_description',
      ALTERNATE_NAMES: 'alternateNames',
      TARGET_TABLE: 'targetTable',
      INPUT_TABLE: 'INPUTTABLE',
      INPUT_TABLE_ALTERNATIVE: 'INPUT_TABLE'
    }

    /** Regex for locating HTML entities. */
    const ENTITY_REGEX = /[\u00A0-\u9999<>\&]/gim

    /** Properly encodes an HTML entity. */
    function encodeRegex(i) {
      return '&#' + i.charCodeAt(0) + ';';
    }

    $.extend($scope, {

      /**
       * Shows a dialog.
       * 
       * This is for displaying Aster-side errors.
       */
      dialog: function (title, content, elem) {

        // [HACK] Sometimes, the title is "error" because of timing issues.
        // So we force it to succeed if the content is "Job succeeded".
        if (content === 'Job succeeded.') {
          title = 'Success'
        }

        $dialog.find('pre').text(content);
        $(elem).click(() => $('.ui-dialog-content').dialog('close'));
        $dialog.find('.other').empty().append(elem);

        $dialog
          .attr('title', title)
          .dialog(DIALOG_PARAMETERS);

        $dialog.css(DIALOG_CSS_PARAMETERS);

      },

      /**
       * Shows a dialog.
       * 
       * This is for displaying frontend validation errors.
       */
      validationDialog: function (html) {

        $validationDialog.find('div').html(html);
        $validationDialog.dialog(DIALOG_PARAMETERS);
        $validationDialog.css(DIALOG_CSS_PARAMETERS);

      },

      /**
       * Gets the static JSON metadata of the given function.
       */
      getFunctionMetadata: function (selectedFunction) {

        if (typeof selectedFunction === 'undefined') {
          return;
        }

        const promise = $http
          .get(`${FUNCTION_METADATA_PATH}${selectedFunction}.json`)
          .success(data => {
            functionMetadata = data;
            console.log(functionMetadata);
            functionVersion = functionMetadata.function_version;
            // functionType = functionMetadata.function_type.toLowerCase();
            // $scope.config.function.function_type = functionMetadata.function_type.toLowerCase();
            console.log(functionVersion);
            // console.log(functionType);
            // console.log($scope.config.function_type);

            // //console.log('Function Metadata');
            // //console.log(data);
            // //console.log($scope.config);

            $scope.preprocessDescriptions();
            $scope.preprocessMetadata();
            $scope.activateTabs();
            $scope.activateMultiTagsInput();
            $scope.activateTooltips();
          })

      },

      /**
       * Preprocesses the descriptions so that the special characters are correctly rendered.
       */
      preprocessDescriptions: function () {

        if (!functionMetadata || !functionMetadata.argument_clauses)
          return;

        functionMetadata.argument_clauses.forEach(
          x => {
            try {

              x.description = x.description
                ? x.description.replace(ENTITY_REGEX, encodeRegex)
                : ''

            } catch (e) { }
          }
        )

      },

      /**
       * Gets the function description from the static JSON metadata.
       */
      getFunctionDescription: function () {

        return (functionMetadata && KEYS.LONG_DESCRIPTION in functionMetadata) ?
          functionMetadata.long_description :
          '';

      },

      /**
       * Checks if there is a version mismatch in function_version
       */
      checkVersionMismatch: function () {
        // $delay(() => {
    	if (!$scope.config.function) {
    		return false;
    	}
        var previousVersion = $scope.config.function.function_version ? $scope.config.function.function_version : ''
        console.log($scope.config.function.function_version ? $scope.config.function.function_version : '');
        if (($scope.config.function.function_version ? $scope.config.function.function_version : '') === functionVersion || ($scope.config.function.function_version ? $scope.config.function.function_version : '') === '') {
          return false;
        } else {
          console.warn('Function version mismatch');
          console.warn('Previous Version:', previousVersion)
          console.warn('Installed Version:', functionVersion)
          return true;
        }

        // })
      },
      
      addPartitionByColumn: function() {
        console.log('Added one column')
        $scope.config.function.partitionAttributes.push('');
    },
    removePartitionByColumn: function(index) {
      if (index > -1) {
          $scope.config.function.partitionAttributes.splice(index, 1);
      }
    },

    addOrderByColumn: function() {
      console.log('Added one column')
      $scope.config.function.orderByColumn.push('');
    },
    removeOrderByColumn: function(index) {
      if (index > -1) {
        $scope.config.function.orderByColumn.splice(index, 1);
      }
    },
      validityChanger: function () {
        // console.log('Validity changer happened');
        // console.log($('#selectize-selectized').parent().parent());
        // console.log($('#selectize-selectized'))
        // $('#selectize-selectized').parent().parent().removeClass("ng-invalid");
        // if (!$('div.ng-invalid').hasClass('invalid')) {
        $('div.ng-invalid').removeClass('ng-invalid')
        // }
        $('#selectize-selectized').removeClass('ng-invalid');
        $('div.invalid').addClass('ng-invalid')
        // console.log($('#selectize-selectized').parent().parent());
        // console.log($('#selectize-selectized'))

        return true;
      },

      /**
       * Checks if function is a driver function
       */
      checkIfDriverFunction: function () {
          return functionMetadata && functionMetadata.argument_clauses &&
              functionMetadata.argument_clauses.filter(arg => arg.isOutputTable).length;
      },

      /**
       * Gets the description of the given argument from the static JSON metadata.
       */
      getArgumentDescription: function (i) {

        try {

          return (functionMetadata && functionMetadata.argument_clauses[i])
            ? functionMetadata.argument_clauses[i].description
            : null;

        } catch (e) {

          return null

        }

      },

      getArgumentWithName: function (name) {
          return (functionMetadata && functionMetadata.argument_clauses) ?
                  functionMetadata.argument_clauses.find(argument => (argument.
                          name.toUpperCase() === name.toUpperCase()) ||
                          (argument.alternateNames && argument.alternateNames.
                                  findIndex(x=> x.toUpperCase() === name.toUpperCase() ) != -1)) :
                      null;
      },

      getPermittedValuesWithName: function (item) {
    	  let name = item.name;
          let argument = $scope.getArgumentWithName(name);
          let permittedvalues = argument && argument.permittedValues && argument.permittedValues.length ?
        		  argument.permittedValues : null;
          //if (permittedvalues && item.allowsLists && (typeof item.value === 'string')) {
        	//  item.value = item.value.split(',');
          //}
          return permittedvalues;
      },

      getArgumentDescriptionWithName: function (name) {
          let argument = $scope.getArgumentWithName(name);
          return argument ? argument.description : null;
      },

      getArgumentFormattedName: function (name) {
          let argument = $scope.getArgumentWithName(name);
          return argument ? argument.name.replace(/([A-Z]+)/g, " $1")
                  .replace(/([A-Z][a-z])/g, " $1").split('_').join(' ')
                  : name;
      },

      /**
       * Gets the schema of the unaliased inputs from the static JSON metadata.
       */
      getSchemaOfUnaliasedInputs: function (unaliasedInputsList) {

        if (!unaliasedInputsList
          || !unaliasedInputsList.values
          || !unaliasedInputsList.values.length)
          return [];

        const targetTableName = unaliasedInputsList.values[0];

        return $scope.inputschemas
          && targetTableName
          && targetTableName in $scope.inputschemas
          ? $scope.inputschemas[targetTableName]
          : []

      },

      findTableNameInArgumentsList: function (argumentsList, tableNameAlias) {
        //Get alternate names
        var tableNameAliases = [];
        tableNameAliases.push(tableNameAlias);
        if (!functionMetadata) {
          return '';
        }
        functionMetadata.argument_clauses.map(argument => {
          if (argument.name.toUpperCase() === tableNameAlias) {
            if (KEYS.ALTERNATE_NAMES in argument) {
              argument.alternateNames.map(function (altname) { tableNameAliases.push(altname); })
            }
            // console.log('tableNameAliases');
            // console.log(tableNameAliases);
            // tableNameAliases.push(argument.name.toUpperCase());

          }
        })
        let potentialMatches = argumentsList
          .filter(arg => tableNameAliases.includes(arg.name.toUpperCase()));
        // .filter(arg => tableNameAlias.toUpperCase() === arg.name.toUpperCase());
        // .filter(arg => [KEYS.INPUT_TABLE, KEYS.INPUT_TABLE_ALTERNATIVE].includes(arg.name.toUpperCase()));
        // console.log('Find tablename');
        // console.log(potentialMatches);
        // console.log(argumentsList);
        if (potentialMatches.length) {
          // console.log(potentialMatches);
          //console.log('We finally got here');
          return potentialMatches[0].value;
        }
        return ''

      },

      /**
       * Gets the function schema by joining and processing the metadata from the python backend 
       * and the static JSON file associated with the function.
       */
      getSchema: function (functionArgument, aliasedInputsList, unaliasedInputsList, argumentsList) {
        //console.log('Get Schema runs');
        aliasedInputsList = aliasedInputsList || []
        argumentsList = argumentsList || []
        console.log('getSchema');
        // console.log(functionMetadata)
        console.log(functionArgument);
        console.log(aliasedInputsList);
        console.log(unaliasedInputsList);
        console.log(argumentsList);
        const hasTargetTable = KEYS.TARGET_TABLE in functionArgument
        let targetTableName = ''
        var isAliasedInputsPopulated;
        var isInAliasedInputsList = false;
        var y = false;
        if (hasTargetTable) {
          //console.log('hasTargetTable');
          const targetTableAlias = functionArgument.targetTable.toUpperCase();
          // if (KEYS.ALTERNATE_NAMES in func)
          // var tableAliasList = 
          console.log('Table name');
          console.log(targetTableAlias);
          // const isAliased = KEYS.INPUT_TABLE !== targetTableAlias;
          if (aliasedInputsList !== []) {
            isAliasedInputsPopulated = true;
            aliasedInputsList.map((input) => {
              if (input.name.toUpperCase() === targetTableAlias.toUpperCase()) {
                console.log('true');
                isInAliasedInputsList = true;
              }
            }
            )
          } else {
            isInAliasedInputsList = false;
          }
          // const isAliased = aliasedInputsList.includes(targetTableAlias);
          const isAliased = isInAliasedInputsList;
          //console.log(KEYS.INPUT_TABLE);
          //console.log(targetTableAlias);

          if (isAliased) {
            console.log('isAliased');
            let matchingInputs = aliasedInputsList.filter(input => targetTableAlias === input.name.toUpperCase());
            if (matchingInputs.length > 0) {
              //console.log('Matching inputs > 0');
              targetTableName = matchingInputs[0].value;
            } else {
              //console.log('Matching inputs < 0');
              targetTableName = $scope.findTableNameInArgumentsList(argumentsList, targetTableAlias);
            }


          } else {
            //console.log('isNotAliased');
            //console.log(unaliasedInputsList);
            if (unaliasedInputsList.count && unaliasedInputsList.values && unaliasedInputsList.values.length) {
              console.log('Went to unaliased');

              targetTableName = unaliasedInputsList.values[0];
              //console.log(targetTableName);
            }

            else {
              targetTableName = $scope.findTableNameInArgumentsList(argumentsList, targetTableAlias);
              console.log('Went to arguments');
              console.log(targetTableName);
            }


          }

        } else if (unaliasedInputsList && unaliasedInputsList.values && unaliasedInputsList.values.length > 0) {

          targetTableName = unaliasedInputsList.values[0]
          //console.log('This else if');
          //console.log(targetTableName);

        }

        if (!targetTableName || !$scope.inputschemas) {
          //console.log('This happened');
          //console.log(targetTableName);
          //console.log($scope);
          return [];
        }


        if (targetTableName && targetTableName in $scope.inputschemas) {
          //console.log('Schemas');
          //console.log($scope.inputschemas[targetTableName]);
          return $scope.inputschemas[targetTableName];

        }

        return $scope.schemas;

      },

      /**
       * Checks whether or not we should show the partition order fields.
       * 
       * NOTE: Temporary code to not show partition 
       * and order by fields when there are no unaliased input dataset
       */
      shouldShowPartitionOrderFields: function (unaliasedInputsList) {
        return unaliasedInputsList && unaliasedInputsList.count > 0;
      },

      /**
       * Checks whether or not the given argument is an output table or not.
       */
      isArgumentOutputTable: function (functionArgument) {
        return functionArgument.isOutputTable
      },

      /**
       * Checks whether or not required arguments are present in the function metadata.
       */
      hasRequiredArguments: function () {

        if (!$scope.config.function.arguments || !$scope.config.function.arguments.length)
          return false

        return $scope.config.function.arguments.filter(x => x.isRequired).length > 0

      },

      /**
       * Checks whether or not optional arguments are present in the function metadata.
       */
      hasOptionalArguments: function () {

        const hasOptionalInputTable = $scope.config.function.required_input
          && $scope.config.function.required_input.length
          && ($scope.config.function.required_input.filter(x => !x.isRequired).length > 0);

        const hasOptionalArgument = $scope.config.function.arguments
          && $scope.config.function.arguments.length
          && ($scope.config.function.arguments.filter(x => !x.isRequired).length > 0);

        return hasOptionalInputTable || hasOptionalArgument;

      },

      /**
       * A function that listens for job results.
       * It accepts a callback function f that is executed after the results are received.
       * The presence or absence of the job results are listened to 
       * by using a simple setInterval (which checks for results every 50ms).
       * 
       * NOTE: This is a hack-ish implementation because we donot know how to listen to the job results properly.
       * If Dataiku publishes a proper DOM event then we should listen to that event instead.
       * But, currently, that event is not being published.
       */
      listenForResults: function (f) {
        const listener = setInterval(() => {
          const $jobResult = $('.recipe-editor-job-result')
          if ($jobResult.length && f()) {
            clearInterval(listener);
            $jobResult.remove();
          }
        }, LISTEN_INTERVAL)
      },

      /**
       * Function that validates all the input controls of the recipe.
       * 
       * Returns true if valid. If not, it shows an error dialog then returns false.
       */
      validate: function () {

        const invalids = []
        $('.ng-invalid:not(form,.ng-hide,div,#selectize-selectized)').each((i, x) => invalids.push($(x).parent().prev().text()))

        if (invalids.length) {
          $scope.validationDialog(`Please amend the following fields: <ul>${invalids.map(x => `<li>${x}</li>`).join('')}</ul>`)
          return false
        }

        return true

      },

      /**
       * Function to execute the "proper" run workflow of an Aster recipe.
       * 
       * Firstly, the inputs are validated.
       * If the inputs are valid, it proceeds to the run phase 
       * which runs the original runFunction of the recipe (which we hijacked earlier).
       * It then listens for any results by using the listenForResults function.
       * Once the results are back, it displays it in a jQuery UI dialog box.
       */
      runThenListen: function () {

        if (!$scope.validate()) return;

        //console.log(functionVersion);
        //console.log($scope.config.function.function_version);
        $scope.config.function.function_version = functionVersion;
        // $scope.config.function.orderByColumn = $scope.config.function.orderByColumns;
        // $scope.config.function.partitionAttributes = $scope.config.function.partitionByColumns;
        
        // console.log($scope.config.function.orderByColumns);
        // console.log($scope.config.function.partitionByColumns)
        // console.log(scope.config.function.partitionByColumns)
        // failer.push("a");
        runFunction();

        $scope.listenForResults(function () {
          //console.log('Got results');
          // //console.log(message);
          //console.log(functionVersion);
          //console.log($scope.config.function.function_version);
          const $results = $('.alert:not(.ng-hide):not(.messenger-message)')

          if ($results.length === 0) return false;

          try {

            const title = $results.get(0).classList[1].split('-')[1]

            if (!title || title === 'info')
              return false

            const result = $results.find('h4').text()

            const $jobLinkClone = $results.find('a').last().clone(true, true)

            $results.remove()
            $scope.dialog(title, result, $jobLinkClone)

            return true

          } catch (e) { }

          return false

        })

      },

      /**
       * Resolves a code-conflict issue between jQuery and Bootstrap.
       */
      initializeBootstrap: function () {
        if ($.fn.button && $.fn.button.noConflict)
          $.fn.bootstrapBtn = $.fn.button.noConflict()
      },

      /**
       * Communicates with Python backend 
       * and acquires necessary data to display in the recipe UI.
       */
      communicateWithBackend: function () {

        $scope.callPythonDo({}).then(
          data => $.extend($scope, data),
          () => { }
        );

      },

      /**
       * Activates the tabbing functionality of this recipe.
       */
      activateTabs: function () {
        try {
          $('#tabs').tabs('destroy')
        } catch (e) { }
        $('#tabs').tabs();
      },

      /**
       * Activates the informative tooltips of each input control.
       * Hijacks each tagsInput element so that it properly displays tooltips as well.
       */
      activateTooltips: function () {

        $('#main-container').tooltip();

        $delay(() => {

          $('.tagsinput').each((i, x) => {

            const original = $(x).prev().attr('data-original-title') || ''

            const title = original ?
              (original + '<br><br><b>(Press ENTER to add to list)</b>') :
              '<b>(Press ENTER to add to list)</b>'
            $(x).data({
              toggle: 'tooltip',
              container: 'body',
              placement: 'right',
              html: true,
              title: title,
              'original-title': title
            })
              .tooltip()

          });

        });

      },

      /**
       * Activates the multi-string input boxes.
       */
      activateMultiTagsInput: function () {
    	  $delay(() => {
        try {

          $('input.teradata-tags').tagsInput({
            unique: false,
            onChange: x => $(x).trigger('change'),
            defaultText: 'add param',
            delimiter: SEPARATOR
          });

        } catch (e) { }
    	  });
      },

      /** 
       * Hijacks the current click handler of the recipe
       * and replaces it with the runThenListen function.
       * 
       * Stores the original recipe run function in the runFunction variable.
       */
      activateValidation: function () {

        const $runButton = $('.btn-run-main')
        runFunction = $._data($runButton.get(0), 'events').click[0].handler.bind($runButton.get(0));
        $runButton
          .off('click')
          .on('click', e => $scope.runThenListen());

      },

      /**
       * Hijacks the current UI and applies a few cosmetic improvements.
       */
      activateCosmeticImprovements: function () {

        const $a = $('.mainPane > div:first > div:first > div.recipe-settings-section2 > a');
        $a
          .text('Aster Analytics Foundation 6.20\nLearn more about Teradata Aster')
          .css('color', 'orange')
          .attr('target', '_blank');
        $a.html($a.html().replace(/\n/g,'<br/>'));
        $a.parent().css('text-align', 'center');
        $('#main-container > div > div:nth-child(1) > div > select')[0].value = '';
        $('.dss-page,#main-container').css('display', 'block');
        $('select:first, select:first > option').css('text-transform', 'capitalize');
        $('form').attr('novalidate', 'novalidate');




      },

      /**
       * Applies the custom changes to the default Dataiku UI needed for the Aster plugin to work.
       */
      activateUi: function () {

        $delay(() => {

          $scope.initializeBootstrap();

          $scope.activateCosmeticImprovements();
          $scope.activateTabs();
          $scope.activateMultiTagsInput();
          $scope.activateValidation();
          console.log('Initializing first tab')
          document.getElementById("defaultOpen").click();
          $scope.reloader = true;
          

        });

        

      },
      

      cleanName: function (rawName) {

        return rawName.split('_').join(' ').toLowerCase()

      },

      cleanKind: function (rawKind) {

        return rawKind ? `(${rawKind})` : ''

      },

      // Opens tabs
      openTabs: function(evt, tabName) {
        // Declare all variables
        var i, tabcontent, tablinks;
        console.log(evt); 
        // Get all elements with class="tabcontent" and hide them
        tabcontent = document.getElementsByClassName("plugintabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }
    
        // Get all elements with class="tablinks" and remove the class "active"
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
    
        // Show the current tab, and add an "active" class to the button that opened the tab
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";
    },

      /**
       * Preprocess function metadata.
       */
      preprocessMetadata: function () {
        if (
          !functionMetadata
          || !$scope.config
          || !$scope.config.function
          || !$scope.config.function.arguments
          || !$scope.config.function.arguments.length) {
        	return;
        }

        $delay(() => {

          // Re-arrange functions alphabetically.
          if ($scope.choices) {
            $scope.choices = $scope.choices.sort((a, b) => a.name.localeCompare(b.name))
          }
          
          let i = 0;
          $scope.config.function.arguments.forEach(argument => {
        	  // Index each argument for easy access.
        	  argument.i = i;
        	  ++i;
        	  
        	  let permittedValues = $scope.getPermittedValuesWithName(argument);
        	              if (permittedValues && argument.allowsLists) {
        	              	let curvalue = argument.value;
        	              	if (typeof curvalue === 'string') {
        	              		argument.value = argument.value.split(',');
        	              	}
        	              }
          });

          // Re-arrange argument order.
          $scope.config.function.arguments = [
            ...$scope.config.function.arguments.filter(x => x.datatype === 'TABLE_NAME'),
            ...$scope.config.function.arguments.filter(x => x.datatype !== 'TABLE_NAME'),
          ]

        });

      },

      /**
       * Initializes this plugin.
       */
      initialize: function () {

        $scope.communicateWithBackend();
        if ($scope.config.function) {
          $scope.getFunctionMetadata($scope.config.function.name);
        }
        $scope.config.function.partitionAttributes = $scope.config.function.partitionAttributes || [];
        $scope.config.function.orderByColumn = $scope.config.function.orderByColumn || [];

        $scope.preprocessMetadata();
        $scope.activateUi();

      },

      /**
       * Initializes this plugin.
       */
      refresh: function (selectedFunction) {

        $scope.getFunctionMetadata(selectedFunction);
        $scope.preprocessMetadata();
      }

    })
    $scope.reloader = false;
    $scope.initialLoading = true;
    $scope.initialize();

  });

  // app.directive('selectize', function () {
  //   var linker = function (scope, element, attr, $timeout) {
  //     // $scope.$watch('$scope.config', function () {
  //     //   console.log('Chosen directive watch happened');
  //     //   element.trigger('liszt:updated');
  //     //   element.trigger('chosen:updated')
  //     // })
  //     scope.$watch('reloader', function (newValue, oldValue, scope) {
  //       console.log('Chosen directive watch happened( inputSchemas)');
  //       console.log(scope.reloader);
  //       element.selectize()[0].selectize.destroy();
  //       // $timeout(function () {
  //       // console.log('Inside timeout');
  //       element.selectize();
  //       // }, 100);
  //       // element.trigger('liszt:updated');        
  //       // element.selectize().destroy();
  //       // element.selectize();
  //       // $element.trigger('chosen:updated')
  //     })
  //     element.selectize();
  //   };

  //   return {
  //     restrict: 'A',
  //     link: linker
  //   }
  // })

  // app.directive('selectize', function($timeout) {
  //         return {
  //             // Restrict it to be an attribute in this case
  //             restrict: 'A',
  //             require: '?ngModel',
  //             // responsible for registering DOM listeners as well as updating the DOM
  //             link: function(scope, element, attrs, ngModel) {
  //                 var $element;
  //                 $timeout(function() {
  //                     $element = $(element).selectize(scope.$eval(attrs.selectize));
  //                     if(!ngModel){
  //                         console.log('no ngModel')
  //                         return;
  //                     }

  //                     $(element).selectize().on('change',function(){
  //                         scope.$apply(function(){
  //                             var newValue = $(element).selectize().val();
  //                             console.log('change:',newValue);                    
  //                             ngModel.$setViewValue(newValue);
  //                         });
  //                     });
  //                 });
  //             }
  //         };
  //     });


  

  // angular.module('selectize', [])

  //   .directive('selectize', ['$parse', '$timeout', function ($parse, $timeout) {
  //     var NG_OPTIONS_REGEXP = /^\s*([\s\S]+?)(?:\s+as\s+([\s\S]+?))?(?:\s+group\s+by\s+([\s\S]+?))?\s+for\s+(?:([\$\w][\$\w]*)|(?:\(\s*([\$\w][\$\w]*)\s*,\s*([\$\w][\$\w]*)\s*\)))\s+in\s+([\s\S]+?)(?:\s+track\s+by\s+([\s\S]+?))?$/;

  //     return {
  //       scope: {
  //         multiple: '@',
  //         opts: '@selectize'
  //       },
  //       require: '?ngModel',
  //       link: function (scope, element, attrs, ngModelCtrl) {
  //         var opts = scope.$parent.$eval(scope.opts) || {};
  //         var initializing = false;
  //         var modelUpdate = false;
  //         var optionsUpdate = false;
  //         var selectize, newModelValue, newOptions, updateTimer;

  //         watchModel();

  //         if (attrs.ngDisabled) {
  //           watchParentNgDisabled();
  //         }

  //         if (!attrs.ngOptions) {
  //           return;
  //         }

  //         var match = attrs.ngOptions.match(NG_OPTIONS_REGEXP);
  //         var valueName = match[4] || match[6];
  //         var optionsExpression = match[7];
  //         var optionsFn = $parse(optionsExpression);
  //         var displayFn = $parse(match[2] || match[1]);
  //         var valueFn = $parse(match[2] ? match[1] : valueName);

  //         watchParentOptions();

  //         function watchModel() {
  //           scope.$watchCollection(function () {
  //             // console.log('Watch collection');
  //             //TO TEST
  //             // console.log(newModelValue);
  //             // console.log(ngModelCtrl.$modelValue);
  //             return ngModelCtrl.$modelValue;
  //           }, function (modelValue) {
  //             // console.log('MODEL EFFIN VALUE');
  //             // console.log(newModelValue);
  //             // console.log(modelValue);
  //             //experimental code
  //             if (modelValue != undefined) {
  //               // console.log('Outer if statement');
  //               if (newModelValue == undefined || modelValue.length < newModelValue.length) {
  //                 // console.log('That if Statement');
  //                 newModelValue = modelValue;
  //                 modelUpdate = true;
  //                 if (!updateTimer) {
  //                   scheduleUpdate();
  //                 }

  //               }
  //             }


  //           });
  //         }

  //         function watchParentOptions() {
  //           scope.$parent.$watchCollection(optionsExpression, function (options) {
  //             // console.log('OPTIONS?!?!')
  //             // console.log(options);
  //             newOptions = options || [];
  //             optionsUpdate = true;
  //             if (!updateTimer) {
  //               scheduleUpdate();
  //             }
  //           });
  //         }

  //         function watchParentNgDisabled() {
  //           scope.$parent.$watch(attrs.ngDisabled, function (isDisabled) {
  //             if (selectize) {
  //               isDisabled ? selectize.disable() : selectize.enable();
  //             }
  //           });
  //         }

  //         function scheduleUpdate() {
  //           // console.log('ScheduleUpdate?');
  //           if (!selectize) {
  //             if (!initializing) {
  //               initSelectize();
  //             }
  //             return;
  //           }

  //           updateTimer = $timeout(function () {
  //             var model = newModelValue;
  //             var options = newOptions;
  //             var selectizeOptions = Object.keys(selectize.options);
  //             var optionsIsEmpty = selectizeOptions.length === 0 || selectize.options['?'] && selectizeOptions.length === 1;
  //             if (optionsUpdate) {
  //               if (!optionsIsEmpty) {
  //                 selectize.clearOptions();
  //               }
  //               selectize.load(function (cb) {
  //                 cb(options.map(function (option, index) {
  //                   return {
  //                     text: getOptionLabel(option),
  //                     value: index
  //                   };
  //                 }));
  //               });
  //             }

  //             if (modelUpdate || optionsUpdate) {
  //               // console.log('MODEL PLS');
  //               // console.log(model);
  //               var selectedItems = getSelectedItems(model);
  //               // console.log('SELECTED ITEMS?!!?!?!');
  //               // console.log(selectedItems); 
  //               if (scope.multiple || selectedItems.length === 0) {
  //                 selectize.clear();
  //                 //clear can set the model to null
  //                 ngModelCtrl.$setViewValue(model);
  //               }
  //               selectedItems.forEach(function (item) {
  //                 selectize.addItem(item);
  //               });
  //               //wait to remove ? to avoid a single select from briefly setting the model to null
  //               selectize.removeOption('?');

  //               var $option = selectize.getOption(0);
  //               if ($option) selectize.setActiveOption($option);
  //             }

  //             modelUpdate = optionsUpdate = false;
  //             updateTimer = null;
  //           });
  //         }

  //         function initSelectize() {
  //           initializing = true;
  //           scope.$evalAsync(function () {
  //             initializing = false;
  //             element.selectize(opts);
  //             selectize = element[0].selectize;
  //             if (attrs.ngOptions) {
  //               if (scope.multiple) {
  //                 // console.log('Initializing');
  //                 selectize.on('item_add', onItemAddMultiSelect);
  //                 selectize.on('item_remove', onItemRemoveMultiSelect);
  //               } else if (opts.create) {
  //                 selectize.on('item_add', onItemAddSingleSelect);
  //               }
  //             }
  //           });
  //         }

  //         function onItemAddMultiSelect(value, $item) {
  //           var model = ngModelCtrl.$viewValue || [];
  //           console.log(model);
  //           var options = optionsFn(scope.$parent);
  //           var option = options[value];
  //           value = option ? getOptionValue(option) : value;
  //           // console.log('Does it get reset here?');
  //           console.log(model);
  //           if (model.indexOf(value) === -1) {
  //             model.push(value);
  //             // console.log('What about here?');
  //             console.log(model);
  //             if (!option && opts.create && options.indexOf(value) === -1) {
  //               options.push(value);
  //             }
  //             scope.$evalAsync(function () {
  //               ngModelCtrl.$setViewValue(model);
  //             });
  //           }
  //         }

  //         function onItemAddSingleSelect(value, $item) {
  //           var model = ngModelCtrl.$viewValue;
  //           var options = optionsFn(scope.$parent);
  //           var option = options[value];
  //           // console.log('Single happens?');
  //           value = option ? getOptionValue(option) : value;

  //           if (model !== value) {
  //             model = value;

  //             if (!option && options.indexOf(value) === -1) {
  //               options.push(value);
  //             }
  //             scope.$evalAsync(function () {
  //               ngModelCtrl.$setViewValue(model);
  //             });
  //           }
  //         }

  //         function onItemRemoveMultiSelect(value) {
  //           // console.log('What about onItemRemoveMultiSelect');
  //           var model = ngModelCtrl.$viewValue;
  //           var options = optionsFn(scope.$parent);
  //           var option = options[value];
  //           // console.log('First model check');
  //           // console.log(model);
  //           value = option ? getOptionValue(option) : value;

  //           var index = model.indexOf(value);
  //           if (index >= 0) {
  //             model.splice(index, 1);
  //             // console.log('After splicing');
  //             // console.log(model);
  //             scope.$evalAsync(function () {
  //               ngModelCtrl.$setViewValue(model);
  //               // console.log('After set view value');
  //               // console.log(model);
  //             });
  //           }
  //         }

  //         function getSelectedItems(model) {
  //           model = angular.isArray(model) ? model : [model] || [];
  //           // console.log('What about getSelectedItems');
  //           // console.log(model);
  //           if (!attrs.ngOptions) {
  //             return model.map(function (i) { return selectize.options[i] ? selectize.options[i].value : '' });
  //           }

  //           var options = optionsFn(scope.$parent);

  //           if (!options) {
  //             return [];
  //           }

  //           var selections = options.reduce(function (selected, option, index) {
  //             var optionValue = getOptionValue(option);
  //             if (model.indexOf(optionValue) >= 0) {
  //               selected[optionValue] = index;
  //             }
  //             // console.log('selected');
  //             // console.log(selected);
  //             return selected;
  //           }, {});
  //           // console.log('Selections');
  //           // console.log(selections);
  //           return Object
  //             .keys(selections)
  //             .map(function (key) {
  //               return selections[key];
  //             });
  //         }

  //         function getOptionValue(option) {
  //           var optionContext = {};
  //           optionContext[valueName] = option;
  //           // console.log('What about getOptionValue');
  //           return valueFn(optionContext);
  //         }

  //         function getOptionLabel(option) {
  //           var optionContext = {};
  //           optionContext[valueName] = option;
  //           // console.log('What about getOptionLabel');
  //           return displayFn(optionContext);
  //         }

  //         scope.$on('$destroy', function () {
  //           if (updateTimer) {
  //             // console.log('What about destroy?');
  //             $timeout.cancel(updateTimer);
  //           }
  //         });
  //       }
  //     };
  //   }]);

})(window, document, angular, jQuery);