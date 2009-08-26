function add_interaction() {
    var url = $(this).attr("href");
    $("#interaction-controls").hide();
    $("#add-interaction-wrapper").slideDown();
    $("#add-interaction-wrapper").load(url, null, function(){
        $("#add-interaction-form").submit(interaction_save);
    });
    return false;
}

function interaction_save () {
    var item = $(this).parent();
    var url  = $("#add-interaction-form").attr("action");
    var data = $("#add-interaction-form").serialize();
    $.post(url, data, function(result){
            $("#add-interaction-wrapper").html(result);
        });
    return false;
}


$(document).ready(function() {  
    $(".add-interaction").click(add_interaction);
    $("#add-interaction-wrapper").hide();
});
