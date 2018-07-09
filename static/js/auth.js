
//点击切换图片验证码
$(function () {
    var imgCaptcha = $('.img-captcha');
    imgCaptcha.click(function () {
        imgCaptcha.attr('src','/account/img_captcha'+"?random"+Math.random());
    })
});


//点击发送短信验证码
$(function () {
    var smsCaptcha = $('.sms-captcha-btn');
    function send_sms() {
        var telephone = $('input[name="telephone"]').val();
        console.log('coming...');
        $.get({
            'url': '/account/sms_captcha/',
            "data":{'telephone': telephone,
            },

            'success': function (result) {
                console.log(telephone)
                var count = 10;
                smsCaptcha.addClass('disabled');
                smsCaptcha.unbind('click');
                var timer = setInterval(function () {
                    smsCaptcha.text(count);
                    count--;
                    if(count <= 0){
                        clearInterval(timer);
                        smsCaptcha.text('发送验证码');
                        smsCaptcha.removeClass('disabled');
                        smsCaptcha.click(send_sms);
                    }
                },1000);
            },
            'fail': function (error) {
                console.log(error);
            },
        });
    }
    smsCaptcha.click(send_sms);
});