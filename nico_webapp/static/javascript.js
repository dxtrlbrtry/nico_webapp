function setActiveTab(tabId) {
    var activeTab = document.getElementsByClassName("active-tab")[0];
    if (activeTab != null) {
        activeTab.classList.remove("active-tab");
    }

    var currentTab = document.getElementById(tabId);
    currentTab.classList.add("active-tab");
}

function apply_span(event) {
    var button = event.target;
    var col_span = document.getElementById('col_' + button.id)
    var row_span = document.getElementById('row_' + button.id);
    var url = document.URL + button.id + '/' + col_span.value + '/' + row_span.value + '/';
    var request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.send();
    col_span.style.backgroundColor = '#3CBC8D';
    row_span.style.backgroundColor = '#3CBC8D';
}