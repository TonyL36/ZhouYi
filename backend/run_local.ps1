$ErrorActionPreference = "Stop"

# Check if .mvn/wrapper directory exists, if not create it
if (-not (Test-Path ".mvn\wrapper")) {
    New-Item -ItemType Directory -Force -Path ".mvn\wrapper" | Out-Null
}

# Create Maven Wrapper properties if not exists
$WrapperPropsPath = ".mvn\wrapper\maven-wrapper.properties"
if (-not (Test-Path $WrapperPropsPath)) {
    Write-Host "Writing maven-wrapper.properties..."
    @"
distributionUrl=https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.9.6/apache-maven-3.9.6-bin.zip
wrapperUrl=https://repo.maven.apache.org/maven2/org/apache/maven/wrapper/maven-wrapper/3.2.0/maven-wrapper-3.2.0.jar
"@ | Set-Content -Encoding ASCII -Path $WrapperPropsPath
}

# Download Maven Wrapper jar if not exists
$WrapperJarUrl = "https://repo.maven.apache.org/maven2/org/apache/maven/wrapper/maven-wrapper/3.2.0/maven-wrapper-3.2.0.jar"
$WrapperJarPath = ".mvn\wrapper\maven-wrapper.jar"
if (-not (Test-Path $WrapperJarPath)) {
    Write-Host "Downloading maven-wrapper.jar..."
    Invoke-WebRequest -Uri $WrapperJarUrl -OutFile $WrapperJarPath
}

# Run the application
Write-Host "Starting Spring Boot application..."
$ProjectDir = (Get-Location).Path
java "-Dmaven.multiModuleProjectDirectory=$ProjectDir" -classpath $WrapperJarPath org.apache.maven.wrapper.MavenWrapperMain spring-boot:run
