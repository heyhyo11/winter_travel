$(document).ready(function(){
    $('.main_header').slick({
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed : 2000,
        pauseOnHover : true,
        arrows: false,
    });
    $('.hot_card').slick({
        infinite: true,
        centerMode: true,
        centerPadding: '60px',
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed : 2000,
        pauseOnHover : true,

        focusOnSelect: true,
        speed: 300,
        prevArrow : "<i class='far fa-arrow-alt-circle-left fa-3x'</i>",
        nextArrow : "<i class='far fa-arrow-alt-circle-right fa-3x'></i>",
    });
    $('.top100_card').slick({
        infinite: true,
        centerMode: true,
        centerPadding: '60px',
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed : 2000,
        pauseOnHover : true,
        speed: 300,
        prevArrow : "<i class='far fa-arrow-alt-circle-left fa-3x'</i>",
        nextArrow : "<i class='far fa-arrow-alt-circle-right fa-3x'></i>",
    });
    $('.recommand_card').slick({
        infinite: true,
        centerMode: true,
        centerPadding: '60px',
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed : 2000,
        pauseOnHover : true,
        speed: 300,
        prevArrow : "<i class='far fa-arrow-alt-circle-left fa-3x'</i>",
        nextArrow : "<i class='far fa-arrow-alt-circle-right fa-3x'></i>",
    });
})