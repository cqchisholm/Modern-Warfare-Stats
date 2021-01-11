function compare() {
    window.location.href = "/compare";
}

function hide_rows() {
    var div = document.getElementsByClassName("friends_rows");
    var i;
    for (i = 0; i < div.length; i++) {
        if (div[i].style.visibility !== "hidden") {
            div[i].style.visibility = "hidden";
        }
        else {
            div[i].style.visibility = "visible";
        }
    }
}
