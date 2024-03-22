$HarmonyVer = 21.1
$MayaVer = 2023 # Using mayapy because Windows doesn't have Python pre-installed

$MayapyPath = "C:\Program Files\Autodesk\Maya${MayaVer}\bin"
$env:Path += ";${MayapyPath}"

$HarmonyPath = mayapy "${PSScriptRoot}\bin\getHarmonyPath.py" "${HarmonyVer}"
$env:Path += ";${HarmonyPath}"

$harmony = "${PSScriptRoot}\src\harmony"
$Scripts = @()
$Scripts += "${PSScriptRoot}\bin\renderHarmonyScenes.py"
$Scripts += "${harmony}\prerender.js"
$Scripts += "${harmony}\postrender.js"

$HarmonyScenePaths = @()
foreach ("${arg}" in "${args}") {
    $HarmonyScenePaths += "${arg}"
}

mayapy $Scripts[0] @HarmonyScenePaths -pr $Scripts[1] -ps $Scripts[2]
