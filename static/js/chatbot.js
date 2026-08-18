const queryInput = document.getElementById("query");
queryInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        askQuestion();   // Same function as clicking Send
    }
})

async function askQuestion(){

    let query = document.getElementById("query").value;
    document.getElementById("query").value = "";
    console.log("Inside RAG");


    addMessage(query,"user");

    let response = await fetch("http://localhost:8000/botchat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
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