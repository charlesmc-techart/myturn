/**
 * @fileoverview Before the render, get the version name, various info about
 * the xstage, then write them to the temporary file
*/

/**
 * Get information about the scene
 * @return {!Array<string>} This returns an array of strings about the scene
 */
function getXstageInfo() {
  const versionName = scene.currentVersionName()
  const numFrames = frame.numberOf()
  const startFrame = scene.getStartFrame()
  const endFrame = scene.getStopFrame()
  const colorSpace = scene.colorSpace()
  return [versionName, numFrames, startFrame, endFrame, colorSpace]
}

/**
 * Set renders to write to directory named after version name
 * @param {string} versionName Verstion name of the scene
 */
function setWriteLocation(versionName) {
  const mlwNode = node.getNodes(['MultiLayerWrite'])[0]
  const renderDir = System.getenv('MYT_RENDER_DIR')
  const renderVer = System.getenv('MYT_RENDER_VER')
  const versionDir = versionName + '_' + renderVer
  var filePath = renderDir + '/' + versionDir + '/' + versionName + '-'
  filePath = fileMapper.toNativePath(filePath)
  node.setTextAttr(mlwNode, 'drawingName', frame.current(), filePath)
  node.setTextAttr(mlwNode, 'drawingType', frame.current(), 'EXR_ZIP_1LINE')
}

/**
 * Write input information to file in specified path
 * @param {string} infoToWrite Text to be written
 */
function writeToFile(infoToWrite, filePath) {
  const file = new File(filePath)
  file.open(FileAccess.WriteOnly)
  file.write(infoToWrite)
  file.close()
}

function main() {
  const xstageInfo = getXstageInfo()
  setWriteLocation(xstageInfo[0])

  const filePath = System.getenv('MYT_TEMP_FILE')
  writeToFile(xstageInfo, filePath)
}

main()
