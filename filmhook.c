/* Safe film OS hooks for the 2000D / T7 port.
 *
 * - Forwards keys and overlay control to filmos.mo once it is loaded.
 * - Does NOT touch the Magic Lantern menu system at all.
 *   Trash always opens the normal ML menu (Modules tab visible).
 * - Writes a clear message + ML/FILMROLL.LOG if the module is missing
 *   or fails to load.
 */

#include <dryos.h>
#include <module.h>
#include <fio-ml.h>
#include <notify_box.h>
#include <tasks.h>
#include <string.h>

/* Declared by the module (filmos.mo). Until the module is loaded these
 * resolve to the stub that returns 0 / does nothing. */
static int (*filmos_key_used)(struct event *event) = MODULE_FUNCTION(filmos_key_used);
static int (*filmos_overlays)(void)                = MODULE_FUNCTION(filmos_overlays);

int handle_filmroll_keys(struct event *event)
{
    /* 0 = film OS consumed the key, 1 = pass it on */
    return filmos_key_used(event) ? 0 : 1;
}

int filmroll_overlays_active(void)
{
    return filmos_overlays();
}

/* ---------- diagnostics only ---------- */

extern int module_autoload_disabled;

static int filmos_is_loaded(void)
{
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

    /* Wait for ML's module loader */
    for (int i = 0; i < 40 && filmos_key_used == (void *)ret_0; i++)
        msleep(400);

    if (filmos_key_used != (void *)ret_0)
        return;   /* module is alive – nothing else to do */

    /* Module never appeared */
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
