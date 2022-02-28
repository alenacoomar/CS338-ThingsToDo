function uploadFileData() {
    let file = document.getElementById("customFile").files[0];
    const reader = new FileReader();
    let res = ""
    let table =  document.getElementById("todolist");
    reader.readAsText(file, "UTF-8");
    reader.onload = function() {
        res = reader.result
        table.innerHTML = "<tr>" +
                "<td style=\"font-size: large;\">Name</td>" +
                "<td style=\"font-size: large;\">Things to do</td>" +
                "</tr>" + "<td style=\"font-size: large;\" > loading... </td>";
        const rsp = fetch( "http://3.15.51.216:8000/", {
            method: 'POST',
            body: res,
        }).then(response => {
            response.json().then(data => {
                let str = "";
                for (let i = 0; i< data.todo.length; i++) {
                    str += "<tr>";
                        str += "<td>" + data.todo[i].name + "</td>";
                        str += "<td>" + data.todo[i].txt[0] + "</td>";
                    str += "</tr>";
                }
                table.innerHTML = "<tr>" + "<td style=\"font-size: large;\">Name</td>" +
                    "<td style=\"font-size: large;\">Things to do</td>" + "</tr>" +str;
            })
        }).catch(err => {
            console.log(err);
        });
    };
}

function Submit() {
    meeting = document.querySelector("#exampleInputPassword1").value;
    //window.open(`http://localhost:8000/meetingid/${meeting}`, "_blank");
    window.location.href = "https://zoom.us/oauth/authorize?response_type=code&client_id=mBr4CQ7wR8KlxZcISGMsyA&redirect_uri=http://localhost:8000";
    fetch(`http://localhost:8000/transcript/${meeting}`)
        .then(res => {
            console.log(res)
        })
}

$(document).ready(function(){
    $("#file").click(function () {
        console.log("click")
        $("#myModalLabel").text("upload the transcript manually");
        $('#myModal').modal();
        document.getElementById("modal-body").innerHTML = '<div><label class="form-label" for="customFile">\
        <h2 style="text-align: center;">Upload the transcript file here (.vtt)</h1></label>\
        <input type="file" class="form-control" id="customFile" accept=".vtt"/><br>'
        document.getElementById("modal-footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span>close</button>\
        <button type="button" id="btn_submit" class="btn btn-primary" data-dismiss="modal" onclick="uploadFileData()"><span class="glyphicon glyphicon-floppy-disk" aria-hidden="true" ></span>Submit</button>';
    
    });
    $("#zoom").click(function(){
        console.log("click")
        $("#myModalLabel").text("upload the transcript by searching your meeting Id");
        $('#myModal').modal();
        let str = '<h2>Search for the meeting</h2><div><form>\
                <div class="form-group">\
                    <label for="exampleInputPassword1">Meeting Id</label>\
                    <input type="text" class="form-control" id="exampleInputPassword1" placeholder="Meeting ID">\
                  </div>';
        document.getElementById("modal-body").innerHTML = str;
        document.getElementById("modal-footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span>close</button>\
        <button type="button" id="btn_submit" class="btn btn-primary" data-dismiss="modal" onclick="Submit()"><span class="glyphicon glyphicon-floppy-disk" aria-hidden="true" ></span>Submit</button>';
    });
}
);