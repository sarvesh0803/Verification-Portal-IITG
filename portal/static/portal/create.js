	$('#uta').on('change',function(){
     var selection = $(this).val();
    switch(selection){
    case 'dept_body':
    $('#deptbody').show()
    $("#hostel").hide()
   	break;
   	case 'hostel_team':
    $('#hostel').show()
    $('#deptbody').hide()
   	break;
    default:
    $('#hostel').hide()
    $('#deptbody').hide()
    }
});