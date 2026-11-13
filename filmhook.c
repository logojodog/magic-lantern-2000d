/* Ultra-passive film OS hooks for the 2000D / T7.
 *
 * Goal: do not contribute to crashes on the second power-on.
 *
 * - Forwards keys and overlay control to filmos.mo if it is loaded.
 * - Does NOT touch the Magic Lantern menu (Trash = normal ML menu).
 * - Does NOT force the film UI open.
 * - Diagnostic only writes to ML/FILMROLL.LOG (no on-screen NotifyBox).
 */

#include <dryos.h>
#include <module.h>
#include <fio-ml.h>
#include <tasks.h>
#include <string.h>

/* Declared by the module. Until loaded these are the ret_0 stub. */
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

/* ---------- diagnostic only (log file, no screen) ---------- */

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

static void filmhook_log(const char *why)
{
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

    /* Wait a few seconds for the module loader */
    for (int i = 0; i < 30 && filmos_key_used == (void *)ret_0; i++)
        msleep(500);

    if (filmos_key_used != (void *)ret_0)
        return;   /* module is alive – stay completely silent */

    /* Module never appeared – log only, never touch the screen */
    uint32_t size = 0;
    if (module_autoload_disabled)
        filmhook_log("'Disable all modules' is ON");
    else if (FIO_GetFileSize("ML/modules/filmos.mo", &size) != 0)
        filmhook_log("ML/modules/filmos.mo missing");
    else if (!filmos_is_loaded())
        filmhook_log("modules skipped or failed to load");
    else
        filmhook_log("filmos.mo present but not answering");
}

TASK_CREATE("filmhook", filmhook_task, 0, 0x1f, 0x1000);
