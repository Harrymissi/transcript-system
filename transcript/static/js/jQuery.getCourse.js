(function ($) {
     $(".use-address").click(function() {
    var $item = $(this).closest("tr")
                       .find(".nr")
                       .text();

    $("#resultas").value($item);
   });
})(jquery);