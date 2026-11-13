/* Minimal film OS hooks for the 2000D / T7 port.
 * - Forwards keys and overlay control to filmos.mo once it is loaded.
 * - Opens the film UI automatically a few seconds after boot if the module
 *   loaded successfully.
 * - Leaves a safe escape: press and hold the Q button for ~1.5 s to force
 *   the real Magic Lantern menu (so you can never get locked out).
 * - Prints a clear message + writes ML/FILMROLL.LOG if the module is missing
 *   or failed to load.
 */

#include <dryos.h>
#include <module.h>
#include <fio-ml.h>
#include <notify_box.h>
#include <tasks.h>
#include <bmp.h>
#include <property.h>
#include <gui.h>

/* Declared by the module (filmos.mo). Until the module is loaded these
 * resolve to the stub that returns 0 / does nothing. */
static int (*filmos_key_used)(struct event *event) = MODULE_FUNCTION(filmos_key_used);
static int (*filmos_menu_open)(void)               = MODULE_FUNCTION(filmos_menu_open);
static int (*filmos_overlays)(void)                = MODULE_FUNCTION(filmos_overlays);

/* Force the real ML menu even when the film OS is active. */
static volatile int force_ml_menu = 0;

int handle_filmroll_keys(struct event *event)
{
    /* Escape hatch: hold Q (~1.5 s) forces the real Magic Lantern menu.
     * Q is BGMT_Q = 0x1C on the 2000D/T7. */
    static int q_down_ms = 0;
    if (event->param == 0x1C) {          /* BGMT_Q press */
        q_down_ms = get_ms_clock() ? get_ms_clock() : 1;
        return 1;                        /* let it through for now */
    }
    /* any other key while Q was held long enough */
    if (q_down_ms) {
        int now = get_ms_clock();
        if (now && now - q_down_ms > 1400) {
            force_ml_menu = 1;
            q_down_ms = 0;
            /* fall through so the real menu can open */
            return 1;
        }
        q_down_ms = 0;
    }

    if (force_ml_menu)
        return 1;                        /* do not give the key to film OS */

    /* Normal path: let the module decide. Returns 0 = consumed by film OS. */
    return filmos_key_used(event) ? 0 : 1;
}

int filmroll_menu_requested(void)
{
    if (force_ml_menu) {
        force_ml_menu = 0;
        return 0;                        /* tell caller "module not interested" → real ML menu */
    }
    return filmos_menu_open();           /* 1 = film OS took it, 0 = not loaded */
}

int filmroll_overlays_active(void)
{
    return filmos_overlays();
}

/* ---------- diagnostics + auto-open ---------- */

extern int module_autoload_disabled;

static int filmos_is_loaded(void)
{
    /* Walk the loaded modules looking for one named "filmos". */
    for (int i = 0; i < MODULE_COUNT_MAX; i++) {
        const char *name = module_get_name(i);
        if (name && strcmp(name, "filmos") == 0)
            return 1;
    }
    return 0;
}

static void filmhook_note(const char *why)
{
    NotifyBox(12000, "M-Film: %s", why);
    FILE *f = FIO_CreateFileOrAppend("ML/FILMROLL.LOG");
    if (f) {
        char line[180];
        snprintf(line, sizeof(line), "filmhook: %s\n", why);
        FIO_WriteFile(f, line, strlen(line));
        FIO_CloseFile(f);
    }
}

static void filmhook_task(void *unused)
{
    (void)unused;

    /* Wait for ML's module loader (a few seconds after boot). */
    for (int i = 0; i < 40 && filmos_menu_open == (void *)ret_0; i++)
        msleep(400);

    if (filmos_menu_open != (void *)ret_0) {
        /* Module is alive. Give it a moment, then ask it to open the UI. */
        msleep(800);
        filmroll_menu_requested();
        return;
    }

    /* Module never appeared – tell the user why. */
    uint32_t size = 0;
    if (module_autoload_disabled)
        filmhook_note("'Disable all modules' is ON (MENU > Debug)");
    else if (FIO_GetFileSize("ML/modules/filmos.mo", &size) != 0)
        filmhook_note("ML/modules/filmos.mo missing – copy M-Film files");
    else if (!filmos_is_loaded())
        filmhook_note("modules skipped (unclean power-off?). Power cycle.");
    else
        filmhook_note("filmos.mo present but did not load – check Modules");
}

TASK_CREATE("filmhook", filmhook_task, 0, 0x1f, 0x1000);
