# Script pour télécharger gradle-wrapper.jar
Write-Host "Téléchargement de gradle-wrapper.jar..." -ForegroundColor Green

$wrapperDir = "gradle\wrapper"
$jarFile = "$wrapperDir\gradle-wrapper.jar"
$url = "https://raw.githubusercontent.com/gradle/gradle/v8.5.0/gradle/wrapper/gradle-wrapper.jar"

# Créer le dossier si nécessaire
if (-not (Test-Path $wrapperDir)) {
    New-Item -ItemType Directory -Path $wrapperDir -Force | Out-Null
}

# Télécharger le fichier
try {
    Invoke-WebRequest -Uri $url -OutFile $jarFile -UseBasicParsing
    Write-Host "✅ gradle-wrapper.jar téléchargé avec succès!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Vous pouvez maintenant exécuter: .\gradlew.bat build" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Erreur lors du téléchargement: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Téléchargez manuellement depuis:" -ForegroundColor Yellow
    Write-Host $url -ForegroundColor Yellow
    Write-Host "Et placez-le dans: $jarFile" -ForegroundColor Yellow
}
