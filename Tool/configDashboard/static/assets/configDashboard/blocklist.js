function alert_show() {
    alert("Please, mind that by selecting this option your experience might be hindered!")
}

function make_active(id) {
    ids = ['dashboard', 'blocklist_settings', 'about']

    ids.forEach(removeActiveTag);

    function removeActiveTag(value, index, array) {
        document.getElementById(value).classList.remove("active");
    }

    document.getElementById(id).classList.add("active")
}

function add_row(text) {
    //add new element in table
    var table = document.getElementById("table-body");
    var row = table.insertRow(-1);
    row.setAttribute("id",text);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.innerHTML = text;
    cell2.innerHTML = "<button class='btn btn-link' id='" + text + "_delete' onclick='deleteRow(this.id)'><i class='tim-icons icon-trash-simple' style='color: #e14eca; font: normal normal normal 1.5em/1 \x22Nucleo\x22;'></i></button>";

    //send POST with domain to backend
    var jsonData = JSON.stringify({ "csrfmiddlewaretoken": getCookie('csrftoken'), "domain": text });

    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        dataType: "json",
        data: jsonData,
        contentType: "application/json"
    });
}

$(function () {
    $("#close_modal").click(function () {
        //get the domain that should be blocked
        var text = $('#inlineFormInputGroup').val();
        console.log(text)

        add_row(text)

        $("#searchModal").modal("hide");
    });
});

function deleteRow(rowid_delete) {   
    //get domain name to delete
    var rowid = rowid_delete.slice(0, -7)

    //send domain to delete to backend
    var jsonData = JSON.stringify({ "csrfmiddlewaretoken": getCookie('csrftoken'), "domain_delete": rowid });

    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        dataType: "json",
        data: jsonData,
        contentType: "application/json"
    });

    //remove row
    var row = document.getElementById(rowid);
    row.parentNode.removeChild(row);
}