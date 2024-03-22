/**
 * @fileoverview After the render, count the number of EXR files saved to the
 * output folder then write them to the temporary file
*/

/**
 * @return {string} Directory containing rendered EXRs
 */
function getVersionDir() {
  const renderDir = System.getenv('MYT_RENDER_DIR')
  const versionName = scene.currentVersionName()
  const renderVer = System.getenv('MYT_RENDER_VER')
  var versionDir = versionName + '_' + renderVer
  versionDir = renderDir + '/' + versionDir
  return fileMapper.toNativePath(versionDir)
}

/**
 * @param {string} directoryPath The directory containing EXR files
 * @return {number} The number of EXR files in the directory
 */
function countRenderedFrames(directoryPath) {
  const dir = new Dir(directoryPath)
  return dir.entryList('*.exr').length
}

/**
 * @param {string} infoToWrite Text to be written
 */
function writeToFile(infoToWrite, filePath) {
  const file = new File(filePath)
  file.open(FileAccess.Append)
  file.write(infoToWrite)
  file.close()
}

function main() {
  const versionDir = getVersionDir()
  const numRenderedFrames = countRenderedFrames(versionDir)
  const filePath = System.getenv('MYT_TEMP_FILE')
  writeToFile([, numRenderedFrames], filePath)
}

main()
