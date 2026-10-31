import sys, re, shutil, subprocess
from datetime import datetime, timezone
from align_string_proportional import word_wrap
from rbf_read import extent_func, rbf_init_font

rbf_init_font("../../data/fonts/argnor23.rbf")

def run(cmd):
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out_s = out.decode('utf-8', errors='replace')
        err_s = err.decode('utf-8', errors='replace')
        if p.returncode:
            return ""
        return out_s
    except Exception:
        return ""

def c_repr(name):
    if "\n" in name:
        s = "\n"
        for l in name.split("\n"):
            s += "    %s\n" % ('"%s\\n"' % l.replace('\\', '\\\\').replace('"', r'\"'))
        return s
    else:
        return '"%s"' % name.replace('\\', '\\\\').replace('"', r'\"')

strings = []
def add_string(name, value):
    a = chr(ord('a') + len(strings))
    print("static char __module_string_%s_name [] MODULE_STRINGS_SECTION = %s;" % (a, c_repr(name)))
    print("static char __module_string_%s_value[] MODULE_STRINGS_SECTION = %s;" % (a, c_repr(value)))
    strings.append((name, value))

def declare_string_section():
    print("")
    print("#define MODULE_STRINGS() \\")
    print("  MODULE_STRINGS_START() \\")
    for i, _ in enumerate(strings):
        a = chr(ord('a') + i)
        print("    MODULE_STRING(__module_string_%s_name, __module_string_%s_value) \\" % (a, a))
    print("  MODULE_STRINGS_END()")

with open("README.rst", encoding="utf-8", errors="replace") as f:
    inp = f.read().replace("\r\n", "\n")

lines = inp.strip("\n").split("\n")
title = lines[0].strip()
add_string("Name", title)

tags = {}
body_lines = []
i = 2
while i < len(lines):
    l = lines[i]
    m = re.match(r"^:([^:]+):(.+)$", l.strip())
    if m:
        name = m.group(1).strip()
        value = m.group(2).strip()
        if not (value.startswith("<") and value.endswith(">")):
            add_string(name, value)
            tags[name] = value
        i += 1
        continue
    if l.startswith(".."):
        i += 1
        continue
    # Convert RST underline headings into "# Heading"
    if i + 1 < len(lines) and len(lines[i + 1].strip()) >= 3 and len(set(lines[i + 1].strip())) == 1 and lines[i + 1].strip()[0] in "=-~^" and l.strip():
        body_lines.append("# " + l.strip())
        i += 2
        continue
    body_lines.append(l)
    i += 1

# Wrap paragraphs to 700px proportional width, matching html2text.py -b 700
wrapped_lines = []
for raw_l in body_lines:
    clean_l = re.sub(r"``([^`]+)``", r"\1", raw_l)
    clean_l = re.sub(r"`([^`<]+)\s*<[^>]+>`__?", r"\1", clean_l)
    if clean_l.startswith("# "):
        wrapped_lines.append(clean_l)
    elif not clean_l.strip():
        if wrapped_lines and wrapped_lines[-1] != "":
            wrapped_lines.append("")
    else:
        for wl in word_wrap(clean_l, 680, extent_func):
            wrapped_lines.append(wl)

desc = ""
last_str = "Description"
help_page_num = 0
lines_per_page = 0
for p in wrapped_lines:
    if p.startswith("# ") or lines_per_page >= 16:
        help_page_num += 1
        add_string(last_str, desc)
        desc = ""
        last_str = "Help page %d" % help_page_num
        lines_per_page = 0
        if p.startswith("# "):
            p = p[2:].strip()
    desc += "%s\n" % p
    lines_per_page += 1

add_string(last_str, desc)

build_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
add_string("Build date", build_date)
add_string("Build user", "ml-2000d-local")

declare_string_section()
