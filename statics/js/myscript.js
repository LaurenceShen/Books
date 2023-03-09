$(document).ready(function(){
//    彈跳視窗的功能
    $(".popup-btn").click(function() {
        var href = $(this).attr("href")
        $(href).show(250);
        $(href).children$("popup-box").removeClass("transform-out").addClass("transform-in");
        e.preventDefault();
    });
    
    $(".popup-close").click(function() {
        closeWindow();
    });
    
    function closeWindow(){
        $(".popup-wrap").hide(200);
        $(".popup-box").removeClass("transform-in").addClass("transform-out");
        event.preventDefault();
    }


    // 讓progress range可以顯示
    $(".rangeTxt").html($("#bookprogress").val()); // 在 #rangeTxt 顯示 #myRange 的 bar 值
    $("#bookprogress").on("input", function(){ // 當輸入 input 時執行以下動作
    $(".rangeTxt").html($(this).val()); // 將本數值顯示在 #rangeTxt 上
    });
    
});



  