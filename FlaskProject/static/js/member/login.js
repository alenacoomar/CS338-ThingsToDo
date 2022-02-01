;
let member_login_ops = {
    init:function (){
        this.eventBind();
    },
    eventBind:function ()
    {
        $(".login-wrap .do-login").click(function () {
            let btn_target = $(this);
            if(btn_target.hasClass("disabled"))
            {
                common_ops.alert("It is processing, do not click again");
                return;
            }
            var login_name = $(".login-wrap input[name = login_name]").val();
            var login_pwd = $(".login-wrap input[name = login_pwd]").val();
            console.log(login_name);
            console.log(login_pwd)
            if(login_name == undefined || login_name.length < 1){
                common_ops.alert("The username is incorrect");
                return;
            }
            if(login_pwd == undefined || login_pwd.length < 8)
            {
                common_ops.alert("the password is not corrrect");
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url:common_ops.buildUrl("/member/login"),
                type:"POST",
                data:{
                    login_name:login_name,
                    login_pwd:login_pwd
                },
                dataType:"json",
                success:function (res) {
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
}

$(document).ready(function ()
    {
        member_login_ops.init();
    }
);