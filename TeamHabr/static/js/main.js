function openForm() {
    document.getElementById("commentsForm").style.display = "block";
    document.getElementById("open-button").style.display = "none";
}

function closeForm() {
    document.getElementById("commentsForm").style.display = "none";
    document.getElementById("open-button").style.display = "block";
}

function addReview(name, id) {
        document.getElementById("contactparent").value = id;
        document.getElementById("id_text").innerText = `${name}, `
        document.getElementById("commentsForm").style.display = "block";
        document.getElementById("open-button").style.display = "none";
    }

function goBack() {
  window.history.back();
}