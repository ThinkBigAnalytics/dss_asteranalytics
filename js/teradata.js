(function (window, document, angular, $) {

  const app = angular.module('teradata.module', []);

  app.controller('TeradataController', function ($scope, $timeout) {

    /**
     * A wrapper function that delays execution so that
     * the Angular rendering cycle will have finished before
     * running the given function f.
     */
    const $delay = f => $timeout(f, 500)

    /**
     * A private variable containing the function metadata.
     */
    let functionMetadata;

    /**
     * A private variable containing the function to run the given recipe.
     */
    let runFunction;

    $.extend($scope, {

      dialog: function (title, content) {
        $('#dialog').attr('title', title);
        $('#dialog > pre').text(content);
        $('#dialog').dialog({
          modal: true,
          width: '33%',
          minHeight: 250,
        });
      },

      validationDialog: function (html) {
        $('#dialog-validation > div').html(html);
        $('#dialog-validation').dialog({
          modal: true,
          width: '33%',
          minHeight: 250,
        });
      },


      getFunctionMetadata: function (selectedFunction) {

        if (typeof selectedFunction === 'undefined') {
          return;
        }

        $http
          .get(`/plugins/AsterAnalytics/resource/data/${selectedFunction}.json`)
          .success(data => {
            functionMetadata = data
            $scope.activateTabs();
            $scope.activateMultiTagsInput();
            $scope.activateTooltips();
          })

      },

      getFunctionDescription: function () {
        return (functionMetadata && 'long_description' in functionMetadata) ?
          functionMetadata.long_description :
          '';
      },

      getArgumentDescription: function (selectedFunction, functionArgument) {
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
      },

      getSchemaOfUnaliasedInputs: function (unaliasedInputsList) {
        if (unaliasedInputsList.values && unaliasedInputsList.values.length > 0) {
          let targetTableName = unaliasedInputsList.values[0];
          if (targetTableName && $scope.inputschemas && targetTableName in $scope.inputschemas) {
            return $scope.inputschemas[targetTableName];
          }
        }
        return [];
      },

      getSchema: function (functionArgument, aliasedInputsList, unaliasedInputsList, argumentsList) {

        let targetTableName = ''
        if ('targetTable' in functionArgument) {
          let targetTableAlias = functionArgument.targetTable;
          if ('INPUTTABLE' === targetTableAlias.toUpperCase()) {
            if (unaliasedInputsList.count > 0) {
              if (unaliasedInputsList.values && unaliasedInputsList.values.length > 0) {
                targetTableName = unaliasedInputsList.values[0];
              }
            } else {
              let inputtableargument = (argumentsList || [])
                .filter(arg => 'INPUTTABLE' === arg.name.toUpperCase() || 'INPUT_TABLE' === arg.name.toUpperCase());
              if (inputtableargument.length > 0) {
                targetTableName = inputtableargument[0].value;
              }
            }
          } else {
            let inputslist = (aliasedInputsList || []).filter(n => targetTableAlias.toUpperCase() === n.name.toUpperCase());
            if (inputslist.length > 0) {
              targetTableName = inputslist[0].value;
            } else {
              let inputtableargument = (argumentsList || []).filter(arg => targetTableAlias.toUpperCase() === arg.name.toUpperCase() || 'INPUT_TABLE' === arg.name.toUpperCase());
              if (inputtableargument.length > 0) {
                targetTableName = inputtableargument[0].value;
              }
            }
          }
        } else if (unaliasedInputsList.values && unaliasedInputsList.values.length > 0) {
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

      // temporary code to not show partition and order by fields when there are no unaliased input dataset
      shouldShowPartitionOrderFields: function (unaliasedInputsList) {
        return unaliasedInputsList && unaliasedInputsList.count > 0;
      },

      isArgumentOutputTable: function (functionArgument) {
        if (functionMetadata && functionMetadata.argument_clauses) {
          const functionargumententry = functionMetadata.argument_clauses.filter(function (item) {
            if ('alternateNames' in item) {
              return item.alternateNames
                .map(x => x.toUpperCase())
                .indexOf(functionArgument.name.toUpperCase()) > -1;
            } else {
              return item.name.toUpperCase() === functionArgument.name.toUpperCase();
            }
          });
          if (functionargumententry && functionargumententry.length > 0) {
            return functionargumententry[0].isOutputTable;
          }
        }
        return false;
      },

      hasRequiredArguments: function () {
        if (!$scope.config.function.arguments || !$scope.config.function.arguments.length) {
          return false
        }

        return $scope.config.function.arguments.filter(x => x.isRequired).length > 0
      },

      hasOptionalArguments: function () {
        let hasOptionalArgument = $scope.config.function.arguments &&
          $scope.config.function.arguments.length &&
          ($scope.config.function.arguments.filter(x => !x.isRequired).length > 0);

        let hasOptionalInputTable = $scope.config.function.required_input &&
          $scope.config.function.required_input.length &&
          ($scope.config.function.required_input.filter(x => !x.isRequired).length > 0);

        return hasOptionalInputTable || hasOptionalArgument;
      },

      listenForResults: function (f) {
        const listener = setInterval(() => {
          if ($('.recipe-editor-job-result').length && f()) {
            clearInterval(listener);
            $('.recipe-editor-job-result').remove();
          }
            
        }, 50)
      },

      validate: function() {

        const invalids = []
        $('.ng-invalid:not(form,.ng-hide)').each((i,x) => invalids.push($(x).parent().prev().text()))

        if (invalids.length) {
          $scope.validationDialog(`Please amend the following fields: <ul>${invalids.map(x => `<li>${x}</li>`).join('')}</ul>`)
          return false
        }

        return true

      },

      runThenListen: function () {

        if (!$scope.validate()) return;

        runFunction()
        $scope.listenForResults(function () {

          if ($('.alert:not(.ng-hide)').length === 0) return false;

          const title = $('.alert:not(.ng-hide)')[0].className.split(' ')[1].split('-')[1]

          if (!title || title === 'info') {
            return false
          }

          const result = $('.alert:not(.ng-hide) > h4').text()
          const detailsUrl = $('.alert:not(.ng-hide) a[href]').attr('href')
          $('.alert:not(.ng-hide)').remove()

          $scope.dialog(title, result)

          return true

        })

      },

      initializeBootstrap: function () {
        if ($.fn.button && $.fn.button.noConflict)
          $.fn.bootstrapBtn = $.fn.button.noConflict()
      },

      communicateWithBackend: function () {

        $scope.callPythonDo({}).then(
          data => $.extend($scope, data),
          () => {}
        );

      },

      activateTabs: function () {
        try {
          $('#tabs').tabs('destroy')
        } catch (e) {}
        $('#tabs').tabs();
      },

      activateTooltips: function () {

        $('#main-container').tooltip();
        $('.tagsinput').each((i, x) => {
          const original = $(x).prev().data('original-title')
          const title = original 
            ? (original + '<br><br><b>(Press ENTER to add to list)</b>') 
            : '<b>(Press ENTER to add to list)</b>'
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

      activateMultiTagsInput: function () {
        try {
          $('input.teradata-tags').tagsInput({
            'onChange': x => $(x).trigger('change'),
            'defaultText': 'add param',
          });
        } catch (e) {}
      },

      activateValidation: function () {

        runFunction = $._data($('.btn-run-main').get(0), 'events').click[0].handler.bind($('.btn-run-main').get(0));
        $('.btn-run-main').off('click');
        $('.btn-run-main').click(e => $scope.runThenListen());

      },

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

      initialize: function (selectedFunction) {

        $scope.communicateWithBackend();
        $scope.getFunctionMetadata(selectedFunction);

        $scope.activateUi();

      }

    })

  });

})(window, document, angular, jQuery);