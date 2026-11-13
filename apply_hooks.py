#!/usr/bin/env python3
"""Add M-Film's hooks to the Magic Lantern 2000D (T7) source tree.

    python3 apply_hooks.py <path to the magic-lantern-2000d folder>

What M-Film's film OS (ML/modules/filmos.mo) needs from autoexec.bin:

  handle_filmroll_keys()      called from the key handler, ahead of the modules,
                              so the film OS gets the buttons while it is up
  filmroll_overlays_active()  ML's LiveView overlays step aside while it is up

Both just call into the module once it is loaded; if it is not loaded they
answer as if there were no film OS, so the camera behaves as before.

Left out on purpose in this first build: the third M-Film hook (the one that
sends the Magic Lantern menu button to the film OS). Without it, Magic Lantern's
own menu stays reachable with the Trash button, so you can always get back to it.

Safe to run twice: each edit is skipped if it is already there. If a place to
edit can't be found, it stops with a message and changes nothing more.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
if not (root / "src" / "gui-common.c").exists():
    sys.exit(f"{root}: this doesn't look like the magic-lantern-2000d folder (no src/gui-common.c)")


def read(rel):
    # newline='' keeps the file's own line endings (some files here are CRLF)
    with open(root / rel, newline="") as f:
        return f.read()


def write(rel, text):
    with open(root / rel, "w", newline="") as f:
        f.write(text)


def edit(rel, anchor, addition, marker, where="after"):
    """Put `addition` right after (or before) the first `anchor` in the file."""
    text = read(rel)
    nl = "\r\n" if "\r\n" in text else "\n"
    anchor = anchor.replace("\n", nl)
    addition = addition.replace("\n", nl)
    if marker in text:
        print(f"  {rel}: already done")
        return
    if text.count(anchor) < 1:
        sys.exit(f"  {rel}: can't find the place to edit:\n{anchor!r}\n(the source differs from what this script expects)")
    new = anchor + addition if where == "after" else addition + anchor
    write(rel, text.replace(anchor, new, 1))
    print(f"  {rel}: edited")


# 1. key hook, ahead of the modules' own key handling
edit("src/gui-common.c",
     "    if (handle_module_keys(event) == 0) return 0;\n",
     "    if (handle_filmroll_keys(event) == 0) return 0;\n",
     "handle_filmroll_keys", where="before")
edit("src/gui-common.c",
     "#include <zebra.h>\n",
     "#include \"filmroll.h\"\n",
     "filmroll.h")

# 2. ML's LiveView overlays step aside while the film OS is up
edit("src/zebra.c",
     "int get_global_draw() // menu setting, or off if \n{\n",
     "    if (filmroll_overlays_active()) return 0;\n",
     "filmroll_overlays_active")
edit("src/zebra.c",
     "#include \"zebra.h\"\n",
     "#include \"filmroll.h\"\n",
     "filmroll.h")

# 3. build the hook file into autoexec.bin
edit("src/Makefile.src",
     "\tgui-common.o \\\n",
     "\tfilmhook.o \\\n",
     "filmhook.o")

# 4. the two new files
filmroll_h = """/* The calls Magic Lantern's core makes into M-Film's film OS module. */
#ifndef _filmroll_h_
#define _filmroll_h_

struct event;

/* 0: the film OS used this button, the rest of ML must not see it; 1: not used */
int handle_filmroll_keys(struct event *event);

/* nonzero while the film OS is up: ML's overlays stay off */
int filmroll_overlays_active();

#endif
"""

filmhook_c = """/* The film OS as a module: all that stays in autoexec.bin are these hooks.
 * The film OS itself is ML/modules/filmos.mo, loaded after boot. Each call goes
 * to the module once it is loaded; without it (missing, failed to load) they
 * answer as if there were no film OS, so the camera is just Magic Lantern. */

#include <dryos.h>
#include <module.h>
#include "filmroll.h"

/* defined in the module (filmroll.c); ret_0 until it is loaded */
static int (*filmos_key_used)(struct event *event) = MODULE_FUNCTION(filmos_key_used);
static int (*filmos_overlays)(void)                = MODULE_FUNCTION(filmos_overlays);

int handle_filmroll_keys(struct event *event)
{
    return filmos_key_used(event) ? 0 : 1;
}

int filmroll_overlays_active()
{
    return filmos_overlays();
}
"""

for rel, body in (("src/filmroll.h", filmroll_h), ("src/filmhook.c", filmhook_c)):
    p = root / rel
    if p.exists() and p.read_text() == body:
        print(f"  {rel}: already done")
    else:
        p.write_text(body)
        print(f"  {rel}: written")

print("done")
