
function uploadFileData() {
    let file = document.getElementById("customFile").files[0];
    const reader = new FileReader();
    let res = ""
    reader.readAsText(file, "UTF-8");
    reader.onload = function() {
        res = reader.result

        const rsp = fetch( "http://3.15.51.216:8000/", {
            method: 'POST',
            body: res,
        }).then(response => {
            response.json().then(data => {
                let table =  document.getElementById("todolist");
                let str = "";
                for (let i = 0; i< data.todo.length; i++) {
                    str += "<tr>";
                        str += "<td>" + data.todo[i].name + "</td>";
                        str += "<td>" + data.todo[i].txt[0] + "</td>";
                    str += "</tr>";
                }
                table.innerHTML += str;
            })
        }).catch(err => {
            console.log(err);
        });
    };
}
