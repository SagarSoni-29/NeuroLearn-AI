async function sendChat() {

    const message =
        document.getElementById("chatInput").value;

    const loader =
        document.getElementById("chatLoader");

    const responseBox =
        document.getElementById("chatResponse");

    loader.style.display = "block";

    responseBox.innerHTML = "";

    try{

        const response = await fetch("/chat",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({message})
        });

        const data = await response.json();

        responseBox.innerHTML = data.response;

    }catch(error){

        responseBox.innerHTML =
            "Error generating response.";

    }

    loader.style.display = "none";
}



async function summarizeNotes(){

    const notes =
        document.getElementById("notesInput").value;

    const loader =
        document.getElementById("summaryLoader");

    const responseBox =
        document.getElementById("summaryResponse");

    loader.style.display = "block";

    responseBox.innerHTML = "";

    try{

        const response = await fetch("/summarize",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({notes})
        });

        const data = await response.json();

        responseBox.innerHTML = data.summary;

    }catch(error){

        responseBox.innerHTML =
            "Error generating summary.";

    }

    loader.style.display = "none";
}



async function generateQuiz(){

    const topic =
        document.getElementById("quizTopic").value;

    const loader =
        document.getElementById("quizLoader");

    const responseBox =
        document.getElementById("quizResponse");

    loader.style.display = "block";

    responseBox.innerHTML = "";

    try{

        const response = await fetch("/quiz",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({topic})
        });

        const data = await response.json();

        responseBox.innerHTML = data.quiz;

    }catch(error){

        responseBox.innerHTML =
            "Error generating quiz.";

    }

    loader.style.display = "none";
}



async function uploadDocument(){

    const file =
        document.getElementById("fileInput").files[0];

    const question =
        document.getElementById("docQuestion").value;

    const loader =
        document.getElementById("docLoader");

    const responseBox =
        document.getElementById("docResponse");

    loader.style.display = "block";

    responseBox.innerHTML = "";

    let formData = new FormData();

    formData.append("file",file);
    formData.append("question",question);

    try{

        const response = await fetch("/upload",{
            method:"POST",
            body:formData
        });

        const data = await response.json();

        responseBox.innerHTML = data.answer;

    }catch(error){

        responseBox.innerHTML =
            "Error processing document.";

    }

    loader.style.display = "none";
}