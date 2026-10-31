# Magic Lantern for Canon EOS 2000D / Rebel T7 / Kiss X90 (Firmware 1.2.1)

[![Platform](https://img.shields.io/badge/Platform-Canon%20EOS%202000D%20%7C%20Rebel%20T7%20%7C%20Kiss%20X90-blue.svg)](https://github.com/dodoloiu1/magic-lantern-2000d)
[![Firmware](https://img.shields.io/badge/Firmware-1.2.1-brightgreen.svg)](https://github.com/dodoloiu1/magic-lantern-2000d)
[![Architecture](https://img.shields.io/badge/Architecture-DIGIC%204%2B%20%28ARMv5TE%29-orange.svg)](https://github.com/dodoloiu1/magic-lantern-2000d)
[![DryOS](https://img.shields.io/badge/DryOS-2.4.3%2020%2803%29-purple.svg)](https://github.com/dodoloiu1/magic-lantern-2000d)
[![Hardware Status](https://img.shields.io/badge/Status-Hardware%20%26%20QEMU%20Verified-success.svg)](https://github.com/dodoloiu1/magic-lantern-2000d)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](LICENSE)

This repository contains the first working **Magic Lantern** port for the **Canon EOS 2000D** (also known as the **Canon EOS Rebel T7**, **Kiss X90**, or internal model code **K432** / `0x432`) running **Firmware 1.2.1**.

Both emulator testing in `qemu-eos` and physical hardware execution on a live camera have been completed and verified.

---

## 📸 Overview

The Canon EOS 2000D was previously considered difficult or unsupported due to its DIGIC 4+ processor architecture, revised 24.1-megapixel memory pool layout, relocated HIVECS boot block, and updated DryOS 2.4.3 operating system.

This port resolves all missing and relocated stubs, fixes memory configuration and cache-hack jump vectors, and compiles clean `AUTOEXEC.BIN` binaries and loadable modules.

```
       +-------------------------------------------------------------+
       |                  Canon EOS 2000D / Rebel T7                 |
       |  Procesor: DIGIC 4+ ARMv5TE  |  Model ID: 0x432 (0x80000432)|
       |  Firmware: 1.2.1             |  ROM Base: 0xFE0C0000        |
       +-------------------------------------------------------------+
                                      |
                     [Bootloader in ROM @ 0xFFFF0000]
                                      |
                     Is NVRAM BOOTDISK == 1 and SD bootable?
                                     / \
                               YES  /   \  NO / Card Missing
                                   /     \
    [Load AUTOEXEC.BIN to RAM 0x800000]   [Boot Stock Firmware @ 0xFE0C0000]
    [Magic Lantern Menu via TRASH Key]    [100% Factory Canon Operation]
```

---

## ⚡ Verified Features & Working Modules

- **Magic Lantern GUI:** Toggled via the **Trash / Delete** button (`CONFIG_MENU_WITH_AV`), full navigation with directional keys and `SET`.
- **Overlay Suite:**
  - Focus Peaking (color, threshold, filter selection)
  - Zebras (overexposure & underexposure warnings)
  - False Color
  - Spotmeter & Vectorscope
  - Cropmarks & Custom Overlays
- **Shoot Menu:**
  - Advanced Intervalometer (timelapse automation)
  - Bulb Timer & Audio Remotes
  - Trap Focus (auto-shutter on focus confirmation)
  - Motion Detection
- **Modules (`.mo`):**
  - `dual_iso.mo` — Dual ISO dynamic range expansion (100/800, 100/1600, etc.)
  - `autoexpo.mo` — Auto Exposure & ETTR (Expose To The Right)
  - `file_man.mo` — On-camera file manager
  - `bench.mo` — CPU, cache, memory, and EDMAC benchmarks
  - `arkanoid.mo` — Classic game engine running directly on DIGIC 4+
- **Diagnostics:**
  - Real-time internal temperature monitoring
  - Precise shutter actuation counter
  - Memory & DryOS task inspector

---

## 🛡️ Zero-Brick Safety Guarantee (Hardware Architecture)

Magic Lantern **never** overwrites the camera's original flash firmware.

1. **Hardware Fallback in ROM:** The primary bootloader is stored in physical read-only ROM (`0xFFFF0000` / `0xFE010000`). It checks if the inserted SD card contains the `EOS_DEVELOP` + `BOOTDISK` signatures and a valid `AUTOEXEC.BIN`.
2. **Volatile RAM Execution:** Magic Lantern code is copied into temporary RAM (`0x800000`) and executes alongside DryOS.
3. **Instant Reversion to Stock:**
   - Removing the SD card immediately restores **100% factory Canon operation**.
   - Inserting any regular SD card boots stock Canon firmware.
   - Holding down the `SET` button while powering on the camera bypasses Magic Lantern loading.
   - Formatting the card removes all ML code.

---

## 🚀 Installation Guide

### Prerequisites
- Canon EOS 2000D / Rebel T7 / Kiss X90 camera on official **Firmware 1.2.1**.
- SD Card formatted as **FAT32** (32 GB or smaller recommended for easiest setup).
- Standard USB cable (mini-USB to USB-A or Type-C).

### Step 1: Prepare the SD Card
1. Download the latest release package (`ML_2000D_121.zip`) from the [Releases](https://github.com/dodoloiu1/magic-lantern-2000d/releases) tab.
2. Extract the contents directly to the root of your FAT32 SD card:
   ```
   SD_CARD:\
   ├── AUTOEXEC.BIN
   └── ML\
       ├── cropmks\
       ├── data\
       ├── doc\
       ├── fonts\
       ├── logs\
       ├── modules\
       ├── scripts\
       └── settings\
   ```
3. Make the card bootable by writing `EOS_DEVELOP` at offset `0x47` and `BOOTDISK` at offset `0x5C` of the FAT32 boot sector (can be done with `mlinstall`, `make_bootable.py`, or `EOScard`).

### Step 2: Enable Camera Boot Flag via USB
Because the 2000D does not yet have a standard `.FIR` installer package, the internal boot flag is enabled safely via standard Canon PTP over USB:

1. Connect the camera to your computer via USB (without SD card or with SD card inserted).
2. Set the mode dial to **P** or **M** and turn the camera **ON**.
3. Launch [`mlinstall`](https://github.com/petabyt/mlinstall) (v1.1.1 is recommended for Windows).
4. Navigate to the **USB** tab and click **"Connect to Camera"** (the tool connects via PTP and identifies `Canon EOS 2000D`).
5. Click **"Enable Custom Boot"** (this calls Canon's built-in `EnableBootDisk` event procedure to toggle the NVRAM flag).
6. Turn the camera **OFF** and disconnect the USB cable.

### Step 3: First Boot
1. Insert the prepared SD card into the camera and securely **close the battery/card door**.
2. Turn the camera **ON**. The card activity LED will flash briefly as `AUTOEXEC.BIN` is loaded.
3. The camera boots to the normal Canon shooting screen.
4. Press the **Trash / Delete (🗑️)** button — the Magic Lantern menu will appear on screen!

*(To uninstall or revert at any time: simply remove the card, or reconnect via USB and click "Disable Custom Boot" in `mlinstall`).*

---

## 🔬 Technical Reverse-Engineering Highlights

### 1. Memory Map & Single ROM Chip
Unlike older cameras with dual 16 MB chips (`ROM0` at `0xF0000000` and `ROM1` at `0xF8000000`), the 2000D utilizes a single **32 MB Flash ROM** mapped across `0xFE000000..0xFFFFFFFF`:
- **Firmware Base:** `ROMBASEADDR = 0xFE0C0000`
- **Boot Block (HIVECS):** Resides in ROM at `0xFE010000..0xFE01FFFF` and is hardware-mapped to `0xFFFF0000`.
- **NVRAM Shadow:** `0xF8000000` (`[0xF8000004]` = `BOOTDISK` flag).

### 2. RAM Sizing for 24 MP Sensor
The 2000D features a 24.1 MP sensor which allocates the ExMem pool at uncached address `0x5540001C` (`0x40000000` + `0x15400000`), requiring a **512 MB RAM configuration (`0x20000000`)** rather than the 256 MB used on the 1300D.

### 3. Critical Stubs & Pointers (Firmware 1.2.1)
All 169 platform stubs were verified against the 1.2.1 ROM dump:
- `task_dispatch_hook`: `0x3592C`
- `task_max`: `0x358F0`
- `_alloc_dma_memory`: `0xFE2C254C`
- `DISPLAY_STATEOBJ`: `0x318BC` (resolved via `0xFE116B80`)
- `INPUT_ENABLE_IMAGE_PHYSICAL_SCREEN_PARAMETER`: `22` (in `DispState` table at `0xFE875224`)
- `gui_task_list`: `0x3D914` (verified in `gui_task_create` at `0xFE3EF348`)
- `LV_BOTTOM_BAR_STATE`: `0x3AA08 + 0x3C` (at `0xFE2E0D28`)
- `WINSYS_BMP_DIRTY_BIT_NEG`: `0x3DA64 + 0x2C`
- `BFNT_CHAR_CODES`: `0xFF23EACC`

---

## 🛠️ Building from Source

### Toolchain Setup
Requires `arm-none-eabi-gcc` (GCC 10 or newer with UCRT64 / MSYS2 / Linux) and Python 3.

```bash
# Clone the repository
git clone https://github.com/dodoloiu1/magic-lantern-2000d.git
cd magic-lantern-2000d

# Build modules
cd modules
make -j$(nproc)
cd ..

# Build 2000D 1.2.1 platform binary
cd platform/2000D.121
make clean
make
```

The compiled `autoexec.bin` (approx. 365 KB) will be output in `platform/2000D.121/`.

---

## 🤝 Credits & Acknowledgements

- **The Magic Lantern Project & Community** ([magiclantern.fm](https://www.magiclantern.fm/))
- **Trammell Hudson** — Original creator of Magic Lantern
- **a1ex** — Core architectural design, reverse-engineering, and QEMU emulator
- **critix** — Initial 1300D / 2000D exploration and branch maintenance
- **kitor** — Digic 4+ hardware reverse engineering and QEMU support
- **petabyt** — Author of `mlinstall` and modern PTP toolchains
- **Lungu Răzvan-Tudor (dodoloiu1)** — 2000D 1.2.1 port calibration, 169 stub verifications, and physical hardware validation

---

## ⚖️ Disclaimer

Magic Lantern is free, open-source software licensed under the **GNU General Public License v2 (GPLv2)**.  
It is not affiliated with or endorsed by Canon Inc. Use at your own risk.
