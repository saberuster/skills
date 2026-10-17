[CmdletBinding()]
param(
    [string] $ProjectRoot = '.',

    [string] $Purpose = 'godot-run',

    [string] $RequestedLogFile,

    [switch] $AllowExternal,

    [string] $ExternalPathReason,

    [string] $RunnerRunId,

    [switch] $PathOnly,

    [switch] $Json,

    [switch] $SelfTest
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-NormalizedDirectoryPath {
    param([Parameter(Mandatory = $true)][string] $Path)

    $fullPath = [System.IO.Path]::GetFullPath($Path)
    $pathRoot = [System.IO.Path]::GetPathRoot($fullPath)
    if ($fullPath.Length -gt $pathRoot.Length) {
        return $fullPath.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
    }
    return $fullPath
}

function Test-PathWithinRoot {
    param(
        [Parameter(Mandatory = $true)][string] $Candidate,
        [Parameter(Mandatory = $true)][string] $Root
    )

    $candidateFull = [System.IO.Path]::GetFullPath($Candidate)
    $rootFull = Get-NormalizedDirectoryPath -Path $Root
    $comparison = if ([System.Environment]::OSVersion.Platform -eq [System.PlatformID]::Win32NT) {
        [System.StringComparison]::OrdinalIgnoreCase
    }
    else {
        [System.StringComparison]::Ordinal
    }

    if ($candidateFull.Equals($rootFull, $comparison)) {
        return $true
    }

    $prefix = $rootFull.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
    return $candidateFull.StartsWith($prefix, $comparison)
}

function Assert-NoReparsePoint {
    param([Parameter(Mandatory = $true)][string] $Path)

    # Conservative adapter policy: reject links/junctions, including existing ancestors.
    # Callers may supply an explicitly approved, direct external path instead.
    $current = [System.IO.Path]::GetFullPath($Path)
    while (-not [string]::IsNullOrWhiteSpace($current)) {
        try { $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop }
        catch [System.Management.Automation.ItemNotFoundException] { $item = $null }
        if ($null -ne $item -and ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
            throw "Rejected symlink or reparse point in log path: $current. Use a direct path; external paths still require explicit provenance."
        }
        $current = Split-Path -Parent $current
    }
}

function Test-LogTargetWritable {
    param([Parameter(Mandatory = $true)][string] $Path)

    Assert-NoReparsePoint $Path
    $existed = Test-Path -LiteralPath $Path
    if ($existed) {
        $item = Get-Item -LiteralPath $Path -Force
        if ($item.PSIsContainer) { throw "Log target is a directory: $Path" }
        if ($item.IsReadOnly) { throw "Log file is read-only: $Path" }
    }
    $stream = $null
    $created = $false
    try {
        $mode = if ($existed) { [System.IO.FileMode]::Open } else { [System.IO.FileMode]::CreateNew }
        $stream = [System.IO.File]::Open($Path, $mode, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
        $created = -not $existed
        # Opening for write checks the file's ACL/lock without truncating existing bytes.
    }
    finally {
        if ($null -ne $stream) { $stream.Dispose() }
        if ($created) { Remove-Item -LiteralPath $Path -Force }
    }
}

function Get-GitIgnoreState {
    param(
        [Parameter(Mandatory = $true)][string] $Root,
        [Parameter(Mandatory = $true)][string] $Candidate
    )

    if ($null -eq (Get-Command git -ErrorAction SilentlyContinue)) {
        return 'git-unavailable'
    }

    $previousErrorActionPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $insideWorkTree = & git -C $Root rev-parse --is-inside-work-tree 2>$null
        $insideWorkTreeExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousErrorActionPreference
    }
    if ($insideWorkTreeExitCode -ne 0 -or $insideWorkTree -notcontains 'true') {
        return 'not-a-repository'
    }

    $rootFull = Get-NormalizedDirectoryPath -Path $Root
    $relativePath = [System.IO.Path]::GetFullPath($Candidate).Substring($rootFull.Length).TrimStart('\', '/')
    try {
        $ErrorActionPreference = 'Continue'
        & git -C $Root check-ignore --quiet -- $relativePath 2>$null
        $checkIgnoreExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousErrorActionPreference
    }
    if ($checkIgnoreExitCode -eq 0) {
        return 'ignored'
    }
    return 'not-ignored'
}

function Resolve-GodotLogPreflight {
    param(
        [Parameter(Mandatory = $true)][string] $Root,
        [Parameter(Mandatory = $true)][string] $RunPurpose,
        [string] $RequestedPath,
        [bool] $PermitExternal,
        [string] $ExternalReason,
        [bool] $ResolveOnly = $false,
        [string] $CompanionRunId = ''
    )

    $warnings = [System.Collections.Generic.List[string]]::new()
    $blockers = [System.Collections.Generic.List[string]]::new()
    $resolvedRoot = ''
    $logPath = ''
    $source = ''
    $isExternal = $false
    $ignoreState = 'not-checked'
    $companionPaths = @()

    try {
        if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
            throw "Project root does not exist: $Root"
        }
        $resolvedRoot = Get-NormalizedDirectoryPath -Path (Resolve-Path -LiteralPath $Root).ProviderPath
        Assert-NoReparsePoint $resolvedRoot
        $projectFile = Join-Path $resolvedRoot 'project.godot'
        if (-not (Test-Path -LiteralPath $projectFile -PathType Leaf)) {
            throw "Project root lacks project.godot: $resolvedRoot"
        }
        if ($RunPurpose -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]*$') {
            throw "Purpose may contain only letters, digits, dots, underscores, and hyphens, and must start with a letter or digit: $RunPurpose"
        }

        if ([string]::IsNullOrWhiteSpace($RequestedPath)) {
            $logDirectory = Join-Path (Join-Path $resolvedRoot '.godot') 'codex-logs'
            $logPath = Join-Path $logDirectory "$RunPurpose.log"
            $source = 'project-default'
        }
        elseif ([System.IO.Path]::IsPathRooted($RequestedPath)) {
            $logPath = [System.IO.Path]::GetFullPath($RequestedPath)
            $source = 'requested'
        }
        else {
            $logPath = [System.IO.Path]::GetFullPath((Join-Path $resolvedRoot $RequestedPath))
            $source = 'requested'
        }

        if ([System.IO.Path]::GetExtension($logPath) -ine '.log') {
            throw "Log files must use the .log extension: $logPath"
        }

        Assert-NoReparsePoint $logPath
        $isExternal = -not (Test-PathWithinRoot -Candidate $logPath -Root $resolvedRoot)
        if ($isExternal) {
            if (-not $PermitExternal) {
                throw "Rejected external project log path: $logPath. Stop and report project-local preflight failures; do not automatically fall back to temporary directories."
            }
            if ([string]::IsNullOrWhiteSpace($ExternalReason)) {
                throw 'External paths require ExternalPathReason identifying explicit user, repository, or CI configuration.'
            }
            $source = 'requested-external'
            $warnings.Add("External log path passed filesystem write preflight only; the current Godot run must still validate it: $ExternalReason")
        }
        else {
            $ignoreState = Get-GitIgnoreState -Root $resolvedRoot -Candidate $logPath
            if ($ignoreState -eq 'not-ignored') {
                throw "Project log path is not Git-ignored: $logPath. Use an existing ignored repository directory; preflight does not modify .gitignore."
            }
            if ($ignoreState -eq 'git-unavailable') {
                $warnings.Add('git was not found; log-path ignore status cannot be confirmed.')
            }
            elseif ($ignoreState -eq 'not-a-repository') {
                $warnings.Add('Project root is not in a Git worktree; skipping ignore checks.')
            }
        }

        if (-not [string]::IsNullOrWhiteSpace($CompanionRunId)) {
            $parsedId = [guid]::Empty
            if (-not [guid]::TryParseExact($CompanionRunId, 'N', [ref]$parsedId)) {
                throw 'RunnerRunId must be a GUID without hyphens.'
            }
            $companionPaths = @("$logPath.lock", "$logPath.$CompanionRunId.stdout.txt", "$logPath.$CompanionRunId.stderr.txt")
            foreach ($companion in $companionPaths) {
                Assert-NoReparsePoint $companion
                if (Test-Path -LiteralPath $companion -PathType Container) { throw "Diagnostic artifact path is a directory: $companion" }
                if (-not $isExternal -and (Get-GitIgnoreState -Root $resolvedRoot -Candidate $companion) -eq 'not-ignored') {
                    throw "Project diagnostic artifact path is not Git-ignored: $companion. Preflight does not modify .gitignore."
                }
            }
        }

        $parent = Split-Path -Parent $logPath
        if ([string]::IsNullOrWhiteSpace($parent)) {
            throw "Cannot resolve log parent directory: $logPath"
        }
        New-Item -ItemType Directory -Path $parent -Force | Out-Null

        Assert-NoReparsePoint $logPath
        if (-not $ResolveOnly) { Test-LogTargetWritable $logPath }
    }
    catch {
        $blockers.Add($_.Exception.Message)
    }

    $status = if ($blockers.Count -gt 0) { 'blocked' } elseif ($ResolveOnly) { 'path-validated' } else { 'ready' }
    return [ordered]@{
        status = $status
        projectRoot = $resolvedRoot
        logPath = $logPath
        source = $source
        isExternal = $isExternal
        gitIgnoreState = $ignoreState
        companionPaths = $companionPaths
        linkPolicy = 'reject-reparse-points'
        writableAtCheckTime = ($blockers.Count -eq 0 -and -not $ResolveOnly)
        warnings = @($warnings)
        blockers = @($blockers)
    }
}

function Write-PreflightResult {
    param(
        [Parameter(Mandatory = $true)][System.Collections.IDictionary] $Result,
        [Parameter(Mandatory = $true)][int] $ExitCode
    )

    if ($Json) {
        $Result | ConvertTo-Json -Depth 6
    }
    else {
        Write-Output "Status: $($Result.status)"
        Write-Output "Project root: $($Result.projectRoot)"
        Write-Output "Log: $($Result.logPath)"
        Write-Output "Source: $($Result.source)"
        Write-Output "External path: $($Result.isExternal)"
        Write-Output "Git ignore state: $($Result.gitIgnoreState)"
        foreach ($warning in @($Result.warnings)) {
            Write-Warning $warning
        }
        foreach ($blocker in @($Result.blockers)) {
            Write-Error $blocker -ErrorAction Continue
        }
    }
    exit $ExitCode
}

function Assert-SelfTest {
    param(
        [Parameter(Mandatory = $true)][bool] $Condition,
        [Parameter(Mandatory = $true)][string] $Message
    )

    if (-not $Condition) {
        throw "Self-test failed: $Message"
    }
}

if ($SelfTest) {
    $tempRoot = Get-NormalizedDirectoryPath -Path ([System.IO.Path]::GetTempPath())
    $fixtureRoot = Join-Path $tempRoot ('godot-log-preflight-' + [guid]::NewGuid().ToString('N'))
    $externalRoot = Join-Path $tempRoot ('godot-log-external-' + [guid]::NewGuid().ToString('N'))
    try {
        New-Item -ItemType Directory -Path $fixtureRoot -Force | Out-Null
        [System.IO.File]::WriteAllText((Join-Path $fixtureRoot 'project.godot'), 'config_version=5')

        $defaultResult = Resolve-GodotLogPreflight -Root $fixtureRoot -RunPurpose 'headless-smoke' -RequestedPath '' -PermitExternal $false -ExternalReason ''
        $expectedDefault = Join-Path (Join-Path (Join-Path $fixtureRoot '.godot') 'codex-logs') 'headless-smoke.log'
        Assert-SelfTest -Condition ($defaultResult.status -eq 'ready') -Message 'The default project-local log path must pass preflight.'
        Assert-SelfTest -Condition ($defaultResult.logPath -eq $expectedDefault) -Message "Incorrect default log path: $($defaultResult.logPath)"
        Assert-SelfTest -Condition (-not $defaultResult.isExternal) -Message 'The default log path must not be external to the project.'

        if ($null -ne (Get-Command git -ErrorAction SilentlyContinue)) {
            [System.IO.File]::WriteAllText((Join-Path $fixtureRoot '.gitignore'), ".godot/`n")
            & git -C $fixtureRoot init --quiet
            Assert-SelfTest -Condition ($LASTEXITCODE -eq 0) -Message 'Cannot initialize the Git self-test fixture.'

            $ignoredResult = Resolve-GodotLogPreflight -Root $fixtureRoot -RunPurpose 'git-ignored' -RequestedPath '' -PermitExternal $false -ExternalReason ''
            Assert-SelfTest -Condition ($ignoredResult.status -eq 'ready') -Message 'Git-ignored project-local log paths must pass preflight.'
            Assert-SelfTest -Condition ($ignoredResult.gitIgnoreState -eq 'ignored') -Message ".godot logs must be identified as ignored; actual state: $($ignoredResult.gitIgnoreState)."

            $visiblePath = Join-Path 'codex-visible' 'visible.log'
            $visibleResult = Resolve-GodotLogPreflight -Root $fixtureRoot -RunPurpose 'visible' -RequestedPath $visiblePath -PermitExternal $false -ExternalReason ''
            Assert-SelfTest -Condition ($visibleResult.status -eq 'blocked') -Message 'Non-ignored project-local log paths must be blocked.'
        }

        $escapePath = Join-Path '..' 'outside.log'
        $escapeResult = Resolve-GodotLogPreflight -Root $fixtureRoot -RunPurpose 'escape' -RequestedPath $escapePath -PermitExternal $false -ExternalReason ''
        Assert-SelfTest -Condition ($escapeResult.status -eq 'blocked') -Message 'Path escapes must be blocked.'

        $externalLog = Join-Path $externalRoot 'explicit.log'
        $unapprovedResult = Resolve-GodotLogPreflight -Root $fixtureRoot -RunPurpose 'external' -RequestedPath $externalLog -PermitExternal $false -ExternalReason ''
        Assert-SelfTest -Condition ($unapprovedResult.status -eq 'blocked') -Message 'Unauthorized external log paths must be blocked.'

        $missingReasonResult = Resolve-GodotLogPreflight -Root $fixtureRoot -RunPurpose 'external' -RequestedPath $externalLog -PermitExternal $true -ExternalReason ''
        Assert-SelfTest -Condition ($missingReasonResult.status -eq 'blocked') -Message 'External log paths lacking provenance must be blocked.'

        $approvedResult = Resolve-GodotLogPreflight -Root $fixtureRoot -RunPurpose 'external' -RequestedPath $externalLog -PermitExternal $true -ExternalReason 'self-test explicit path'
        Assert-SelfTest -Condition ($approvedResult.status -eq 'ready') -Message 'Explicitly allowed external log paths with provenance must pass filesystem preflight.'
        Assert-SelfTest -Condition $approvedResult.isExternal -Message 'External project log paths must be marked external.'

        $invalidPurposeResult = Resolve-GodotLogPreflight -Root $fixtureRoot -RunPurpose '..\bad' -RequestedPath '' -PermitExternal $false -ExternalReason ''
        Assert-SelfTest -Condition ($invalidPurposeResult.status -eq 'blocked') -Message 'Invalid Purpose values must be blocked.'

        Write-Output 'Self-test: passed'
        exit 0
    }
    finally {
        foreach ($path in @($fixtureRoot, $externalRoot)) {
            if ((Test-Path -LiteralPath $path) -and (Test-PathWithinRoot -Candidate $path -Root $tempRoot)) {
                Remove-Item -LiteralPath $path -Recurse -Force
            }
        }
    }
}

$result = Resolve-GodotLogPreflight `
    -Root $ProjectRoot `
    -RunPurpose $Purpose `
    -RequestedPath $RequestedLogFile `
    -PermitExternal $AllowExternal.IsPresent `
    -ExternalReason $ExternalPathReason `
    -ResolveOnly $PathOnly.IsPresent `
    -CompanionRunId $RunnerRunId

$exitCode = if ($result.status -in @('ready', 'path-validated')) { 0 } else { 1 }
Write-PreflightResult -Result $result -ExitCode $exitCode
