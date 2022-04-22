function addDateRange(){
    var tag = "<p>Date range 1: <input type=\"date\" name=\"data_range_from[]\"> to <input type=\"date\" name=\"data_range_to[]\"><br></p>"
    var element = document.getElementById("event_inp");
    element.appendChild(tag);
}