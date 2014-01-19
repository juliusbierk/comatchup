// Wait for device API libraries to load
//
document.addEventListener("deviceready", onDeviceReady, false);

// device APIs are available
//
function onDeviceReady() {
    var db = window.openDatabase("comatchup", "1.0", "coMatchup", 200000);
    db.transaction(populateDB, errorCB, successCB);
}

// Populate the database
//
function populateDB(tx) {
    tx.executeSql('DROP TABLE IF EXISTS PROGRESS');
    tx.executeSql('CREATE TABLE IF NOT EXISTS PROGRESS (level, moves)');
    tx.executeSql('INSERT INTO PROGRESS (level, moves) VALUES ("s2l3", 5)');
}

// Transaction error callback
//
function errorCB(tx, err) {
    alert("Error processing SQL: "+err);
}

// Transaction success callback
//
function successCB() {
    alert("success!");
}