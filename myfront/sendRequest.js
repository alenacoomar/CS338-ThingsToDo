let meetingID = ""
let returnTasks = []

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

                    returnTasks.push([data.todo[i].name, data.todo[i].txt[0]])
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
    meetingID = document.getElementById("exampleInputPassword1").value;
    window.open(`http://localhost:8000/meetingid/${meetingID}`, "_blank");
}

function submitMail() {
    const email = document.getElementById('exampleInputEmail1').value;
    let tasks = ""
    Object.values(returnTasks).map((value) => {
        tasks += value[0] + ": " + value[1] + "%0D%0A"
    })
    const subject = `Tasks for meeting ${meetingID}`
    const url = `mailto:${email}?subject=${subject}&body=${tasks}`;
    window.open(url);
}

$(document).ready(function(){
    $("#file").click(function () {
        $("#myModalLabel").text("upload the transcript manually");
        $('#myModal').modal();
        document.getElementById("modal-body").innerHTML = '<div><label class="form-label" for="customFile">\
        <h2 style="text-align: center;">Upload the transcript file here (.vtt)</h1></label>\
        <input type="file" class="form-control" id="customFile" accept=".vtt"/><br>'
        document.getElementById("modal-footer").innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span>close</button>\
        <button type="button" id="btn_submit" class="btn btn-primary" data-dismiss="modal" onclick="uploadFileData()"><span class="glyphicon glyphicon-floppy-disk" aria-hidden="true" ></span>Submit</button>';
    });
    $("#zoom").click(function(){
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


