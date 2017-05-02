const app = angular.module('teradata.module', []);

app.controller('TeradataController', function ($scope) {

  $scope.callPythonDo({}).then(
    data => {
      $scope.choices = data.choices;
      $scope.schema = data.schema;
      console.log(data);

      // setTimeout(() => {
      //   const $elem = $('#main-container select:first')
      //   $elem.selectize({
      //     dropdownParent: 'body'
      //   })
      //   $elem[0].selectize.on('change', e => {
      //     setTimeout(() => $('#main-container select:not(.selectized)').selectize({
      //       dropdownParent: 'body'
      //     }), 100)
      //   })
      // });

    },
    data => {
      $scope.choices = [];
      $scope.schema = [];
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

    console.log('updated')

  });

});