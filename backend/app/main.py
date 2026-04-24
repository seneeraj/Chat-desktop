const { app, BrowserWindow } = require("electron");
const path = require("path");

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    title: "Approval Based Chat App",
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  let indexPath;

  if (app.isPackaged) {
    // ✅ When running EXE
    indexPath = path.join(
      process.resourcesPath,
      "app",
      "frontend",
      "build",
      "index.html"
    );
  } else {
    // ✅ When running locally
    indexPath = path.join(
      __dirname,
      "frontend",
      "build",
      "index.html"
    );
  }

  console.log("Loading:", indexPath);

  mainWindow.loadFile(indexPath);

  mainWindow.webContents.openDevTools();
}

app.whenReady().then(() => {
  createWindow();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
