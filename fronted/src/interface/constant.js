const defaultExport = undefined;
export default defaultExport;

const reactInterval = {
  rapid: 150,
  medium: 300,
  slow: 450
};
export { reactInterval };

const isWebview = window.require === undefined;
const isDevMode = window.location.port === "3000";
export { isWebview, isDevMode }

const pythonFileName = "quick_start.py";
const logDirectoryName = "log";
export { pythonFileName, logDirectoryName };
