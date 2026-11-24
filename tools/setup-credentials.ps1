$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$envPath = Join-Path $projectRoot '.env'
$settings = @{}
if (Test-Path -LiteralPath $envPath) {
    foreach ($line in Get-Content -LiteralPath $envPath) {
        if ($line -match '^(SPEECH_KEY|SPEECH_REGION|OPENAI_API_KEY|OPENAI_MODEL)=(.*)$') {
            $settings[$Matches[1]] = $Matches[2]
        }
    }
}
Write-Host 'Keys stay in the local .env file and are excluded from the classroom ZIP.'
Write-Host 'Leave an entry blank to keep its existing value.'
$helpText = @{
    SPEECH_KEY = 'Azure portal > your Speech resource > Keys and Endpoint: copy KEY 1 or KEY 2. This is not your Microsoft password.'
    SPEECH_REGION = 'The region code of that same resource, e.g. koreacentral or eastus. Do not enter a URL, display name, or en-AU.'
    OPENAI_API_KEY = 'OpenAI API platform > your project > API keys: create/copy a secret API key. Do not use an Azure key or a ChatGPT password.'
    OPENAI_MODEL = 'API model ID, e.g. gpt-5.4-mini if your project has access. This is a model name, not a secret key.'
}
foreach ($name in @('SPEECH_KEY','SPEECH_REGION','OPENAI_API_KEY','OPENAI_MODEL')) {
    Write-Host ''
    Write-Host $helpText[$name]
    if ($name.EndsWith('KEY')) {
        while ($true) {
            $mode = Read-Host 'Press C to read a copied key from the clipboard, or Enter for hidden input'
            if ($mode -ieq 'C') {
                $value = Get-Clipboard -Raw
            } else {
                $secureValue = Read-Host $name -AsSecureString
                $value = [System.Net.NetworkCredential]::new('', $secureValue).Password
            }
            $candidate = if ($value) { $value.Trim() } else { $settings[$name] }
            if (-not $candidate) { break }
            if ($candidate.Length -ge 20 -and $candidate -cmatch '^[\x21-\x7E]+$' -and -not $candidate.StartsWith('http') -and -not $candidate.Contains('=')) {
                Write-Host 'Key format accepted. The service connection has not been tested.'
                break
            }
            Write-Host 'The key is incomplete or contains invalid characters. Copy the full key, then choose C. Its contents will not be displayed.' -ForegroundColor Yellow
        }
    } else {
        $value = Read-Host $name
    }
    if ($value) { $settings[$name] = $value.Trim() }
}
$content = @('# Local credentials. Never commit or share this file.')
foreach ($name in @('SPEECH_KEY','SPEECH_REGION','OPENAI_API_KEY','OPENAI_MODEL')) {
    $content += "$name=$($settings[$name])"
}
[System.IO.File]::WriteAllLines($envPath, $content, [System.Text.UTF8Encoding]::new($false))
Write-Host 'Saved. Restart the classroom server after changing credentials.'
