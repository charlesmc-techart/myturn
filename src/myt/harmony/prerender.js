/**
 * @fileoverview Before the render, get the version name, various info about
 * the xstage, then write them to the temporary file
*/

/**
 * Get information about the scene
 * @return {!Array<string>} This returns an array of strings about the scene
 */
function getSceneInfo() {
  const versionName = scene.currentVersionName()
  const numFrames = frame.numberOf()
  const startFrame = scene.getStartFrame()
  const endFrame = scene.getStopFrame()
  const colorSpace = scene.colorSpace()
  return [versionName, numFrames, startFrame, endFrame, colorSpace]
}

/**
 * Set renders to write to directory named after version name
 * @param {string} sceneVersionName Verstion name of the scene
 */
function setWriteLocation(sceneVersionName) {
  const mlwNode = node.getNodes(['MultiLayerWrite'])[0]
  const renderPath = System.getenv('MYT_RENDER_PATH')
  const renderVersion = System.getenv('MYT_RENDER_VERSION')
  const versionDir = sceneVersionName + '_' + renderVersion
  var filePath = renderPath + '/' + versionDir + '/' + sceneVersionName + '-'
  filePath = fileMapper.toNativePath(filePath)
  node.setTextAttr(mlwNode, 'drawingName', frame.current(), filePath)
  node.setTextAttr(mlwNode, 'drawingType', frame.current(), 'EXR_ZIP_1LINE')
}

/**
 * Write input information to file in specified path
 * @param {string} sceneInfo Text to be written
 */
function writeToFile(sceneInfo, filePath) {
  const file = new File(filePath)
  file.open(FileAccess.WriteOnly)
  file.write(sceneInfo)
  file.close()
}

function main() {
  const sceneInfo = getSceneInfo()
  setWriteLocation(sceneInfo[0])

  const filePath = System.getenv('MYT_RENDER_INFO_PATH')
  writeToFile(sceneInfo, filePath)
}

main()
