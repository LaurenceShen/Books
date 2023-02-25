$(document).ready(function(){
//    popup的書籤
    $(".popup-btn").click(function() {
        var href = $(this).attr("href")
        $(href).show(250);
        $(href).children$("popup-box").removeClass("transform-out").addClass("transform-in");
        e.preventDefault();
    });
    
    $(".popup-close").click(function() {
        closeWindow();
    });
    // $(".popup-wrap").click(function(){
    //   closeWindow();
    // })
    function closeWindow(){
        $(".popup-wrap").hide(200);
        $(".popup-box").removeClass("transform-in").addClass("transform-out");
        event.preventDefault();
    }
//    書籤結束
});