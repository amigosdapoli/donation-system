$(document).ready(function(){
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