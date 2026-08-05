async function analyzeWebsite() {

    const url = document.getElementById("url").value.trim();

    const loading = document.getElementById("loading");

    const result = document.getElementById("result");

    if (url === "") {
        alert("Please enter a website URL.");
        return;
    }

    loading.innerHTML = "🔍 Analyzing website...";
    result.style.display = "none";

    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: url
            })

        });

        const data = await response.json();

        loading.innerHTML = "";

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("status").innerHTML = data.status;
        document.getElementById("time").innerHTML = data.response_time;
        document.getElementById("title").innerHTML = data.title;
        document.getElementById("meta").innerHTML = data.meta_description;
        document.getElementById("h1").innerHTML = data.h1_count;
        document.getElementById("alt").innerHTML = data.images_without_alt;
        document.getElementById("words").innerHTML = data.word_count;

        result.style.display = "block";

    }

    catch (error) {

        loading.innerHTML = "";

        alert("Unable to analyze the website.");

        console.log(error);

    }

}