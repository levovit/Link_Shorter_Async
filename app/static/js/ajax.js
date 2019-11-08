"use strict";

 $(function() {
     $('#submitButton').click(function() {
         $.ajax({
             type: "POST",
             url: "/short",
             data: JSON.stringify({'url' : $('#url').val()}),
             success: returnSuccess,
             error: returnError,
             dataType: "json",
             contentType: "application/json",
         });
     });
});

function returnSuccess(data, textStatus, jqXHR) {
    if(data.url) {
        $('#url-result').text(data.url);
        $('#url').val("");
        $("a").attr("href", data.url);
    } else {
        $('#url-result').text("Please enter a URL!");
    }
}

function returnError(jqXHR, textStatus, errorThrown ) {
    console.log(errorThrown);
    console.log(textStatus);
    console.log(jqXHR);
    console.log(typeof errorThrown);
    $('#url-result').text(jqXHR.responseJSON.error.message);
    $('#url').val("");
    $("a").attr("href", "#");

}