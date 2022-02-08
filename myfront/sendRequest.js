
let msg = ""

function uploadFileData() {
    let file = document.getElementById("customFile").files[0];
    console.log("123", file);
    const rsp = fetch( "http://3.15.51.216:8000/", {
        method: 'POST',
        body: file,
    }).then(response => {
        console.log("File successfully uploaded");
        response.json().then(data => {
            console.log("rsp:", data.todo);
            for (let i = 0; i< data.todo.length;i++) {
                document.getElementById("todolist").innerHTML += data.todo[i].name
                document.getElementById("todolist").innerHTML += "</br>"
            }
        })
    }).catch(err => {
        console.log(err);
    });
}

const onFileChange = (event) => {
    msg = event.target.files[0]
}