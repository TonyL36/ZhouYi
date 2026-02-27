# Update Frontend on the server
$ServerIP = "47.109.193.180"
# Use relative path from home directory on server
$RemotePath = "ZhouYi_Final/frontend/dist"
$LocalPath = "frontend\dist"

Write-Host "Uploading Frontend build to server..."
scp -r $LocalPath/* root@${ServerIP}:${RemotePath}/

if ($LASTEXITCODE -eq 0) {
    Write-Host "Upload successful. Restarting frontend service (no rebuild)..."
    ssh -t root@${ServerIP} "cd ZhouYi_Final && (docker compose restart frontend || docker-compose restart frontend)"
} else {
    Write-Host "Upload failed. Please check your connection and try again."
}
