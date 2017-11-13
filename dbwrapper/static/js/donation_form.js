$(document).ready(function(){
    // Masks
    $('.phone_with_ddd').mask('(00) 00000-0000');
    $('.cpf').mask('000.000.000-00');
    $('.money').mask('000.000.000.000.000,00', {reverse: true});
    $('.card_number').mask('0000 0000 0000 0000');
    $('.expiry_date_month').mask('00');
    $('.expiry_date_year').mask('00');


    // Conditional fields
    $('input[name=is_recurring]').on('change', function() {
      if ( $('#rad2').is(':checked'))
      {
        $("#id_installments").show();
        $(".id_installments_select").get(0).selectedIndex = 1;
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