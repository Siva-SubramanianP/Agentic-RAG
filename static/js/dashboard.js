const queryInput = document.getElementById("query");
queryInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        askRAGQuestion();   // Same function as clicking Send
    }
})

async function uploadDocuments() {

    let fileInput = document.getElementById("files");
    let files = fileInput.files;

    if (files.length === 0) {
        document.getElementById("uploadStatus").innerHTML = "Please select files";
        return;
    }

    let formData = new FormData();

    for (let file of files) {
        formData.append("documents", file);
    }

    document.getElementById("uploadStatus").innerHTML = "Uploading...";

    let response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData
    });

    let result = await response.json();
    if(result.message === "Document uploaded") {
        alert("Document uploaded Succesfully")
    }
    else{
        alert(
            result.message +
            "\nSuccess Count: " + (result.uploaded - result.failed) +
            "\nFailed Count: " + result.failed
        );
    }
    document.getElementById("uploadStatus").innerHTML = "";
    

    
    fileInput.value = "";
}

async function askRAGQuestion(){

    let query = document.getElementById("query").value;
    document.getElementById("query").value = "";
    addMessage(query,"user");
    console.log("Inside RAG");

    let response =await fetch("http://localhost:8000/query",{
        method:"POST",
        headers:{
        "Content-Type":
        "application/json"
        },
        body:JSON.stringify({
            question:query
        })

    });
    let data = await response.json();

    typeMessage(data.answer,"bot");

}

function typeMessage(text,type){

    const chat = document.getElementById("chatBox");

    const div = document.createElement("div");
    div.className = type;

    chat.appendChild(div);

    let words = text.split(" ");
    let index = 0;

    let interval = setInterval(()=>{

        div.innerHTML += words[index] + " ";

        index++;

        chat.scrollTop = chat.scrollHeight;

        if(index >= words.length){
            clearInterval(interval);
        }

    },100);
}

function addMessage(text,type){
    if (text.trim() !== "") {
        const chat = document.getElementById("chatBox");
        const div = document.createElement("div");

        div.className = type;
        div.innerHTML = text;

        chat.appendChild(div);
        chat.scrollTop = chat.scrollHeight;
    }
}

function logout(){

    localStorage.removeItem("user");
    window.location.href = "/";

}

function dashboard(){
    window.location.href = "/dashboard"
}

function Normalchat(){
    window.location.href = "/chat"
}