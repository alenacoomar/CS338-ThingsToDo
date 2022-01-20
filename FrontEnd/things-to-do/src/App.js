import './App.css';
import {useState} from "react";

const targetURL = "http://localhost:8000/"

function App() {
    const [msg, setMsg] = useState("")
    const [file, setF] = useState()

    const onFileChange = (event) => {
        setF(event.target.files[0])
    }

    const uploadFileData = (event) => {
        event.preventDefault();
        setMsg("")

        const rsp = fetch(targetURL, {
            method: 'POST',
            body: file,
        }).then(response => {
            setMsg("File successfully uploaded");
            response.json().then(data => {
                console.log("rsp:", data);
            })
        }).catch(err => {
            console.log(err);
            setMsg("error! check log");
        });
    }

    return (
        <div>
            <h1>File Upload Example using React</h1>
            <h3>Upload a File</h3>
            <h4>{msg}</h4>
            <input onChange={onFileChange} type="file"/>
            <button disabled={!file} onClick={uploadFileData}>Upload</button>
        </div>
    );
}

export default App;
