$(document).ready(function(){
    $('#side.hide').hide()
    $('.side_container').hide()
    $('#side_show').show()
    $('.main_header').slick({
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed : 2500, 
        pauseOnHover : true,
        arrows: false,
    });
    $('.hot_card').slick({
        infinite: true,
        centerMode: true,
        centerPadding: '60px',
        slidesToShow: 3,
        slidesToScroll: 1,
        focusOnSelect: true,
        speed: 600,
        prevArrow : "<i class='far fa-arrow-alt-circle-left fa-3x'</i>",		
        nextArrow : "<i class='far fa-arrow-alt-circle-right fa-3x'></i>",		
    });
    $('.top100_card').slick({
        infinite: true,
        centerMode: true,
        centerPadding: '60px',
        slidesToShow: 3,
        slidesToScroll: 1,
        speed: 600,
        prevArrow : "<i class='far fa-arrow-alt-circle-left fa-3x'</i>",		
        nextArrow : "<i class='far fa-arrow-alt-circle-right fa-3x'></i>",		
    });
    $('.recommand_card').slick({
        infinite: true,
        centerMode: true,
        centerPadding: '60px',
        slidesToShow: 3,
        slidesToScroll: 1,
        speed: 600,
        prevArrow : "<i class='far fa-arrow-alt-circle-left fa-3x'</i>",		
        nextArrow : "<i class='far fa-arrow-alt-circle-right fa-3x'></i>",		
    });
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