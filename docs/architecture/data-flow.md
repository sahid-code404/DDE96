# Glasswave Desktop - Data Flow & System Interactions

## 1. Overview
This document illustrates how configuration data, desktop events, and system interactions flow across Glasswave Desktop components, KDE Plasma, KWin, and underlying Linux kernel subsystems.

## 2. Configuration & State Flow

```
[User Action in Glasswave Settings GUI]
                |
                v
  [SettingsManager.set(key, value)]
                |
                +---> [Validate against schema.json]
                |             |
                |             +--> (If invalid: raise ValidationError & rollback)
                |
                +---> [Create Pre-Migration Backup (~/.config/glasswave/backups/)]
                |
                +---> [Atomic Write to ~/.config/glasswave/glasswave.json]
                |       (write to .tmp + os.replace)
                |
                +---> [Synchronize to KDE Plasma & KWin via DBus / KConfig]
                        |
                        +--> kwriteconfig6 --file kwinrc ...
                        +--> kwriteconfig6 --file kdeglobals ...
                        +--> qdbus org.kde.KWin /KWin reconfigure
```

## 3. Desktop Shell & Dock Event Flow

```
[Mouse Pointer Enters Dock Area]
                |
                v
[Dock QML / Companion: Calculate Gaussian/Cosine Magnification Factor]
                |
                +---> Smooth GPU scale transform on hovered item (1.0x -> 1.4x)
                +---> Adjacent items scale proportionately (1.0x -> 1.2x)
                |
[User Clicks Pinned Application (e.g. glasswave-files)]
                |
                v
[Check Process Table / DBus for Existing Instance]
                |
                +---> If Running:
                |       Call org.freedesktop.Application.Activate() via DBus
                |       or KWin activateWindow()
                |
                +---> If Not Running:
                        Trigger bounce launch animation
                        Spawn process via GAppInfo / QProcess (unprivileged)
                        Add running dot indicator once process ID appears
```

## 4. File Operations & Trash Data Flow

```
[User Trashes File in glasswave-files]
                |
                v
[Verify Source Path within Allowed POSIX Namespace]
                |
                v
[Check FreeDesktop Trash (~/.local/share/Trash)]
                |
                +---> Move payload to ~/.local/share/Trash/files/<name>
                +---> Write metadata to ~/.local/share/Trash/info/<name>.trashinfo
                |       (Records original path and deletion timestamp)
                |
[Update File View & Refresh Trash Dock Icon State (Empty -> Full)]
```

## 5. System Monitor Data Flow

```
[Timer Tick (1 Hz)]
        |
        +---> Read /proc/stat       --> Compute Delta CPU Jiffies (User, System, Idle)
        +---> Read /proc/meminfo    --> MemTotal, MemAvailable, Buffers, Cached
        +---> Read /proc/diskstats  --> Read/Write Sectors Throughput
        +---> Iterate /proc/[pid]/  --> PID, Name, State, RSS Memory
                |
                +---> Gracefully handle PermissionError (honestly marked as System Process)
                |
[Update UI Model & Render Graphs via Cairo / GTK]
```
