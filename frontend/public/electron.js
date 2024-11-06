// Modules to control application life and create native browser window
const { app, Menu, BrowserWindow } = require('electron');
const path = require('path');
const isDevMode = require('electron-is-dev');

function createWindow() {
  if (process.platform === 'darwin') {
    const template = [
      {
        label: "Application",
        submenu: [
          { label: "Quit", accelerator: "Command+Q", click: function() { app.quit(); }}
        ]
      }, 
      {
        label: "Edit",
        submenu: [
          { label: "Copy", accelerator: "CmdOrCtrl+C", selector: "copy:" },
          { label: "Paste", accelerator: "CmdOrCtrl+V", selector: "paste:" },
        ]
      }
    ];
    Menu.setApplicationMenu(Menu.buildFromTemplate(template))
  } else {
    Menu.setApplicationMenu(null)
  }

  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 440,
    height: 750,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
    },
    // frame: false,
    // transparent: true,
    // backgroundColor: '#00000000'
  })

  // mainWindow.Menu.setApplicationMenu(null);
  // and load the index.html of the app.
  if (isDevMode) {
    // mainWindow.webContents.openDevTools();
    mainWindow.loadURL('http://localhost:3000/');
  } else {
    mainWindow.loadURL(`file://${path.join(__dirname, '../build/index.html')}`);
  }
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()
  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit();
  }
})
