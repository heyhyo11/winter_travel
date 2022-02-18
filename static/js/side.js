$(document).ready(function(){
    $('#side.hide').hide()
    $('.side_container').hide()
    $('#side_show').show()
})

$('#side_show').click(function(){
    $('#side_show').hide()
    $('#side_hide').show()
    $('.side_container').show()
    $('.side_container').css({
        "border-right" : "1px solid #cfd3dc",
        "width":"15%",
    })
    $('.main_wrap').css({
        "width":"85%",
        "margin-left":"20%"
    })
});

$('#side_hide').click(function(){
    $('#side_show').show()
    $('#side_hide').hide()
    $('.side_container').css({
        "border-right" : "None",
        "width":"0%",
    })
    $('.main_wrap').css({
        "width":"100%",
        "margin-left": "0"
    })
    setTimeout(() =>     $('.side_container').hide() , 150);
})