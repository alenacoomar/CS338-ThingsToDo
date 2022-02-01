;
let member_sign_up = {
    init:function (){
        this.eventBind();
    },
    eventBind:function () {
        $(".reg_wrap .do-reg").click(function () {
            let btn_target = $(this);
            if(btn_target.hasClass("disabled"))
            {
                return;
            }
            let login_name = $(".reg_wrap input[name=login_name]").val();
            let login_pwd1 = $(".reg_wrap input[name= login_pwd1]").val();
            let login_pwd2 = $(".reg_wrap input[name =  login_pwd2]").val();
            if(login_name == undefined || login_name.length < 1){
                common_ops.alert("The username is incorrect");
                return;
            }
            if(login_pwd1 == undefined || login_pwd1.length < 8)
            {
                common_ops.alert("the password cannot be empty or shorter than 8 characters");
                return;
            }

            if(login_pwd2 == undefined || login_pwd2 != login_pwd1)
            {
                common_ops.alert("two passwords are not identical")
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url:common_ops.buildUrl("/member/signup"),
                type:"POST",
                data:{
                    login_name:login_name,
                    login_pwd1:login_pwd1,
                    login_pwd2:login_pwd2,
                },
                dataType:'json',
                success:function (res)
                {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code === 200 ){
                        callback = function(){
                            window.location.href = common_ops.buildUrl( "/" );
                        };
                    }
                    common_ops.alert( res.msg,callback );
                }

            });
        });
    }

};

$(document).ready(function (){
    member_sign_up.init();
});