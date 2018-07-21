document.addEventListener("keydown", function (e) {
    if (e.which === 123) {
        // F12
        require("electron").remote.BrowserWindow.getFocusedWindow().webContents.toggleDevTools();
    } else if (e.which === 116) {
        // F5
        location.reload();
    }
});
