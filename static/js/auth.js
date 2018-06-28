
$(function () {
    var imgCaptcha = $('.img-captcha');
    imgCaptcha.click(function () {
        imgCaptcha.attr('src','/account/img_captcha'+"?random"+Math.random());
    })
});