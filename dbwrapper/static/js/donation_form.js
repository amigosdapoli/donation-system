$(document).ready(function(){
    // Masks
    $('.phone_with_ddd').mask('(00) 00000-0000');
    $('.cpf').mask('000.000.000-00', {reverse: true});
    $('.money').mask('000.000.000.000.000,00', {reverse: true});

    // Conditional fields
    $('input[name=is_recurring]').on('change', function() {
      if ( $('#rad2').is(':checked'))
      {
        $("#id_installments").show();
      }
      else
      {
        $("#id_installments").hide();
      }
    });

    $('#id_course_taken').on('change', function() {
      if ( this.selectedIndex != '0' && this.selectedIndex != '1')
      {
        $("#id_course_year").show();
      }
      else
      {
        $("#id_course_year").hide();
      }
    });
});