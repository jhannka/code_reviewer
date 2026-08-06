$targetDir = "c:\Users\DESARROLLADOR\Documents\www\code_reviewer"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

if (-not $currentPath) {
    $currentPath = ""
}

if ($currentPath -notmatch [regex]::Escape($targetDir)) {
    if ($currentPath.EndsWith(";")) {
        $newPath = $currentPath + $targetDir
    } else {
        $newPath = $currentPath + ";" + $targetDir
    }
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "Added $targetDir to User PATH."
} else {
    Write-Host "Directory $targetDir is already in User PATH."
}
