/**
 * @fileoverview After the render, count the number of EXR files saved to the
 * output folder then write them to the temporary file
 */

/**
 * @return {string} Directory containing rendered EXRs
 */
function findRenderPath() {
  const renderPath = System.getenv("MYT_RENDER_PATH");
  const sceneVersionName = scene.currentVersionName();
  const renderVersion = System.getenv("MYT_RENDER_VERSION");
  var versionDir = sceneVersionName + "_" + renderVersion;
  versionDir = renderPath + "/" + versionDir;
  return fileMapper.toNativePath(versionDir);
}

/**
 * @param {string} renderPath The directory containing EXR files
 * @return {number} The number of EXR files in the directory
 */
function countRenderedFrames(renderPath) {
  const dir = new Dir(renderPath);
  return dir.entryList("*.exr").length;
}

/**
 * @param {string} renderInfo Text to be written
 */
function writeToFile(renderInfo, filePath) {
  const file = new File(filePath);
  file.open(FileAccess.Append);
  file.write(renderInfo);
  file.close();
}

function main() {
  const renderPath = findRenderPath();
  const numRenderedFrames = countRenderedFrames(renderPath);
  const filePath = System.getenv("MYT_RENDER_INFO_PATH");
  writeToFile([, numRenderedFrames], filePath);
}

main();
