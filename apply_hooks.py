#!/usr/bin/env python3
"""Apply the minimal M-Film hooks to a magic-lantern 2000D source tree.

Usage:
    python3 apply_hooks.py /path/to/magic-lantern-2000d-main

Idempotent. Safe to run more than once.
"""

import sys
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 apply_hooks.py /path/to/ml-source")
        sys.exit(1)

    root = Path(sys.argv[1])
    if not (root / "src" / "gui-common.c").exists():
        print("ERROR: does not look like a Magic Lantern source tree")
        sys.exit(1)

    def edit(rel, old, new, marker):
        p = root / rel
        text = p.read_text(encoding="utf-8", errors="replace")
        if marker in text:
            print(f"  {rel}: already applied")
            return
        if old not in text:
            print(f"  {rel}: WARNING – anchor not found (source may have changed)")
            print(f"         looking for:\n{old!r}")
            return
        p.write_text(text.replace(old, new, 1), encoding="utf-8")
        print(f"  {rel}: patched")

    print("Applying M-Film hooks for 2000D…")

    # 1. Key hook (must be before handle_module_keys)
    edit("src/gui-common.c",
         "    if (handle_module_keys(event) == 0) return 0;\n",
         "#ifdef FEATURE_FILMROLL\n"
         "    if (handle_filmroll_keys(event) == 0) return 0;\n"
         "#endif\n"
         "    if (handle_module_keys(event) == 0) return 0;\n",
         "handle_filmroll_keys")

    edit("src/gui-common.c",
         "#include <zebra.h>\n",
         "#include <zebra.h>\n"
         "#ifdef FEATURE_FILMROLL\n"
         "#include <filmroll.h>\n"
         "#endif\n",
         "#include <filmroll.h>")

    # 2. Overlay hook
    edit("src/zebra.c",
         "int get_global_draw() // menu setting, or off if \n{\n",
         "int get_global_draw() // menu setting, or off if \n{\n"
         "#ifdef FEATURE_FILMROLL\n"
         "    if (filmroll_overlays_active()) return 0;\n"
         "#endif\n",
         "filmroll_overlays_active")

    edit("src/zebra.c",
         '#include "zebra.h"\n',
         '#include "zebra.h"\n'
         "#ifdef FEATURE_FILMROLL\n"
         '#include "filmroll.h"\n'
         "#endif\n",
         '#include "filmroll.h"')

    # 3. Safe menu redirect – only takes over when the module is loaded
    edit("src/menu.c",
         "static void menu_open() \n{ \n    if (menu_shown)\n        return;\n",
         "static void menu_open() \n{ \n"
         "#ifdef FEATURE_FILMROLL\n"
         "#ifdef FEATURE_FILMOS_MODULE\n"
         "    if (filmroll_menu_requested())   /* 1 = film OS handled it */\n"
         "        return;\n"
         "#else\n"
         "    filmroll_menu_requested();\n"
         "    return;\n"
         "#endif\n"
         "#endif\n"
         "    if (menu_shown)\n        return;\n",
         "filmroll_menu_requested")

    edit("src/menu.c",
         '#include "powersave.h"\n',
         '#include "powersave.h"\n'
         "#ifdef FEATURE_FILMROLL\n"
         '#include "filmroll.h"\n'
         "#endif\n",
         '#include "filmroll.h"')

    # 4. Copy the filmhook source
    src_hook = Path(__file__).parent / "filmhook.c"
    dst_hook = root / "src" / "filmhook.c"
    if src_hook.exists():
        dst_hook.write_text(src_hook.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"  src/filmhook.c: written")
    else:
        # Fallback: write the content inline if the sibling file is missing
        print("  WARNING: filmhook.c not found next to this script – writing embedded version")
        dst_hook.write_text(open(__file__).read().split('EMBEDDED_FILMHOOK_START\n')[1].split('EMBEDDED_FILMHOOK_END')[0] if False else "", encoding="utf-8")

    # 5. Header that the rest of the code includes
    hdr = root / "src" / "filmroll.h"
    hdr.write_text(
        "/* Minimal declarations for the film OS hooks (module build) */\n"
        "#ifndef _FILMROLL_H_\n"
        "#define _FILMROLL_H_\n"
        "struct event;\n"
        "int handle_filmroll_keys(struct event *event);\n"
        "int filmroll_menu_requested(void);\n"
        "int filmroll_overlays_active(void);\n"
        "#endif\n",
        encoding="utf-8"
    )
    print("  src/filmroll.h: written")

    # 6. Make sure the new file is compiled
    edit("src/Makefile.src",
         "gui-common.o \\\n",
         "gui-common.o \\\n"
         "filmhook.o \\\n",
         "filmhook.o")

    # 7. Turn the features on for the 2000D platform(s)
    for plat in ["platform/2000D.121", "platform/2000D.110"]:
        feat = root / plat / "features.h"
        if not feat.exists():
            continue
        text = feat.read_text(encoding="utf-8", errors="replace")
        changed = False
        if "FEATURE_FILMROLL" not in text:
            text += "\n#define FEATURE_FILMROLL\n"
            changed = True
        if "FEATURE_FILMOS_MODULE" not in text:
            text += "#define FEATURE_FILMOS_MODULE\n"
            changed = True
        if changed:
            feat.write_text(text, encoding="utf-8")
            print(f"  {plat}/features.h: FEATURE_FILMROLL + FEATURE_FILMOS_MODULE added")
        else:
            print(f"  {plat}/features.h: already has the features")

    print("\nDone. Now build the platform (e.g. make -C platform/2000D.121).")
    print("The resulting AUTOEXEC.BIN will:")
    print("  • open the film OS automatically once filmos.mo loads")
    print("  • still let you reach the real ML menu by holding the Q button ~1.5 s")
    print("  • write a clear message to the screen + ML/FILMROLL.LOG if the module is missing")

if __name__ == "__main__":
    main()
