(function (window, document, angular, $) {

  const app = angular.module('teradata.module', []);

  app.controller('TeradataController', function ($scope, $timeout) {

    /**
     * A wrapper function that delays execution so that
     * the Angular rendering cycle will have finished before
     * running the given function f.
     */
    const $delay = f => $timeout(f, 500);

    /**
     * Default separator for list-like objects.
     */
    const SEPARATOR = String.fromCharCode(0);

    /**
     * A private variable containing the function metadata.
     */
    let functionMetadata;

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

    $.extend($scope, {

      /**
       * Shows a dialog.
       * 
       * This is for displaying Aster-side errors.
       */
      dialog: function (title, content) {

        $dialog.find('pre').text(content);
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
            $scope.preprocessMetadata();
            $scope.activateTabs();
            $scope.activateMultiTagsInput();
            $scope.activateTooltips();
          })

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
       * Gets the description of the given argument from the static JSON metadata.
       */
      getArgumentDescription: function (selectedFunction, functionArgument) {

        functionArgument = functionArgument.toUpperCase();

        if (!functionMetadata || !functionMetadata.argument_clauses) 
          return '';

        const potentialMatches = functionMetadata.argument_clauses.filter(item =>
          KEYS.ALTERNATE_NAMES in item 
            ? item.alternateNames
                .map(x => x.toUpperCase())
                .includes(functionArgument)
            : item.name.toUpperCase() === functionArgument
        );
        
        return potentialMatches.length > 0 ? potentialMatches[0].description : '';

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

      findTableNameInArgumentsList: function(argumentsList) {

        let potentialMatches = argumentsList
          .filter(arg => [KEYS.INPUT_TABLE, KEYS.INPUT_TABLE_ALTERNATIVE].includes(arg.name.toUpperCase()));
        if (potentialMatches.length)
            return potentialMatches[0].value;
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
        
        if (hasTargetTable) {

          const targetTableAlias = functionArgument.targetTable.toUpperCase();
          const isAliased = KEYS.INPUT_TABLE !== targetTableAlias;

          if (isAliased) {

            let matchingInputs = aliasedInputsList.filter(input => targetTableAlias === input.name.toUpperCase());
            if (matchingInputs.length > 0)
              targetTableName = matchingInputs[0].value;
            else
              targetTableName = $scope.findTableNameInArgumentsList(argumentsList);

          } else {

            if (unaliasedInputsList.count && unaliasedInputsList.values && unaliasedInputsList.values.length)
              targetTableName = unaliasedInputsList.values[0];
            else
              targetTableName = $scope.findTableNameInArgumentsList(argumentsList);

          }

        } else if (unaliasedInputsList.values && unaliasedInputsList.values.length > 0) {
          
          targetTableName = unaliasedInputsList.values[0]
        
        }

        if (!targetTableName || !$scope.inputschemas)
          return [];

        if (targetTableName && targetTableName in $scope.inputschemas)
          return $scope.inputschemas[targetTableName];

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

        runFunction()

        $scope.listenForResults(function () {

          const $results = $('.alert:not(.ng-hide):not(.messenger-message)')

          if ($results.length === 0) return false;

          try {

            const title = $results.get(0).classList[1].split('-')[1]

            if (!title || title === 'info')
              return false

            const result = $results.find('h4').text()
            $results.remove()
            $scope.dialog(title, result)

            return true

          } catch (e) {}
          
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
      communicateWithBackend: function (f) {

        $scope.callPythonDo({}).then(
          data => $.extend($scope, data),
          () => {}
        );

      },

      /**
       * Activates the tabbing functionality of this recipe.
       */
      activateTabs: function () {
        try {
          $('#tabs').tabs('destroy')
        } catch (e) {}
        $('#tabs').tabs();
      },

      /**
       * Activates the informative tooltips of each input control.
       * Hijacks each tagsInput element so that it properly displays tooltips as well.
       */
      activateTooltips: function () {

        $('#main-container').tooltip();
        $('.tagsinput').each((i, x) => {

          const original = $(x).prev().data('original-title')
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

        } catch (e) {}
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
          .text('Learn more about Teradata Aster')
          .css('color', 'orange')
          .attr('target', '_blank');
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
          $scope.activateTooltips();
          $scope.activateValidation();

        });

      },

      cleanName: function(rawName) {

        return rawName.split('_').join(' ').toLowerCase()

      },

      /**
       * Preprocess function metadata.
       */
      preprocessMetadata: function() {

        if (
          !functionMetadata
          || !$scope.config
          || !$scope.config.function
          || !$scope.config.function.arguments 
          || !$scope.config.function.arguments.length) return;

        $delay(() => {

          // Re-arrange argument order.
          $scope.config.function.arguments = [
            ...$scope.config.function.arguments.filter(x => x.datatype === 'TABLE_NAME'),
            ...$scope.config.function.arguments.filter(x => x.datatype !== 'TABLE_NAME'),
          ]

          // Properly bind default arguments.
          let i = 0;
          $scope.config.function.arguments.forEach(argument => {

            if (typeof functionMetadata.argument_clauses[i].defaultValue != 'undefined') {
              argument.value = functionMetadata.argument_clauses[i].defaultValue;
            }

            ++i;

          });

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
      refresh: function(selectedFunction) {

        $scope.getFunctionMetadata(selectedFunction);
        $scope.preprocessMetadata();

      }

    })

    $scope.initialize();

  });

})(window, document, angular, jQuery);