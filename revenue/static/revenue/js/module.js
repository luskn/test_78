$(".refresh").click(function() {
    console.log('click');
    $.get("/sales/", function(data) {
        $(".content").html(data);
    }, "html");
});