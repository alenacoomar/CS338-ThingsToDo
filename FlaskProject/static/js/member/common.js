;
let common_ops = {
    buildUrl: function (path, params) {

        let url = "" + path;
        let _param_url = ""
        if (params) {
            Object.keys(params).map(function (k) {
                return [encodeURIComponent(k), encodeURIComponent(params[k])].join("=")
            }).join("&");
            _param_url = "?" + _param_url;

        }

        return url+ _param_url;
    },
    alert:function (msg, cb)
    {
        layer.alert(msg,{
           yes:function (index){
               if(typeof cb == "function")
               {
                   cb();
               }
               layer.close(index);
           }
        });
    }

}