# Update ZhouYi.md on the server
$ServerIP = "47.109.193.180"
# Use relative path from home directory on server
$RemotePath = "ZhouYi_Final/backend/src/main/resources/data/ZhouYi.md"
$LocalPath = "backend\src\main\resources\data\ZhouYi.md"

Write-Host "Uploading ZhouYi.md to server..."
scp $LocalPath root@${ServerIP}:${RemotePath}

if ($LASTEXITCODE -eq 0) {
    Write-Host "Upload successful. Restarting backend service (no rebuild)..."
    # Backend reads markdown from mounted volume (/data/ZhouYi.md), so a restart is enough.
    ssh -t root@${ServerIP} "cd ZhouYi_Final && (docker compose restart backend || docker-compose restart backend)"
} else {
    Write-Host "Upload failed. Please check your connection and try again."
}
