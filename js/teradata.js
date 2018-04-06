/**
 * Copyright © 2018 by Teradata.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
 * associated documentation files (the "Software"), to deal in the Software without restriction,
 * including without limitation the rights to use, copy, modify, merge, publish, distribute,
 * sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * The above copyright notice and this permission notice shall be included in all copies or
 * substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
 * NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 * DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

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

  const app = angular.module('teradata.module', []);

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

            $scope.config.function.partitionAttributes = $scope.config.function.partitionAttributes || [''];
            $scope.config.function.orderByColumn = $scope.config.function.orderByColumn || [''];

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
      
      addPartitionByColumn_TEST: function(partitionArray) {
        console.log('Added to partition array')
        console.log(partitionArray)
        partitionArray.push('');
    },

    initializeColumnArray: function(columnArray){
      columnArray = columnArray || [''];
      return columnArray;
    },

    initializeColumnArrayOptional: function(columnArray){
      columnArray = columnArray || [];
      return columnArray;
    },

    removePartitionByColumn_TEST: function(partitionArray,index) {
      if (index > -1) {
        console.log('Removed from partition array')
        console.log(partitionArray)
        partitionArray.splice(index, 1);
      }
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

    initTab:function(){
      $delay(() => {console.log('InitTab Happens');
      document.getElementById("defaultOpen").click();
      });
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
        $('div.ng-invalid').removeClass('ng-invalid')
        $('div.invalid').addClass('ng-invalid')

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
        if (potentialMatches.length) {
          return potentialMatches[0].value;
        }
        return ''

      },

      /**
       * Gets the function schema by joining and processing the metadata from the python backend 
       * and the static JSON file associated with the function.
       */
      getSchema: function (functionArgument, aliasedInputsList, unaliasedInputsList, argumentsList) {
        aliasedInputsList = aliasedInputsList || []
        argumentsList = argumentsList || []
        const hasTargetTable = KEYS.TARGET_TABLE in functionArgument
        let targetTableName = ''
        var isAliasedInputsPopulated;
        var isInAliasedInputsList = false;
        var y = false;
        if (hasTargetTable) {
          const targetTableAlias = functionArgument.targetTable.toUpperCase();
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
          const isAliased = isInAliasedInputsList;

          if (isAliased) {
            console.log('isAliased');
            let matchingInputs = aliasedInputsList.filter(input => targetTableAlias === input.name.toUpperCase());
            if (matchingInputs.length > 0) {
              targetTableName = matchingInputs[0].value;
            } else {
              targetTableName = $scope.findTableNameInArgumentsList(argumentsList, targetTableAlias);
            }


          } else {
            if (unaliasedInputsList.count && unaliasedInputsList.values && unaliasedInputsList.values.length) {
              targetTableName = unaliasedInputsList.values[0];
            }
            else {
              targetTableName = $scope.findTableNameInArgumentsList(argumentsList, targetTableAlias);
            }


          }

        } else if (unaliasedInputsList && unaliasedInputsList.values && unaliasedInputsList.values.length > 0) {

          targetTableName = unaliasedInputsList.values[0]
        }

        if (!targetTableName || !$scope.inputschemas) {
          return [];
        }


        if (targetTableName && targetTableName in $scope.inputschemas) {
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
        $('.ng-invalid:not(form,.ng-hide,div)').each((i, x) => invalids.push($(x).parent().prev().text()))

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
        $scope.config.function.function_version = functionVersion;
        runFunction();

        $scope.listenForResults(function () {
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
          $scope.initTab();
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

})(window, document, angular, jQuery);