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

  const app = angular.module('teradata-7.module', ['selectize']);

  app.controller('TeradataController7', function ($scope, $timeout) {

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
          .get(`${FUNCTION_METADATA_PATH}${selectedFunction}.json`, {
            transformResponse: [function (data) {
              if (typeof data === 'string') {
                // strip json vulnerability protection prefix
                data = data.replace(")]}',\n", '');
                data = data.replace(/: Infinity/g, ': "Infinity"');
                console.log(data);
                data = data.replace(/: -Infinity/g, ': "-Infinity"');
                data = JSON.parse(data, function censor(key, value) {
                  return value == Infinity ? "Infinity" : value;
                });
              }
              return data;
            }]
          })
          .success(data => {
            functionMetadata = data;
            functionVersion = functionMetadata.function_version;

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
    	  if (!$scope.config.function) {
            return false;
            }
        var previousVersion = $scope.config.function.function_version ? $scope.config.function.function_version : '';
        console.log($scope.config.function.function_version ? $scope.config.function.function_version : '');
        // console.log(functionVersion);
        if (($scope.config.function.function_version ? $scope.config.function.function_version : '') === functionVersion || ($scope.config.function.function_version ? $scope.config.function.function_version : '') === '') {
          console.log('False');
          return false;
        } else {
          console.log('True')
          console.warn('Function version mismatch');
          console.warn('Previous Version:', previousVersion)
          console.warn('Installed Version:', functionVersion)
          return true;
        }

        // })
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

      getPermittedValues: function (i) {

        try {
          return (functionMetadata
            && functionMetadata.argument_clauses[i]
            && functionMetadata.argument_clauses[i].permittedValues
            && functionMetadata.argument_clauses[i].permittedValues.length)
            ? functionMetadata.argument_clauses[i].permittedValues
            : null;

        } catch (error) {

          return null;

        }


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
        // tableNameAliases.push(tableNameAlias);
        //TODO: Change naming
        tableNameAliases = tableNameAlias;
        if (!functionMetadata) {
          return [''];
        }
        functionMetadata.argument_clauses.map(argument => {
          if (argument.name.toUpperCase() === tableNameAlias) {
            if (KEYS.ALTERNATE_NAMES in argument) {
              argument.alternateNames.map(function (altname) { tableNameAliases.push(altname); })
            }
            // tableNameAliases.push(argument.name.toUpperCase());

          }
        })
        let potentialMatches = argumentsList
          .filter(arg => tableNameAliases.includes(arg.name.toUpperCase()));
        // .filter(arg => tableNameAlias.toUpperCase() === arg.name.toUpperCase());
        // .filter(arg => [KEYS.INPUT_TABLE, KEYS.INPUT_TABLE_ALTERNATIVE].includes(arg.name.toUpperCase()));
        if (potentialMatches.length) {
          console.log('Potential matches');
          // 
          console.log(potentialMatches)
          if (tableNameAlias.length > 1) {
            return potentialMatches.map(function (match) {
              return match.value
            });
          } else {
            return [potentialMatches[0].value];
          }
        }
        return ['']

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
          var targetTableAlias;
          if (typeof functionArgument.targetTable === 'string') {
            targetTableAlias = [(functionArgument.targetTable || '').toUpperCase()];
            console.log('Table name');
            console.log(targetTableAlias);
          } else {
            targetTableAlias = functionArgument.targetTable.map(function (table_name) {

              return (table_name || '').toUpperCase();
            })
            console.log('Table name');
            console.log(targetTableAlias);
          }

          // if (KEYS.ALTERNATE_NAMES in func)
          // var tableAliasList = 

          // const isAliased = KEYS.INPUT_TABLE !== targetTableAlias;
          if (aliasedInputsList !== []) {
            isAliasedInputsPopulated = true;
            aliasedInputsList.map((input) => {
              // if (input.name.toUpperCase() === targetTableAlias.toUpperCase()) {
              if (targetTableAlias.includes(input.name.toUpperCase())) {
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
            // let matchingInputs = aliasedInputsList.filter(input => targetTableAlias === input.name.toUpperCase());
            let matchingInputs = aliasedInputsList.filter(input => targetTableAlias.includes(input.name.toUpperCase()));
            if (matchingInputs.length > 0) {
              //console.log('Matching inputs > 0');
              // targetTableName = matchingInputs[0].value;
              // matchingInputs[targetTableAlias.length - 1].value
              targetTableName = matchingInputs.map(function(input) {
                return input.value
              });
            } else {
              //console.log('Matching inputs < 0');
              console.log('Does Matching <= 0 happen?')
              targetTableName = $scope.findTableNameInArgumentsList(argumentsList, targetTableAlias);
            }


          } else {
            //console.log('isNotAliased');
            //console.log(unaliasedInputsList);
            if (unaliasedInputsList.count && unaliasedInputsList.values && unaliasedInputsList.values.length) {
              console.log('Went to unaliased');

              targetTableName = [unaliasedInputsList.values[0]];
              //console.log(targetTableName);
            }

            else {
              targetTableName = $scope.findTableNameInArgumentsList(argumentsList, targetTableAlias);
              console.log('Went to arguments');
              console.log(targetTableName);
            }


          }

        } else if (unaliasedInputsList.values && unaliasedInputsList.values.length > 0) {

          targetTableName = [unaliasedInputsList.values[0]];
          //console.log('This else if');
          //console.log(targetTableName);

        }

        if (!targetTableName || !$scope.inputschemas) {
          //console.log('This happened');
          //console.log(targetTableName);
          //console.log($scope);
          return [];
        }


        if (targetTableName) {
          //console.log('Schemas');
          //console.log($scope.inputschemas[targetTableName]);
          var forReturnInputSchemas = [];
          for (var i = 0; i < targetTableName.length; i++) {
            if (targetTableName[i] in $scope.inputschemas) {
              var currentInputSchemas = $scope.inputschemas[targetTableName[i]]
              currentInputSchemas = currentInputSchemas.map(function (eachInput) {
                return $.extend(eachInput, { "tableName": targetTableName[i] });
              })
              console.log('Current');
              console.log(currentInputSchemas);
              forReturnInputSchemas.push.apply(forReturnInputSchemas, currentInputSchemas)
            }
          }
          console.log('Schema');
          console.log(forReturnInputSchemas)
          return forReturnInputSchemas;

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
        $('.ng-invalid:not(form,.ng-hide)').each((i, x) => invalids.push($(x).parent().prev().text()))

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
        try {

          $('input.teradata-tags').tagsInput({
            onChange: x => $(x).trigger('change'),
            defaultText: 'add param',
            delimiter: SEPARATOR
          });

        } catch (e) { }
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
          .text('Aster Analytics Foundation 7.00\nLearn more about Teradata Aster')
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
          $scope.reloader = true;

        });

      },

      cleanName: function (rawName) {

        return rawName.split('_').join(' ').toLowerCase()

      },

      cleanKind: function (rawKind) {

        return rawKind ? `(${rawKind})` : ''

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
          || !$scope.config.function.arguments.length) return;

        $delay(() => {

          // Re-arrange functions alphabetically.
          if ($scope.choices) {
            $scope.choices = $scope.choices.sort((a, b) => a.name.localeCompare(b.name))
          }

          // Properly bind default arguments.
          let i = 0;
          $scope.config.function.arguments.forEach(argument => {

            // Index each argument for easy access.
            argument.i = i;

            try {

              if (functionMetadata.argument_clauses[i]
                && typeof functionMetadata.argument_clauses[i].defaultValue != 'undefined') {
                argument.value = functionMetadata.argument_clauses[i].defaultValue;
              }

            } catch (e) {

            }

            ++i;

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

        $scope.preprocessMetadata();
        $scope.activateUi();

      },

      /**
       * Initializes this plugin.
       */
      refresh: function (selectedFunction) {

        $scope.getFunctionMetadata(selectedFunction);
        $scope.preprocessMetadata();
        // //console.log($scope);
      }

    })

    $scope.reloader = false;
    $scope.initialLoading = true;
    $scope.initialize();

  });

  angular.module('selectize', [])

    .directive('selectize', ['$parse', '$timeout', function ($parse, $timeout) {
      var NG_OPTIONS_REGEXP = /^\s*([\s\S]+?)(?:\s+as\s+([\s\S]+?))?(?:\s+group\s+by\s+([\s\S]+?))?\s+for\s+(?:([\$\w][\$\w]*)|(?:\(\s*([\$\w][\$\w]*)\s*,\s*([\$\w][\$\w]*)\s*\)))\s+in\s+([\s\S]+?)(?:\s+track\s+by\s+([\s\S]+?))?$/;

      return {
        scope: {
          multiple: '@',
          opts: '@selectize'
        },
        require: '?ngModel',
        link: function (scope, element, attrs, ngModelCtrl) {
          var opts = scope.$parent.$eval(scope.opts) || {};
          var initializing = false;
          var modelUpdate = false;
          var optionsUpdate = false;
          var selectize, newModelValue, newOptions, updateTimer;

          watchModel();

          if (attrs.ngDisabled) {
            watchParentNgDisabled();
          }

          if (!attrs.ngOptions) {
            return;
          }

          var match = attrs.ngOptions.match(NG_OPTIONS_REGEXP);
          var valueName = match[4] || match[6];
          var optionsExpression = match[7];
          var optionsFn = $parse(optionsExpression);
          var displayFn = $parse(match[2] || match[1]);
          var valueFn = $parse(match[2] ? match[1] : valueName);

          watchParentOptions();

          function watchModel() {
            scope.$watchCollection(function () {
              console.log('Watch collection');
              //TO TEST
              // console.log(newModelValue);
              console.log(ngModelCtrl.$modelValue);
              return ngModelCtrl.$modelValue;
            }, function (modelValue) {
              console.log('MODEL EFFIN VALUE');
              console.log(newModelValue);
              console.log(modelValue);
              //experimental code
              if (modelValue != undefined) {
                console.log('Outer if statement');
                if (newModelValue == undefined || modelValue.length < newModelValue.length) {
                  console.log('That if Statement');
                  newModelValue = modelValue;
                  modelUpdate = true;
                  if (!updateTimer) {
                    scheduleUpdate();
                  }

                }
              }


            });
          }

          function watchParentOptions() {
            scope.$parent.$watchCollection(optionsExpression, function (options) {
              console.log('OPTIONS?!?!')
              console.log(options);
              newOptions = options || [];
              optionsUpdate = true;
              if (!updateTimer) {
                scheduleUpdate();
              }
            });
          }

          function watchParentNgDisabled() {
            scope.$parent.$watch(attrs.ngDisabled, function (isDisabled) {
              if (selectize) {
                isDisabled ? selectize.disable() : selectize.enable();
              }
            });
          }

          function scheduleUpdate() {
            console.log('ScheduleUpdate?');
            if (!selectize) {
              if (!initializing) {
                initSelectize();
              }
              return;
            }

            updateTimer = $timeout(function () {
              var model = newModelValue;
              var options = newOptions;
              var selectizeOptions = Object.keys(selectize.options);
              var optionsIsEmpty = selectizeOptions.length === 0 || selectize.options['?'] && selectizeOptions.length === 1;
              if (optionsUpdate) {
                if (!optionsIsEmpty) {
                  selectize.clearOptions();
                }
                selectize.load(function (cb) {
                  cb(options.map(function (option, index) {
                    return {
                      text: getOptionLabel(option),
                      value: index
                    };
                  }));
                });
              }

              if (modelUpdate || optionsUpdate) {
                console.log('MODEL PLS');
                console.log(model);
                var selectedItems = getSelectedItems(model);
                console.log('SELECTED ITEMS?!!?!?!');
                console.log(selectedItems);
                if (scope.multiple || selectedItems.length === 0) {
                  selectize.clear();
                  //clear can set the model to null
                  ngModelCtrl.$setViewValue(model);
                }
                selectedItems.forEach(function (item) {
                  selectize.addItem(item);
                });
                //wait to remove ? to avoid a single select from briefly setting the model to null
                selectize.removeOption('?');

                var $option = selectize.getOption(0);
                if ($option) selectize.setActiveOption($option);
              }

              modelUpdate = optionsUpdate = false;
              updateTimer = null;
            });
          }

          function initSelectize() {
            initializing = true;
            scope.$evalAsync(function () {
              initializing = false;
              element.selectize(opts);
              selectize = element[0].selectize;
              if (attrs.ngOptions) {
                if (scope.multiple) {
                  console.log('Initializing');
                  selectize.on('item_add', onItemAddMultiSelect);
                  selectize.on('item_remove', onItemRemoveMultiSelect);
                } else if (opts.create) {
                  selectize.on('item_add', onItemAddSingleSelect);
                }
              }
            });
          }

          function onItemAddMultiSelect(value, $item) {
            var model = ngModelCtrl.$viewValue || [];
            console.log(model);
            var options = optionsFn(scope.$parent);
            var option = options[value];
            value = option ? getOptionValue(option) : value;
            console.log('Does it get reset here?');
            console.log(model);
            if (model.indexOf(value) === -1) {
              model.push(value);
              console.log('What about here?');
              console.log(model);
              if (!option && opts.create && options.indexOf(value) === -1) {
                options.push(value);
              }
              scope.$evalAsync(function () {
                ngModelCtrl.$setViewValue(model);
              });
            }
          }

          function onItemAddSingleSelect(value, $item) {
            var model = ngModelCtrl.$viewValue;
            var options = optionsFn(scope.$parent);
            var option = options[value];
            console.log('Single happens?');
            value = option ? getOptionValue(option) : value;

            if (model !== value) {
              model = value;

              if (!option && options.indexOf(value) === -1) {
                options.push(value);
              }
              scope.$evalAsync(function () {
                ngModelCtrl.$setViewValue(model);
              });
            }
          }

          function onItemRemoveMultiSelect(value) {
            console.log('What about onItemRemoveMultiSelect');
            var model = ngModelCtrl.$viewValue;
            var options = optionsFn(scope.$parent);
            var option = options[value];
            console.log('First model check');
            console.log(model);
            value = option ? getOptionValue(option) : value;

            var index = model.indexOf(value);
            if (index >= 0) {
              model.splice(index, 1);
              console.log('After splicing');
              console.log(model);
              scope.$evalAsync(function () {
                ngModelCtrl.$setViewValue(model);
                console.log('After set view value');
                console.log(model);
              });
            }
          }

          function getSelectedItems(model) {
            model = angular.isArray(model) ? model : [model] || [];
            console.log('What about getSelectedItems');
            console.log(model);
            if (!attrs.ngOptions) {
              return model.map(function (i) { return selectize.options[i] ? selectize.options[i].value : '' });
            }

            var options = optionsFn(scope.$parent);

            if (!options) {
              return [];
            }

            var selections = options.reduce(function (selected, option, index) {
              var optionValue = getOptionValue(option);
              if (model.indexOf(optionValue) >= 0) {
                selected[optionValue] = index;
              }
              console.log('selected');
              console.log(selected);
              return selected;
            }, {});
            console.log('Selections');
            console.log(selections);
            return Object
              .keys(selections)
              .map(function (key) {
                return selections[key];
              });
          }

          function getOptionValue(option) {
            var optionContext = {};
            optionContext[valueName] = option;
            console.log('What about getOptionValue');
            return valueFn(optionContext);
          }

          function getOptionLabel(option) {
            var optionContext = {};
            optionContext[valueName] = option;
            console.log('What about getOptionLabel');
            return displayFn(optionContext);
          }

          scope.$on('$destroy', function () {
            if (updateTimer) {
              console.log('What about destroy?');
              $timeout.cancel(updateTimer);
            }
          });
        }
      };
    }]);
})(window, document, angular, jQuery);

