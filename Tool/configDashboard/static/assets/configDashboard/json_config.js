function getCookie(name) {
    var cookieArr = document.cookie.split(";");

    // Loop through the array elements
    for (var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");

        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if (name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }

    // Return null if not found
    return null;
}

function http_config_submit(http_value) {

    if (http_value == 'block_http') {
        alert_show()
    }

    document.getElementById(http_value).children[0].checked = true;

    var jsonData = JSON.stringify({ "csrfmiddlewaretoken": getCookie('csrftoken'), "http_settings": http_value });

    if (document.getElementById('default_on').children[0].checked & http_value != 'block_http') {
        document.getElementById('default_on').children[0].checked = false
        document.getElementById('default_on').classList.remove("active")
        document.getElementById('default_off').children[0].checked = true
        document.getElementById('default_off').classList.add("active")
    }

    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        dataType: "json",
        data: jsonData,
        contentType: "application/json"
    });
    return false;
}

function default_secure_config(secure_config_value) {

    document.getElementById(secure_config_value).children[0].checked = true;

    var jsonData = JSON.stringify({ "csrfmiddlewaretoken": getCookie('csrftoken'), "default_config_value": secure_config_value });

    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        dataType: "json",
        data: jsonData,
        contentType: "application/json"
    });

    if (secure_config_value == 'default_on') {
        location.reload()
    }

    return false;
}

function channel_config_submit(broadcaster, mode) {

    if (document.getElementById('default_on').children[0].checked & mode != 'noTrack') {
        document.getElementById('default_on').children[0].checked = false
        document.getElementById('default_on').classList.remove("active")
        document.getElementById('default_off').children[0].checked = true
        document.getElementById('default_off').classList.add("active")
    }

    if (mode == 'block') {
        alert_show()
    }

    var jsonData = JSON.stringify({ "csrfmiddlewaretoken": getCookie('csrftoken'), "broadcaster": broadcaster, "modality": mode });

    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        dataType: "json",
        data: jsonData,
        contentType: "application/json"
    });
    return false;

}

//this can be used both when loading data for the plot for the specific broadcaster but also when loading the previuos configuration
// to show the user with his old one
function loadJson(element_id) {
    var json_string = document.getElementById(element_id).getAttribute("data-json")
    var json_string_correct = json_string.replace(/'/g, '"');
    json_data = JSON.parse(json_string_correct);
    //console.log(json_data)
    return json_data
}

function set_previous_config() {
    json_data = loadJson('previous_config')

    channel_list = ['rai', 'mediaset', 'rkk', 'sportitalia', 'rds', 'rtl', 'discovery', 'paramount', 'cairo']

    for (i = 0; i < channel_list.length; i++) {
        if (Object.values(json_data)[i] == 'block') {
            id = channel_list[i] + "_2"
            rem_1 = channel_list[i] + "_0"
            rem_2 = channel_list[i] + "_1"
            document.getElementById(id).children[0].checked = true
            document.getElementById(id).classList.add("active")
            document.getElementById(rem_1).classList.remove("active")
            document.getElementById(rem_2).classList.remove("active")
        } else if (Object.values(json_data)[i] == 'allow') {
            id = channel_list[i] + "_0"
            rem_1 = channel_list[i] + "_2"
            rem_2 = channel_list[i] + "_1"
            document.getElementById(id).children[0].checked = true
            document.getElementById(id).classList.add("active")
            document.getElementById(rem_1).classList.remove("active")
            document.getElementById(rem_2).classList.remove("active")
        } else {
            id = channel_list[i] + "_1"
            rem_1 = channel_list[i] + "_0"
            rem_2 = channel_list[i] + "_2"
            document.getElementById(id).children[0].checked = true
            document.getElementById(id).classList.add("active")
            document.getElementById(rem_1).classList.remove("active")
            document.getElementById(rem_2).classList.remove("active")
        }
    }
}

function set_previous_http() {
    var http_value = document.getElementById("http_config").getAttribute('data-json')

    if (http_value == 'block') {
        document.getElementById("block_http").children[0].checked = true
        document.getElementById("block_http").classList.add("active")
        document.getElementById("allow_http").classList.remove("active")
    } else {
        document.getElementById("allow_http").children[0].checked = true
        document.getElementById("allow_http").classList.add("active")
        document.getElementById("block_http").classList.remove("active")
    }
}


console.log('working')