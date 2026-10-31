import os, sys

def read_dep(file):
    with open(file, encoding='utf-8', errors='replace') as f:
        return [d.strip() for d in f if d.strip()]

def read_sym(file):
    with open(file, encoding='utf-8', errors='replace') as f:
        return [s.strip().split(" ")[1] for s in f if " " in s.strip()]

def try_solve_deps(file, deps):
    try:
        syms = read_sym(file)
    except Exception:
        return []
    return [s for s in syms if s in deps]

module = sys.argv[1]
modules = sorted([m for m in os.listdir(".") if os.path.isdir(m)])
platformdir = "../platform/"
cameras = sorted([
    c for c in os.listdir(platformdir)
    if "." in c and c[0] == c[0].upper() and "MASTER" not in c and os.path.isdir(os.path.join(platformdir, c))
])

deps = read_dep(os.path.join(module, module + ".dep"))

module_deps = []
for m in modules:
    solved = try_solve_deps(os.path.join(m, m + ".sym"), deps)
    if solved:
        module_deps.append((m, solved))
        deps = list(set(deps) - set(solved))

if module_deps:
    print("Depends on modules: ")
    for m, d in module_deps:
        print("    %s (%s)" % (m, ", ".join(d)))

working_cameras = []
not_working_cameras = []
not_checked_cameras = []

for c in cameras:
    cam_name = c.split(".")[0]
    if cam_name in [c2.split(".")[0] for c2 in cameras if c2 != c]:
        cam_name = c
    cam_sym = os.path.join(platformdir, c, "magiclantern.sym")
    solved = try_solve_deps(cam_sym, deps)
    if solved or not deps:
        unsolved_deps = list(set(deps) - set(solved))
        if unsolved_deps:
            not_working_cameras.append((cam_name, unsolved_deps))
        else:
            working_cameras.append(cam_name)
    elif os.path.isfile(cam_sym):
        with open(cam_sym, encoding='utf-8', errors='replace') as f:
            txt = f.read()
        if len(txt) == 0:
            not_checked_cameras.append(cam_name + " (empty sym)")
        else:
            not_checked_cameras.append(cam_name + " (error)")
    else:
        not_checked_cameras.append(cam_name)

if working_cameras:
    print("Will load on:\n   ", ", ".join(working_cameras))
if not_working_cameras:
    print("Will NOT load on: ")
    for c, d in not_working_cameras:
        if len(d) > 4:
            d = d[:3] + ["and %d others" % (len(d) - 3)]
        print("    %s (%s)" % (c, ", ".join(d)))
if not_checked_cameras:
    print("Not checked (compile ML for these cameras first):\n   ", ", ".join(not_checked_cameras))
if not working_cameras:
    try:
        os.remove(os.path.join(module, module + ".dep"))
    except OSError:
        pass
    sys.exit(1)
