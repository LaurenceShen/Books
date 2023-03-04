$(document).ready(function(){
//    推擠main效果
    $('#check').click(function(event){
        $('main').toggleClass('.open');
    });
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
//  書籤結束

});

//  progressbar
const progress = document.querySelector(".progress-done");
const input = document.querySelector(".input");
const maxInput = document.querySelector(".maxInput");
let finalValue = 0;
let max = 0;

function changeWidth(){
    progress.style.width = `${(finalValue / max) * 100}%`;
    progress.innerText = `${Math.ceil((finalValue / max) * 100)}%`;
}

input.addEventListener("keyup", function(){
    finalValue = parseInt(input.value, 10);
    changeWidth();
});

maxInput.addEventListener("keyup", function(){
    max = parseInt(maxInput.value, 10);
    changeWidth();
});