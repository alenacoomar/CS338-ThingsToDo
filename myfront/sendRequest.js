
function uploadFileData() {
    let file = document.getElementById("customFile").files[0];
    console.log("123", file);
    const rsp = fetch( "http://3.15.51.216:8000/", {
        method: 'POST',
        body: file,
    }).then(response => {
        response.json().then(data => {
            let table =  document.getElementById("todolist");
            let str = "";
            for (let i = 0; i< data.todo.length; i++) {
                str += "<tr>";
                    str += "<td>" + "name" + "</td>";
                    str += "<td>" + data.todo[i].name + "</td>";
                str += "</tr>";
            }
            table.innerHTML += str;
        })
    }).catch(err => {
        console.log(err);
    });
}
