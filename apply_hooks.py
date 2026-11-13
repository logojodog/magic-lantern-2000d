#!/usr/bin/env python3
"""Apply ultra-passive M-Film hooks to the 2000D source.

Only key + overlay hooks. No menu changes. Diagnostic is log-only.
"""

import sys
from pathlib import Path

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not (root / "src" / "gui-common.c").exists():
        print("ERROR: not a Magic Lantern source tree")
        sys.exit(1)

    def edit(rel, old, new, marker):
        p = root / rel
        text = p.read_text(encoding="utf-8", errors="replace")
        if marker in text:
            print(f"  {rel}: already applied")
            return
        if old not in text:
            print(f"  {rel}: WARNING – anchor not found")
            return
        p.write_text(text.replace(old, new, 1), encoding="utf-8")
        print(f"  {rel}: patched")

    print("Applying ultra-passive M-Film hooks…")

    # 1. Key hook
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

    # 3. Copy filmhook.c into src/
    src_hook = root / "filmhook.c"
    dst_hook = root / "src" / "filmhook.c"
    if not src_hook.exists():
        print("ERROR: filmhook.c missing from repo root")
        sys.exit(1)
    dst_hook.write_text(src_hook.read_text(encoding="utf-8"), encoding="utf-8")
    print("  src/filmhook.c: written")

    # 4. Header
    (root / "src" / "filmroll.h").write_text(
        "#ifndef _FILMROLL_H_\n"
        "#define _FILMROLL_H_\n"
        "struct event;\n"
        "int handle_filmroll_keys(struct event *event);\n"
        "int filmroll_overlays_active(void);\n"
        "#endif\n",
        encoding="utf-8"
    )
    print("  src/filmroll.h: written")

    # 5. Compile filmhook.o
    edit("src/Makefile.src",
         "gui-common.o \\\n",
         "gui-common.o \\\n"
         "filmhook.o \\\n",
         "filmhook.o")

    # 6. FEATURE_FILMROLL
    for plat in ["platform/2000D.121", "platform/2000D.110"]:
        feat = root / plat / "features.h"
        if not feat.exists():
            continue
        text = feat.read_text(encoding="utf-8", errors="replace")
        if "FEATURE_FILMROLL" not in text:
            text += "\n#define FEATURE_FILMROLL\n"
            feat.write_text(text, encoding="utf-8")
            print(f"  {plat}/features.h: FEATURE_FILMROLL added")
        else:
            print(f"  {plat}/features.h: already has FEATURE_FILMROLL")

    print("\nDone – ultra-passive hooks ready.")

if __name__ == "__main__":
    main()
