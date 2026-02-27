# Deploy Script for Windows User (Local Build, Remote Run)
# Run this in PowerShell

# 1. Config
$ServerIP = "47.109.193.180"
$User = "root"
$LocalPath = "E:\GitProjects\MyProject\ZhouYi"
$RemotePath = "/root/zhouyi_deploy"

# 2. Build Backend (Assuming user has Java installed, but maybe not Maven)
# Since 'mvn' is missing, we skip local build and use Docker on server but with MIRRORS.
# Or better: upload source and use a proper Dockerfile with mirrors.

Write-Host "Creating deployment package..."
New-Item -ItemType Directory -Force -Path "$LocalPath\deploy_package" | Out-Null
Copy-Item -Path "$LocalPath\backend" -Destination "$LocalPath\deploy_package" -Recurse -Force
Copy-Item -Path "$LocalPath\frontend\dist" -Destination "$LocalPath\deploy_package\frontend_dist" -Recurse -Force
Copy-Item -Path "$LocalPath\docker-compose.yml" -Destination "$LocalPath\deploy_package" -Force
Copy-Item -Path "$LocalPath\deployment" -Destination "$LocalPath\deploy_package" -Recurse -Force

# 3. Modify Dockerfile to use Mirrors (to fix timeout)
$Dockerfile = "$LocalPath\deploy_package\backend\Dockerfile"
$Content = Get-Content $Dockerfile
$NewContent = $Content -replace "FROM maven:3.8.5-openjdk-17", "FROM maven:3.8.5-openjdk-17-slim" 
# Ideally we should use a domestic mirror for maven settings, but let's try configuring daemon.json on server first.
Set-Content -Path $Dockerfile -Value $NewContent

# 4. Upload
Write-Host "Uploading to server (this might take a while)..."
scp -r "$LocalPath\deploy_package" "$User@$ServerIP:$RemotePath"

# 5. Execute on Server
Write-Host "Executing on server..."
ssh "$User@$ServerIP" "
    # Configure Docker Mirror
    mkdir -p /etc/docker
    echo '{
      \"registry-mirrors\": [
        \"https://docker.m.daocloud.io\",
        \"https://docker.1panel.live\"
      ]
    }' > /etc/docker/daemon.json
    systemctl restart docker

    # Deploy
    cd $RemotePath
    # Move frontend dist to where Dockerfile expects it (or adjust Dockerfile)
    # Our docker-compose expects build context '.'
    
    # We need to restructure slightly to match docker-compose expectations
    # docker-compose.yml expects:
    #   ./backend (present)
    #   ./deployment/frontend/Dockerfile (present)
    #   ./frontend/dist (we uploaded to frontend_dist, need to move)
    
    mkdir -p frontend
    cp -r frontend_dist/* frontend/
    
    # Run
    docker-compose down
    docker-compose up -d --build
"
