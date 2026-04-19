async function issueFile() {
    const file = document.getElementById("issueFile").files[0];
    if (!file) return alert("Select file");

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/issue", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("result").innerHTML =
        `STATUS: ${data.status}\nHASH: ${data.hash}`;
}

async function verifyFile() {
    const file = document.getElementById("verifyFile").files[0];
    if (!file) return alert("Select file");

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/verify", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("result").innerHTML =
        `FINAL: ${data.final}\nVOTES: ${JSON.stringify(data.votes)}`;
}