$(document).ready(function(){

    $('a.likeIcon').on('click', function(event){
            event.stopPropagation();
            event.stopImmediatePropagation();
            let like_count = $(this).siblings();
            let url = $(this).attr("data-url");


        $.ajax({
                type: "GET",
                url: url,
                success: function(response){
                    updated_like_count = parseInt($(this).html()) + parseInt(response.like_change);
                    $(this).html(updated_like_count);
                },
                error: function(){
                    console.log("error");
                }
        });
    });
});