#requires -Version 7.2
[CmdletBinding()]
param(
    [string] $GodotExecutable,

    [string] $ProjectRoot = '.',

    [string] $Purpose = 'godot-run',

    [string[]] $EngineArgs = @(),

    [string[]] $UserArgs = @(),

    [string] $RequestedLogFile,

    [switch] $AllowExternalLog,

    [string] $ExternalLogReason,

    [string[]] $AllowedLogErrorPattern = @(),

    [double] $TimeoutSeconds = 120,

    [switch] $Json,

    [switch] $SelfTest,

    [Parameter(DontShow)][switch] $InternalSupervisor
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RunnerExitCode = [ordered]@{
    InvalidArguments = 64
    LogPreflight = 65
    StaleLog = 66
    LogErrors = 67
    Timeout = 68
    Launch = 69
}

$ProtectedEngineOptions = @(
    '--editor',
    '--headless',
    '--import',
    '--log-file',
    '--path',
    '--project-manager',
    '--quit-after',
    '--scene',
    '--script',
    '--write-movie'
)

$GodotErrorHeaderPattern = '^\s*(?:SCRIPT ERROR:|ERROR:|E \d{1,2}:\d{2}:\d{2}:)'

function Test-OptionMatch {
    param(
        [Parameter(Mandatory = $true)][string] $Argument,
        [Parameter(Mandatory = $true)][string] $Option
    )

    return $Argument -eq $Option -or $Argument.StartsWith("$Option=", [System.StringComparison]::Ordinal)
}

function Assert-ArgumentPartition {
    param(
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][string[]] $EngineArguments,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][string[]] $ProjectArguments,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][string[]] $AllowedPatterns
    )

    foreach ($argument in @($EngineArguments) + @($ProjectArguments)) {
        if ($null -eq $argument) {
            throw 'EngineArgs and UserArgs must not contain null.'
        }
        if ($argument -eq '--') {
            throw 'EngineArgs and UserArgs must not contain the argument separator --.'
        }
    }

    foreach ($argument in $EngineArguments) {
        foreach ($ownedOption in @('--path', '--log-file')) {
            if (Test-OptionMatch -Argument $argument -Option $ownedOption) {
                throw "$ownedOption is injected by invoke_godot.ps1 and must not appear in EngineArgs."
            }
        }
    }

    foreach ($argument in $ProjectArguments) {
        foreach ($engineOption in $ProtectedEngineOptions) {
            if (Test-OptionMatch -Argument $argument -Option $engineOption) {
                throw "Godot engine option $engineOption must not appear in UserArgs."
            }
        }
    }

    foreach ($pattern in $AllowedPatterns) {
        try {
            [void][regex]::new($pattern)
        }
        catch {
            throw "AllowedLogErrorPattern is not a valid regular expression: $pattern"
        }
    }
}

function Resolve-ExecutablePath {
    param([Parameter(Mandatory = $true)][string] $Executable)

    if ([string]::IsNullOrWhiteSpace($Executable)) {
        throw 'GodotExecutable is required.'
    }

    $looksLikePath = [System.IO.Path]::IsPathRooted($Executable) -or
        $Executable.Contains([System.IO.Path]::DirectorySeparatorChar) -or
        $Executable.Contains([System.IO.Path]::AltDirectorySeparatorChar)

    if ($looksLikePath) {
        if (-not (Test-Path -LiteralPath $Executable -PathType Leaf)) {
            throw "GodotExecutable does not exist: $Executable"
        }
        return (Resolve-Path -LiteralPath $Executable).ProviderPath
    }

    $command = Get-Command $Executable -CommandType Application,ExternalScript -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($null -eq $command) {
        throw "Cannot resolve GodotExecutable from PATH: $Executable"
    }
    return $command.Source
}

function Get-FileSnapshot {
    param([Parameter(Mandatory = $true)][string] $Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $null
    }

    $item = Get-Item -LiteralPath $Path -Force
    return [ordered]@{
        length = $item.Length
        lastWriteTimeUtc = $item.LastWriteTimeUtc
        hash = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
    }
}

function Test-FreshLog {
    param(
        [System.Collections.IDictionary] $Before,
        [System.Collections.IDictionary] $After,
        [Parameter(Mandatory = $true)][datetime] $RunStartedUtc
    )

    if ($null -eq $After) {
        return $false
    }

    $changed = $null -eq $Before -or
        $Before.length -ne $After.length -or
        $Before.lastWriteTimeUtc -ne $After.lastWriteTimeUtc -or
        $Before.hash -ne $After.hash
    $writtenDuringRun = $After.lastWriteTimeUtc -ge $RunStartedUtc.AddSeconds(-2)
    return $changed -and $writtenDuringRun
}

function Get-UnclassifiedLogErrors {
    param(
        [Parameter(Mandatory = $true)][string] $LogPath,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][string[]] $AllowedPatterns
    )

    $errors = [System.Collections.Generic.List[string]]::new()
    $seen = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    foreach ($line in [System.IO.File]::ReadLines($LogPath)) {
        if ($line -notmatch $GodotErrorHeaderPattern) {
            continue
        }

        $isAllowed = $false
        foreach ($pattern in $AllowedPatterns) {
            if ($line -match $pattern) {
                $isAllowed = $true
                break
            }
        }

        if (-not $isAllowed -and $errors.Count -lt 50 -and $seen.Add($line)) {
            $errors.Add($line)
        }
    }
    return @($errors)
}

function Initialize-RunScope {
    if ('GodotRunScope' -as [type]) { return }
    # Only the runner's execution unit is addressed. No process-name or Editor-wide kill.
    Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.Diagnostics;
using System.ComponentModel;
using System.Runtime.InteropServices;
public static class GodotRunScope {
    [StructLayout(LayoutKind.Sequential)] struct BasicLimits {
        public long ProcessTime, JobTime; public uint Flags;
        public UIntPtr MinWorkingSet, MaxWorkingSet; public uint ActiveLimit;
        public UIntPtr Affinity; public uint Priority, Scheduling;
    }
    [StructLayout(LayoutKind.Sequential)] struct IoCounters { public ulong A, B, C, D, E, F; }
    [StructLayout(LayoutKind.Sequential)] struct ExtendedLimits {
        public BasicLimits Basic; public IoCounters Io;
        public UIntPtr ProcessMemory, JobMemory, PeakProcessMemory, PeakJobMemory;
    }
    [StructLayout(LayoutKind.Sequential)] struct Accounting {
        public long UserTime, KernelTime, PeriodUserTime, PeriodKernelTime;
        public uint Faults, TotalProcesses, ActiveProcesses, TerminatedProcesses;
    }
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    static extern IntPtr CreateJobObject(IntPtr attributes, string name);
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    static extern IntPtr OpenJobObject(uint access, bool inherit, string name);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool SetInformationJobObject(IntPtr job, int kind, ref ExtendedLimits info, uint size);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool QueryInformationJobObject(IntPtr job, int kind, out Accounting info, uint size, IntPtr returned);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool AssignProcessToJobObject(IntPtr job, IntPtr process);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool TerminateJobObject(IntPtr job, uint exitCode);
    [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr handle);
    [DllImport("libc", SetLastError=true)] static extern int setsid();
    [DllImport("libc", SetLastError=true)] static extern int kill(int pid, int signal);
    [DllImport("libc", SetLastError=true)] static extern int getpgid(int pid);
    [DllImport("libc", SetLastError=true)] static extern long syscall(long number, int pid, uint flags);
    [StructLayout(LayoutKind.Sequential)] struct PollFd { public int Fd; public short Events, Returned; }
    [DllImport("libc", SetLastError=true)] static extern int poll(ref PollFd descriptor, UIntPtr count, int timeout);
    static void Check(bool success) { if (!success) throw new Win32Exception(Marshal.GetLastWin32Error()); }
    public static IntPtr Create(string name) {
        IntPtr job = CreateJobObject(IntPtr.Zero, name);
        Check(job != IntPtr.Zero);
        try {
            var limits = new ExtendedLimits();
            limits.Basic.Flags = 0x2000; // JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE; no breakaway.
            Check(SetInformationJobObject(job, 9, ref limits, (uint)Marshal.SizeOf<ExtendedLimits>()));
            return job;
        } catch { CloseHandle(job); throw; }
    }
    public static void Join(string name) {
        if (OperatingSystem.IsWindows()) {
            IntPtr job = OpenJobObject(1, false, name); // JOB_OBJECT_ASSIGN_PROCESS
            Check(job != IntPtr.Zero);
            try { Check(AssignProcessToJobObject(job, Process.GetCurrentProcess().Handle)); }
            finally { CloseHandle(job); } // The controller retains the only job handle.
        } else if (OperatingSystem.IsLinux()) {
            Check(setsid() == Environment.ProcessId);
        } else { throw new PlatformNotSupportedException("Runner supervision requires Windows or Linux."); }
    }
    public static int ObserveController(int pid) {
        var arch = RuntimeInformation.ProcessArchitecture;
        if (arch != Architecture.X64 && arch != Architecture.Arm64)
            throw new PlatformNotSupportedException("Linux pidfd supervision requires x64 or ARM64.");
        // SYS_pidfd_open is 434 on these architectures; requires Linux 5.3+, not a recent libc wrapper.
        int fd = (int)syscall(434, pid, 0);
        Check(fd >= 0);
        return fd;
    }
    public static bool ControllerExited(int fd) {
        var descriptor = new PollFd { Fd = fd, Events = 1 }; // POLLIN becomes ready on process exit.
        int result = poll(ref descriptor, (UIntPtr)1, 0);
        Check(result >= 0);
        return result > 0;
    }
    public static void Terminate(IntPtr job, int group) {
        if (OperatingSystem.IsWindows()) { Check(TerminateJobObject(job, 137)); }
        else {
            if (group <= 1 || group == getpgid(Environment.ProcessId)) throw new InvalidOperationException("Unsafe process group.");
            if (kill(-group, 9) != 0 && Marshal.GetLastWin32Error() != 3) Check(false); // ESRCH: already empty.
        }
    }
    public static void TerminateSupervisorGroup() {
        int group = Environment.ProcessId;
        if (group <= 1 || getpgid(group) != group) throw new InvalidOperationException("Supervisor does not own this group.");
        if (kill(-group, 9) != 0 && Marshal.GetLastWin32Error() != 3) Check(false);
    }
    public static bool Empty(IntPtr job, int group) {
        if (OperatingSystem.IsWindows()) {
            Accounting info;
            Check(QueryInformationJobObject(job, 1, out info, (uint)Marshal.SizeOf<Accounting>(), IntPtr.Zero));
            return info.ActiveProcesses == 0;
        }
        if (kill(-group, 0) != 0) {
            if (Marshal.GetLastWin32Error() == 3) return true;
            Check(false);
        }
        string ownNamespace = new FileInfo("/proc/self/ns/pid").LinkTarget;
        if (ownNamespace == null) throw new IOException("Cannot identify the PID namespace.");
        bool observedMember = false;
        foreach (string entry in Directory.EnumerateDirectories("/proc")) {
            int hostPid;
            if (!int.TryParse(Path.GetFileName(entry), out hostPid)) continue;
            try {
                // /proc may be mounted by an ancestor PID namespace. Never treat its directory IDs as local PIDs.
                if (new FileInfo(Path.Combine(entry, "ns/pid")).LinkTarget != ownNamespace) continue;
                string groupLine = Array.Find(File.ReadAllLines(Path.Combine(entry, "status")), line => line.StartsWith("NSpgid:"));
                if (groupLine == null) throw new IOException("Cannot read namespace process-group identity.");
                string[] ids = groupLine.Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
                if (int.Parse(ids[ids.Length - 1]) != group) continue;
                observedMember = true;
                string stat = File.ReadAllText(Path.Combine(entry, "stat"));
                char state = stat[stat.LastIndexOf(')') + 2];
                // Orphan zombies may await init's reaping, but can no longer execute.
                if (state != 'Z' && state != 'X') return false;
            } catch (FileNotFoundException) { }
              catch (DirectoryNotFoundException) { }
        }
        if (!observedMember && kill(-group, 0) == 0)
            throw new IOException("Process group exists but its members are not observable in this procfs view.");
        return true;
    }
    public static void Close(IntPtr job) { if (job != IntPtr.Zero) CloseHandle(job); }
}
'@
}

function Invoke-RunSupervisor {
    # Enter containment BEFORE starting the engine; assigning an already-running engine races its children.
    $payload = $env:GODOT_RUNNER_PAYLOAD | ConvertFrom-Json
    $env:GODOT_RUNNER_PAYLOAD = $null
    Initialize-RunScope
    [GodotRunScope]::Join($payload.jobName)
    $controllerHandle = if ($IsLinux) { [GodotRunScope]::ObserveController($payload.controllerPid) } else { -1 }
    $child = [Diagnostics.Process]::new()
    $stdoutFile = $null; $stderrFile = $null
    try {
        # The controller never writes. EOF means it exited, including abrupt termination.
        $controllerInput = [IO.StreamReader]::new([Console]::OpenStandardInput())
        $controllerClosed = $controllerInput.ReadLineAsync()
        $child.StartInfo = [Diagnostics.ProcessStartInfo]::new()
        $child.StartInfo.FileName = $payload.executable
        $child.StartInfo.WorkingDirectory = $payload.root
        $child.StartInfo.UseShellExecute = $false
        $child.StartInfo.RedirectStandardOutput = $true
        $child.StartInfo.RedirectStandardError = $true
        $child.StartInfo.RedirectStandardInput = $true
        foreach ($argument in $payload.arguments) { $child.StartInfo.ArgumentList.Add([string]$argument) }
        try {
            if ($controllerClosed.IsCompleted -or ($IsLinux -and [GodotRunScope]::ControllerExited($controllerHandle))) { return }
            $stdoutFile = [IO.File]::Open($payload.stdoutPath, 'CreateNew', 'Write', 'Read')
            $stderrFile = [IO.File]::Open($payload.stderrPath, 'CreateNew', 'Write', 'Read')
            [void]$child.Start()
            $child.StandardInput.Close()
            $outTask = $child.StandardOutput.BaseStream.CopyToAsync($stdoutFile)
            $errTask = $child.StandardError.BaseStream.CopyToAsync($stderrFile)
            while (-not $child.WaitForExit(100)) {
                if ($controllerClosed.IsCompleted -or ($IsLinux -and [GodotRunScope]::ControllerExited($controllerHandle))) { return }
            }
            # Send the native exit before collecting output, which a surviving descendant may hold open.
            [Console]::Out.WriteLine((@{ exitCode = $child.ExitCode } | ConvertTo-Json -Compress))
            [Console]::Out.Flush()
            $outputError = ''
            try {
                $drain = [Diagnostics.Stopwatch]::StartNew()
                while (-not $outTask.IsCompleted -or -not $errTask.IsCompleted) {
                    if ($controllerClosed.IsCompleted -or ($IsLinux -and [GodotRunScope]::ControllerExited($controllerHandle))) { return }
                    if ($drain.Elapsed.TotalSeconds -ge 5) { throw 'Child output pipes remain open; output collection cannot be confirmed complete.' }
                    Start-Sleep -Milliseconds 20
                }
                [void]$outTask.GetAwaiter().GetResult(); [void]$errTask.GetAwaiter().GetResult()
            }
            catch { $outputError = $_.Exception.Message }
            $stdoutFile.Flush(); $stderrFile.Flush()
            if (-not $outputError) {
                # A successful receipt must mean captures are closed and readable,
                # without relying on forced process termination to release writers.
                $stdoutFile.Dispose(); $stdoutFile = $null
                $stderrFile.Dispose(); $stderrFile = $null
            }
            [Console]::Out.WriteLine((@{ outputError = $outputError } | ConvertTo-Json -Compress))
            [Console]::Out.Flush()
        }
        catch {
            [Console]::Out.WriteLine((@{ launchError = $_.Exception.Message } | ConvertTo-Json -Compress))
            [Console]::Out.Flush()
        }
        # Keep the session leader alive after the engine exits, until controller cleanup or pipe closure.
        while (-not $controllerClosed.IsCompleted -and -not ($IsLinux -and [GodotRunScope]::ControllerExited($controllerHandle))) { Start-Sleep -Milliseconds 20 }
    }
    finally {
        # Kill before disposing redirected streams: a descendant can keep an async read pending.
        if ($IsLinux) { [GodotRunScope]::TerminateSupervisorGroup() }
        $child.Dispose()
        if ($null -ne $stdoutFile) { $stdoutFile.Dispose() }
        if ($null -ne $stderrFile) { $stderrFile.Dispose() }
        # Windows closes the controller's job handle on process exit, killing the entire job.
    }
}

if ($InternalSupervisor) { Invoke-RunSupervisor; exit 69 }

function Stop-ExecutionUnit {
    param([Diagnostics.Process] $Supervisor, [IntPtr] $Job)
    try {
        # Stop a supervisor still in startup before it can create an engine outside cleanup's observation.
        if (-not $Supervisor.HasExited) { $Supervisor.Kill() }
        [GodotRunScope]::Terminate($Job, $Supervisor.Id)
        $wait = [Diagnostics.Stopwatch]::StartNew()
        while (-not $Supervisor.HasExited -or -not [GodotRunScope]::Empty($Job, $Supervisor.Id)) {
            if ($wait.Elapsed.TotalSeconds -ge 5) { throw 'Cannot confirm the execution unit has no live processes after cleanup.' }
            [Threading.Thread]::Sleep(20)
        }
        return @{ confirmed = $true; error = '' }
    }
    catch { return @{ confirmed = $false; error = $_.Exception.Message } }
}

function Invoke-BoundedProcess {
    param([string] $Executable, [string[]] $Arguments, [string] $Root,
          [string] $LogPath, [string] $RunId)

    Initialize-RunScope
    if (-not $IsWindows -and -not $IsLinux) { throw 'The supervised process entrypoint currently supports only Windows and Linux.' }
    $engineExecutable = $Executable
    $engineArguments = @($Arguments)
    if ([System.IO.Path]::GetExtension($Executable) -eq '.ps1') {
        $engineExecutable = (Get-Process -Id $PID).Path
        $engineArguments = @('-NoProfile', '-File', $Executable) + $engineArguments
    }
    $jobName = "godot-run-$RunId"
    $info = [System.Diagnostics.ProcessStartInfo]::new()
    $info.FileName = (Get-Process -Id $PID).Path
    foreach ($arg in @('-NoProfile', '-File', $PSCommandPath, '-InternalSupervisor')) { $info.ArgumentList.Add($arg) }
    $info.Environment['GODOT_RUNNER_PAYLOAD'] = @{ executable = $engineExecutable; arguments = $engineArguments
        root = $Root; jobName = $jobName; controllerPid = $PID; stdoutPath = "$LogPath.$RunId.stdout.txt"
        stderrPath = "$LogPath.$RunId.stderr.txt" } | ConvertTo-Json -Compress
    $info.WorkingDirectory = $Root
    $info.UseShellExecute = $false
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    $info.RedirectStandardInput = $true
    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $info
    $stdoutPath = "$LogPath.$RunId.stdout.txt"
    $stderrPath = "$LogPath.$RunId.stderr.txt"
    $started = $false; $scopeStopped = $false; $job = [IntPtr]::Zero
    try {
        if ($IsWindows) { $job = [GodotRunScope]::Create($jobName) }
        $clock = [Diagnostics.Stopwatch]::StartNew()
        $started = $process.Start()
        $supervisorErrors = $process.StandardError.ReadToEndAsync()
        $reply = $process.StandardOutput.ReadLineAsync()
        $rawExitCode = $null; $timedOut = $false; $outputError = ''
        while (-not $reply.IsCompleted) {
            if ($clock.Elapsed.TotalSeconds -ge $TimeoutSeconds) { $timedOut = $true; break }
            if ($process.HasExited) { throw 'The process supervisor exited early; no engine result was obtained.' }
            Start-Sleep -Milliseconds 20
        }
        if (-not $timedOut) {
            $message = $reply.GetAwaiter().GetResult() | ConvertFrom-Json -AsHashtable
            if ($null -eq $message) { throw 'The process supervision channel closed; no engine result was obtained.' }
            if ($message.ContainsKey('launchError')) { throw $message.launchError }
            $rawExitCode = [int]$message.exitCode
            $outputReply = $process.StandardOutput.ReadLineAsync()
            $drain = [Diagnostics.Stopwatch]::StartNew()
            while (-not $outputReply.IsCompleted -and $drain.Elapsed.TotalSeconds -lt 5.5) {
                Start-Sleep -Milliseconds 20
            }
            if ($outputReply.IsCompleted) {
                try {
                    $outputMessage = $outputReply.GetAwaiter().GetResult() | ConvertFrom-Json -AsHashtable
                    if ($null -ne $outputMessage -and $outputMessage.ContainsKey('outputError')) { $outputError = $outputMessage.outputError }
                    else { $outputError = 'Output collection is incomplete; the supervision channel returned no valid result.' }
                } catch { $outputError = "Invalid output collection result: $($_.Exception.Message)" }
            } else { $outputError = 'Child output collection exceeded 5.5 seconds and cannot be confirmed complete.' }
        }
        else { $outputError = 'Run interrupted; output collection cannot be confirmed complete.' }
        $cleanup = Stop-ExecutionUnit $process $job
        $scopeStopped = $true
        return [ordered]@{ exitCode = $rawExitCode; timedOut = $timedOut
            termination = $(if ($cleanup.confirmed) { 'execution-unit-empty' } else { 'termination-unconfirmed' })
            cleanupConfirmed = $cleanup.confirmed; cleanupError = $cleanup.error
            processScope = $(if ($IsWindows) { 'windows-job' } else { 'linux-process-group' })
            supervisorPid = $process.Id
            outputError = $outputError
            stdoutPath = $stdoutPath; stderrPath = $stderrPath }
    }
    finally {
        if ($started -and -not $scopeStopped) { $null = Stop-ExecutionUnit $process $job }
        [GodotRunScope]::Close($job)
        $process.Dispose()
    }
}

function New-RunnerResult {
    param(
        [Parameter(Mandatory = $true)][string] $Status,
        [Parameter(Mandatory = $true)][string] $FailureKind,
        [AllowNull()][Nullable[int]] $GodotExitCode,
        [Parameter(Mandatory = $true)][int] $ExitCode,
        [string] $LogPath = '',
        [bool] $LogFresh = $false,
        [string[]] $UnclassifiedErrors = @(),
        [string[]] $EffectiveEngineArgs = @(),
        [string[]] $EffectiveUserArgs = @(),
        [string[]] $Messages = @()
    )

    return [ordered]@{
        run = $script:RunEvidence
        status = $Status
        failureKind = $FailureKind
        exitCode = $ExitCode
        godotExitCode = $GodotExitCode
        logPath = $LogPath
        logFresh = $LogFresh
        unclassifiedErrors = @($UnclassifiedErrors)
        engineArgs = @($EffectiveEngineArgs)
        userArgs = @($EffectiveUserArgs)
        messages = @($Messages)
    }
}

function Invoke-GodotRun {
    param(
        [Parameter(Mandatory = $true)][string] $Executable,
        [Parameter(Mandatory = $true)][string] $Root,
        [Parameter(Mandatory = $true)][string] $RunPurpose,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][string[]] $GodotArguments,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][string[]] $ProjectArguments,
        [string] $RequestedLogPath,
        [bool] $PermitExternalLog,
        [string] $ExternalReason,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][string[]] $AllowedPatterns
    )

    $script:RunEvidence = $null
    $runId = [guid]::NewGuid().ToString('N')
    try {
        if ([double]::IsNaN($TimeoutSeconds) -or [double]::IsInfinity($TimeoutSeconds) -or
            $TimeoutSeconds -le 0 -or $TimeoutSeconds -gt 2147483) {
            throw 'TimeoutSeconds must be finite, positive, and at most 2147483 seconds.'
        }
        Assert-ArgumentPartition -EngineArguments $GodotArguments -ProjectArguments $ProjectArguments -AllowedPatterns $AllowedPatterns
        $resolvedExecutable = Resolve-ExecutablePath -Executable $Executable
    }
    catch {
        return New-RunnerResult -Status 'blocked' -FailureKind 'arguments' `
            -GodotExitCode $null -ExitCode $RunnerExitCode.InvalidArguments -Messages @($_.Exception.Message)
    }

    $preflightScript = Join-Path $PSScriptRoot 'prepare_godot_log.ps1'
    if (-not (Test-Path -LiteralPath $preflightScript -PathType Leaf)) {
        return New-RunnerResult -Status 'blocked' -FailureKind 'preflight' `
            -GodotExitCode $null -ExitCode $RunnerExitCode.LogPreflight `
            -Messages @("Missing log preflight script: $preflightScript")
    }

    $preflightParameters = @{
        ProjectRoot = $Root
        Purpose = "$RunPurpose-$runId"
        RequestedLogFile = $RequestedLogPath
        Json = $true
        PathOnly = $true
        RunnerRunId = $runId
    }
    if ($PermitExternalLog) {
        $preflightParameters.AllowExternal = $true
        $preflightParameters.ExternalPathReason = $ExternalReason
    }

    $preflightOutput = @(& $preflightScript @preflightParameters)
    $preflightExitCode = $LASTEXITCODE
    $preflightText = $preflightOutput -join [System.Environment]::NewLine
    try {
        $preflight = $preflightText | ConvertFrom-Json
    }
    catch {
        return New-RunnerResult -Status 'blocked' -FailureKind 'preflight' `
            -GodotExitCode $null -ExitCode $RunnerExitCode.LogPreflight `
            -Messages @("Cannot parse log preflight result: $($_.Exception.Message)")
    }

    if ($preflightExitCode -ne 0 -or $preflight.status -ne 'path-validated') {
        return New-RunnerResult -Status 'blocked' -FailureKind 'preflight' `
            -GodotExitCode $null -ExitCode $RunnerExitCode.LogPreflight `
            -LogPath ([string]$preflight.logPath) -Messages @($preflight.blockers)
    }

    $effectiveEngineArgs = @('--path', [string]$preflight.projectRoot, '--log-file', [string]$preflight.logPath) + @($GodotArguments)
    $finalArguments = @($effectiveEngineArgs)
    if ($ProjectArguments.Count -gt 0) {
        $finalArguments += '--'
        $finalArguments += @($ProjectArguments)
    }

    $lock = $null
    try {
        # Persistent sidecar avoids unlink/recreate races; FileShare.None is the lease.
        $lockPath = "$($preflight.logPath).lock"
        $lockItem = Get-Item -LiteralPath $lockPath -Force -ErrorAction SilentlyContinue
        if ($null -ne $lockItem -and ($lockItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
            throw 'The log lock path must not be a link.'
        }
        $lock = [System.IO.File]::Open($lockPath, 'OpenOrCreate', 'ReadWrite', 'None')
        $lockCheck = @(& $preflightScript -ProjectRoot $Root -Purpose "$RunPurpose-$runId" `
            -RequestedLogFile $preflight.logPath -AllowExternal:$PermitExternalLog `
            -ExternalPathReason $ExternalReason -RunnerRunId $runId -Json) -join [Environment]::NewLine | ConvertFrom-Json
        if ($lockCheck.status -ne 'ready') { throw ($lockCheck.blockers -join '; ') }
    }
    catch {
        if ($null -ne $lock) { $lock.Dispose() }
        return New-RunnerResult -Status 'blocked' -FailureKind 'preflight' `
            -GodotExitCode $null -ExitCode $RunnerExitCode.LogPreflight -LogPath $preflight.logPath `
            -Messages @("Log path changed, is unwritable, or is held by another runner: $($_.Exception.Message)")
    }
    try {
        $beforeLog = Get-FileSnapshot -Path $preflight.logPath
        $runStartedUtc = [datetime]::UtcNow
        $script:RunEvidence = [ordered]@{ runId = $runId; startedUtc = $runStartedUtc.ToString('o')
            finishedUtc = $null; timedOut = $false; termination = 'starting'
            stdoutPath = "$($preflight.logPath).$runId.stdout.txt"
            stderrPath = "$($preflight.logPath).$runId.stderr.txt" }
        try {
            $run = Invoke-BoundedProcess -Executable $resolvedExecutable -Arguments $finalArguments `
                -Root $preflight.projectRoot -LogPath $preflight.logPath -RunId $runId
        }
        catch {
            $script:RunEvidence.finishedUtc = [datetime]::UtcNow.ToString('o')
            $script:RunEvidence.termination = 'launch-or-output-failure'
            return New-RunnerResult -Status 'failed' -FailureKind 'launch-or-output' `
                -GodotExitCode $null -ExitCode $RunnerExitCode.Launch -LogPath $preflight.logPath `
                -EffectiveEngineArgs $effectiveEngineArgs -EffectiveUserArgs $ProjectArguments `
                -Messages @($_.Exception.Message)
        }
        $godotExitCode = $run.exitCode
        $script:RunEvidence = [ordered]@{ runId = $runId; startedUtc = $runStartedUtc.ToString('o')
            finishedUtc = [datetime]::UtcNow.ToString('o'); timedOut = $run.timedOut
            termination = $run.termination; cleanupConfirmed = $run.cleanupConfirmed; cleanupError = $run.cleanupError
            processScope = $run.processScope; supervisorPid = $run.supervisorPid
            outputError = $run.outputError; stdoutPath = $run.stdoutPath; stderrPath = $run.stderrPath }
        if ($run.timedOut) {
            return New-RunnerResult -Status 'failed' -FailureKind 'timeout' `
                -GodotExitCode $godotExitCode -ExitCode $RunnerExitCode.Timeout -LogPath $preflight.logPath `
                -EffectiveEngineArgs $effectiveEngineArgs -EffectiveUserArgs $ProjectArguments `
                -Messages @("Run timed out; execution-unit cleanup state: $($run.termination).", $run.cleanupError)
        }

        if (-not $run.cleanupConfirmed) {
            $resultExit = if ($null -ne $godotExitCode -and $godotExitCode -ne 0) { $godotExitCode } else { $RunnerExitCode.Launch }
            return New-RunnerResult -Status 'failed' -FailureKind 'termination-unconfirmed' `
                -GodotExitCode $godotExitCode -ExitCode $resultExit -LogPath $preflight.logPath `
                -EffectiveEngineArgs $effectiveEngineArgs -EffectiveUserArgs $ProjectArguments `
                -Messages @($run.cleanupError)
        }

        if ($run.outputError) {
            $resultExit = if ($godotExitCode -ne 0) { $godotExitCode } else { $RunnerExitCode.Launch }
            return New-RunnerResult -Status 'failed' -FailureKind 'output-collection' `
                -GodotExitCode $godotExitCode -ExitCode $resultExit -LogPath $preflight.logPath `
                -EffectiveEngineArgs $effectiveEngineArgs -EffectiveUserArgs $ProjectArguments `
                -Messages @($run.outputError)
        }

        $messages = [System.Collections.Generic.List[string]]::new()
        foreach ($warning in @($preflight.warnings)) {
            $messages.Add([string]$warning)
        }
        $logFresh = $false
        $unclassifiedErrors = @()
        $seenErrors = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
        $source = @{ name = 'main log'; path = $preflight.logPath }
        try {
            $afterLog = Get-FileSnapshot -Path $preflight.logPath
            $logFresh = Test-FreshLog -Before $beforeLog -After $afterLog -RunStartedUtc $runStartedUtc
            $sources = @()
            if ($logFresh) { $sources += $source }
            # Capture files are created exclusively for this run and closed by the
            # supervisor before inspection. Empty files are valid; missing ones are not.
            $sources += @{ name = 'stdout'; path = $run.stdoutPath }
            $sources += @{ name = 'stderr'; path = $run.stderrPath }
            foreach ($source in $sources) {
                $errors = @(Get-UnclassifiedLogErrors -LogPath $source.path -AllowedPatterns $AllowedPatterns)
                if ($errors.Count -gt 0) {
                    $messages.Add("Current $($source.name) contains unclassified Godot errors: $($source.path)")
                    foreach ($errorLine in $errors) {
                        if ($unclassifiedErrors.Count -lt 50 -and $seenErrors.Add($errorLine)) {
                            $unclassifiedErrors += $errorLine
                        }
                    }
                }
            }
        }
        catch {
            $inspectionError = "Cannot read current $($source.name) '$($source.path)': $($_.Exception.Message)"
            $script:RunEvidence.outputError = $inspectionError
            $messages.Add($inspectionError)
            $resultExit = if ($godotExitCode -ne 0) { $godotExitCode } else { $RunnerExitCode.Launch }
            return New-RunnerResult -Status 'failed' -FailureKind 'output-collection' `
                -GodotExitCode $godotExitCode -ExitCode $resultExit -LogPath $preflight.logPath `
                -LogFresh $logFresh -UnclassifiedErrors $unclassifiedErrors `
                -EffectiveEngineArgs $effectiveEngineArgs -EffectiveUserArgs $ProjectArguments -Messages $messages
        }
        if (-not $logFresh) {
            $messages.Add('Godot log is missing, unchanged, or timestamped before this run.')
        }

        if ($godotExitCode -ne 0) {
            return New-RunnerResult -Status 'failed' -FailureKind 'godot-exit' `
                -GodotExitCode $godotExitCode -ExitCode $godotExitCode -LogPath $preflight.logPath `
                -LogFresh $logFresh -UnclassifiedErrors $unclassifiedErrors `
                -EffectiveEngineArgs $effectiveEngineArgs -EffectiveUserArgs $ProjectArguments -Messages $messages
        }
        if (-not $logFresh) {
            return New-RunnerResult -Status 'failed' -FailureKind 'stale-log' `
                -GodotExitCode $godotExitCode -ExitCode $RunnerExitCode.StaleLog -LogPath $preflight.logPath `
                -LogFresh $false -UnclassifiedErrors $unclassifiedErrors `
                -EffectiveEngineArgs $effectiveEngineArgs -EffectiveUserArgs $ProjectArguments -Messages $messages
        }
        if ($unclassifiedErrors.Count -gt 0) {
            return New-RunnerResult -Status 'failed' -FailureKind 'log-errors' `
                -GodotExitCode $godotExitCode -ExitCode $RunnerExitCode.LogErrors -LogPath $preflight.logPath `
                -LogFresh $true -UnclassifiedErrors $unclassifiedErrors `
                -EffectiveEngineArgs $effectiveEngineArgs -EffectiveUserArgs $ProjectArguments -Messages $messages
        }

        return New-RunnerResult -Status 'success' -FailureKind 'none' `
            -GodotExitCode $godotExitCode -ExitCode 0 -LogPath $preflight.logPath -LogFresh $true `
            -EffectiveEngineArgs $effectiveEngineArgs -EffectiveUserArgs $ProjectArguments -Messages $messages
    }
    finally { $lock.Dispose() }
}

function Write-RunnerResult {
    param([Parameter(Mandatory = $true)][System.Collections.IDictionary] $Result)

    if ($Json) {
        $Result | ConvertTo-Json -Depth 7
        return
    }

    Write-Output "Status: $($Result.status)"
    Write-Output "Failure kind: $($Result.failureKind)"
    Write-Output "Exit code: $($Result.exitCode)"
    Write-Output "Godot Exit code: $($Result.godotExitCode)"
    Write-Output "Log: $($Result.logPath)"
    Write-Output "Log belongs to current run: $($Result.logFresh)"
    if ($null -ne $Result.run) {
        Write-Output "Run ID: $($Result.run.runId)"
        Write-Output "Stdout: $($Result.run.stdoutPath)"
        Write-Output "Stderr: $($Result.run.stderrPath)"
    }
    foreach ($message in @($Result.messages)) {
        Write-Warning $message
    }
    foreach ($errorLine in @($Result.unclassifiedErrors)) {
        Write-Output "Unclassified log error: $errorLine"
    }
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
    $tempRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath()).TrimEnd('\', '/')
    $fixtureRoot = Join-Path $tempRoot ('godot runner fixture ' + [guid]::NewGuid().ToString('N'))
    try {
        New-Item -ItemType Directory -Path $fixtureRoot -Force | Out-Null
        [System.IO.File]::WriteAllText((Join-Path $fixtureRoot 'project.godot'), 'config_version=5')

        if ([System.Environment]::OSVersion.Platform -eq [System.PlatformID]::Win32NT -and $PSVersionTable.PSEdition -eq 'Desktop') {
            $fakeGodot = Join-Path $fixtureRoot 'fake godot.exe'
            $fakeGodotSource = @'
using System;
using System.IO;
using System.Linq;

public static class FakeGodotRunner
{
    public static int Main(string[] args)
    {
        int logIndex = Array.IndexOf(args, "--log-file");
        int pathIndex = Array.IndexOf(args, "--path");
        string logPath = logIndex >= 0 ? args[logIndex + 1] : "";
        string projectRoot = pathIndex >= 0 ? args[pathIndex + 1] : ".";
        File.WriteAllLines(Path.Combine(projectRoot, "received-args.txt"), args);
        bool skipLog = args.Contains("--fake-stale");
        bool writeError = args.Contains("--fake-error");
        bool writeAllowedError = args.Contains("--fake-allowed-error");
        if (!skipLog)
        {
            string content = "Godot Engine fake\n";
            if (writeError) content += "ERROR: fake project error\n";
            if (writeAllowedError) content += "ERROR: approved fake noise\n";
            File.WriteAllText(logPath, content);
        }
        if (args.Contains("--fake-stderr-error")) Console.Error.WriteLine("ERROR: fake stderr error");
        if (args.Contains("--fake-stdout-error")) Console.WriteLine("ERROR: fake stdout error");
        string exitArgument = args.FirstOrDefault(value => value.StartsWith("--fake-exit=", StringComparison.Ordinal));
        return exitArgument == null ? 0 : int.Parse(exitArgument.Substring("--fake-exit=".Length));
    }
}
'@
            Add-Type -TypeDefinition $fakeGodotSource -OutputAssembly $fakeGodot -OutputType ConsoleApplication
        }
        else {
            $fakeGodot = Join-Path $fixtureRoot 'fake godot.ps1'
            $fakeGodotSource = @'
$logIndex = [array]::IndexOf($args, '--log-file')
$pathIndex = [array]::IndexOf($args, '--path')
$logPath = if ($logIndex -ge 0) { $args[$logIndex + 1] } else { '' }
$projectRoot = if ($pathIndex -ge 0) { $args[$pathIndex + 1] } else { '.' }
[System.IO.File]::WriteAllLines((Join-Path $projectRoot 'received-args.txt'), [string[]]$args)
$skipLog = $args -contains '--fake-stale'
$writeError = $args -contains '--fake-error'
$writeAllowedError = $args -contains '--fake-allowed-error'
if (-not $skipLog) {
    $content = "Godot Engine fake`n"
    if ($writeError) { $content += "ERROR: fake project error`n" }
    if ($writeAllowedError) { $content += "ERROR: approved fake noise`n" }
    [System.IO.File]::WriteAllText($logPath, $content)
}
if ($args -contains '--fake-stderr-error') { [Console]::Error.WriteLine('ERROR: fake stderr error') }
if ($args -contains '--fake-stdout-error') { [Console]::Out.WriteLine('ERROR: fake stdout error') }
$exitArgument = $args | Where-Object { $_ -like '--fake-exit=*' } | Select-Object -First 1
if ($null -ne $exitArgument) { exit [int]($exitArgument -replace '^--fake-exit=', '') }
exit 0
'@
            [System.IO.File]::WriteAllText($fakeGodot, $fakeGodotSource)
        }

        $success = Invoke-GodotRun -Executable $fakeGodot -Root $fixtureRoot -RunPurpose 'success' `
            -GodotArguments @('--headless', '--scene', 'res://scene with spaces.tscn') `
            -ProjectArguments @('--custom-value', 'value with spaces') -RequestedLogPath '' `
            -PermitExternalLog $false -ExternalReason '' -AllowedPatterns @()
        Assert-SelfTest -Condition ($success.exitCode -eq 0 -and $success.logFresh) `
            -Message "Successful runs must return fresh logs and zero exit status; actual exit=$($success.exitCode) kind=$($success.failureKind) messages=$($success.messages -join '; ')."
        $receivedArgs = @(Get-Content -LiteralPath (Join-Path $fixtureRoot 'received-args.txt'))
        $separatorIndex = [array]::IndexOf($receivedArgs, '--')
        Assert-SelfTest -Condition ($separatorIndex -gt 0) -Message 'UserArgs require the -- separator.'
        Assert-SelfTest -Condition ($receivedArgs[$separatorIndex + 2] -eq 'value with spaces') -Message 'UserArgs containing spaces must remain single arguments.'

        $invalid = Invoke-GodotRun -Executable $fakeGodot -Root $fixtureRoot -RunPurpose 'invalid' `
            -GodotArguments @('--path', $fixtureRoot) -ProjectArguments @() -RequestedLogPath '' `
            -PermitExternalLog $false -ExternalReason '' -AllowedPatterns @()
        Assert-SelfTest -Condition ($invalid.exitCode -eq $RunnerExitCode.InvalidArguments) -Message 'Duplicate --path must be blocked by argument validation.'

        $rawExit = Invoke-GodotRun -Executable $fakeGodot -Root $fixtureRoot -RunPurpose 'raw-exit' `
            -GodotArguments @('--fake-exit=23') -ProjectArguments @() -RequestedLogPath '' `
            -PermitExternalLog $false -ExternalReason '' -AllowedPatterns @()
        Assert-SelfTest -Condition ($rawExit.exitCode -eq 23 -and $rawExit.godotExitCode -eq 23) -Message 'Nonzero Godot exit codes must propagate unchanged.'

        $initialStale = Invoke-GodotRun -Executable $fakeGodot -Root $fixtureRoot -RunPurpose 'stale' `
            -GodotArguments @() -ProjectArguments @() -RequestedLogPath '' `
            -PermitExternalLog $false -ExternalReason '' -AllowedPatterns @()
        Assert-SelfTest -Condition ($initialStale.exitCode -eq 0) -Message "The stale-log fixture initial run must succeed: $($initialStale | ConvertTo-Json -Depth 8 -Compress)"
        $stale = Invoke-GodotRun -Executable $fakeGodot -Root $fixtureRoot -RunPurpose 'stale' `
            -GodotArguments @('--fake-stale') -ProjectArguments @() -RequestedLogPath '' `
            -PermitExternalLog $false -ExternalReason '' -AllowedPatterns @()
        Assert-SelfTest -Condition ($stale.exitCode -eq $RunnerExitCode.StaleLog) -Message 'Unrefreshed logs must fail.'

        $logError = Invoke-GodotRun -Executable $fakeGodot -Root $fixtureRoot -RunPurpose 'error' `
            -GodotArguments @('--fake-error') -ProjectArguments @() -RequestedLogPath '' `
            -PermitExternalLog $false -ExternalReason '' -AllowedPatterns @()
        Assert-SelfTest -Condition ($logError.exitCode -eq $RunnerExitCode.LogErrors) -Message 'Unclassified log errors must fail.'

        foreach ($channel in @('stdout', 'stderr')) {
            $streamError = Invoke-GodotRun -Executable $fakeGodot -Root $fixtureRoot -RunPurpose "$channel-error" `
                -GodotArguments @("--fake-$channel-error") -ProjectArguments @() -RequestedLogPath '' `
                -PermitExternalLog $false -ExternalReason '' -AllowedPatterns @()
            Assert-SelfTest -Condition ($streamError.exitCode -eq $RunnerExitCode.LogErrors -and $streamError.godotExitCode -eq 0) `
                -Message "Errors only in $channel must fail even with a fresh clean main log and native exit zero."
        }

        $allowedError = Invoke-GodotRun -Executable $fakeGodot -Root $fixtureRoot -RunPurpose 'allowed-error' `
            -GodotArguments @('--fake-allowed-error') -ProjectArguments @() -RequestedLogPath '' `
            -PermitExternalLog $false -ExternalReason '' -AllowedPatterns @('^ERROR: approved fake noise$')
        Assert-SelfTest -Condition ($allowedError.exitCode -eq 0) -Message 'Explicitly allowlisted log errors must be classified.'

        if (-not [string]::IsNullOrWhiteSpace($GodotExecutable)) {
            $realFixtureRoot = Join-Path $fixtureRoot 'real godot project'
            New-Item -ItemType Directory -Path $realFixtureRoot -Force | Out-Null
            $projectConfig = @'
config_version=5

[application]
run/main_scene="res://main.tscn"
'@
            $mainScene = @'
[gd_scene format=3]

[node name="Main" type="Node"]
'@
            [System.IO.File]::WriteAllText((Join-Path $realFixtureRoot 'project.godot'), $projectConfig)
            [System.IO.File]::WriteAllText((Join-Path $realFixtureRoot 'main.tscn'), $mainScene)

            $realImport = Invoke-GodotRun -Executable $GodotExecutable -Root $realFixtureRoot -RunPurpose 'real-import' `
                -GodotArguments @('--headless', '--import') -ProjectArguments @() -RequestedLogPath '' `
                -PermitExternalLog $false -ExternalReason '' -AllowedPatterns @($AllowedLogErrorPattern)
            Write-Output ('Real import validation: ' + (@{ result = $realImport; log = $(if (Test-Path -LiteralPath $realImport.logPath -PathType Leaf) { Get-Content -LiteralPath $realImport.logPath -Raw }) } | ConvertTo-Json -Depth 8 -Compress))
            Assert-SelfTest -Condition ($realImport.exitCode -eq 0) -Message "Real Godot --headless --import failed: $($realImport.messages -join '; ')"

            $realScene = Invoke-GodotRun -Executable $GodotExecutable -Root $realFixtureRoot -RunPurpose 'real-scene' `
                -GodotArguments @('--headless', '--scene', 'res://main.tscn', '--quit-after', '1') `
                -ProjectArguments @() -RequestedLogPath '' -PermitExternalLog $false -ExternalReason '' `
                -AllowedPatterns @($AllowedLogErrorPattern)
            Write-Output ('Real scene validation: ' + (@{ result = $realScene; log = $(if (Test-Path -LiteralPath $realScene.logPath -PathType Leaf) { Get-Content -LiteralPath $realScene.logPath -Raw }) } | ConvertTo-Json -Depth 8 -Compress))
            Assert-SelfTest -Condition ($realScene.exitCode -eq 0) -Message "Real Godot scene run failed: $($realScene.messages -join '; ')"
        }

        Write-Output 'Self-test: passed'
        exit 0
    }
    finally {
        if ((Test-Path -LiteralPath $fixtureRoot) -and $fixtureRoot.StartsWith($tempRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
            Remove-Item -LiteralPath $fixtureRoot -Recurse -Force
        }
    }
}

$result = Invoke-GodotRun -Executable $GodotExecutable -Root $ProjectRoot -RunPurpose $Purpose `
    -GodotArguments @($EngineArgs) -ProjectArguments @($UserArgs) -RequestedLogPath $RequestedLogFile `
    -PermitExternalLog $AllowExternalLog.IsPresent -ExternalReason $ExternalLogReason `
    -AllowedPatterns @($AllowedLogErrorPattern)
Write-RunnerResult -Result $result
exit $result.exitCode
