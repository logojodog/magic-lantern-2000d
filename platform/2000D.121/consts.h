/*
 *  Canon EOS 2000D 1.2.1 consts.h (verified against ROM1.BIN 4db8f7780983b1890b50cd305ba74b8b)
 */

#define CANON_SHUTTER_RATING 100000

#define CARD_LED_ADDRESS 0xc022d1e0 // DIGIC 4+ LED GPIO (same family as 1300D)
#define LEDON 0x93d800
#define LEDOFF 0x83dc00

#define HIJACK_CACHE_HACK

#define HIJACK_CACHE_HACK_BSS_END_ADDR   0xfe0c1b74
#define HIJACK_CACHE_HACK_BSS_END_INSTR  0xE3A01732 // MOV R1, #0xc80000 (was 0xe3a0160d MOV R1, #0xd00000)
#define HIJACK_CACHE_HACK_INITTASK_ADDR  0xfe0c3b34

#define HIJACK_INSTR_BL_CSTART  0xfe0c0638
#define HIJACK_INSTR_BSS_END    0xfe0c3b24
#define HIJACK_FIXBR_BZERO32    0xfe0c3a6c
#define HIJACK_FIXBR_CREATE_ITASK 0xfe0c3b0c
#define HIJACK_INSTR_MY_ITASK   0xfe0c3b34

#define DRYOS_ASSERT_HANDLER 0x35888 // verified in TH_assert (RAM 0x3cbc)
#define MVR_992_STRUCT (*(void**)(0x315dc+0x4)) // verified in MVR_Initialize (0xfe0fe8e4)

#define div_maybe(a,b) ((a)/(b))
#define MVR_BUFFER_USAGE_FRAME ABS(div_maybe(-100*MEM(356 + MVR_992_STRUCT) - 100*MEM(364 + MVR_992_STRUCT) - 100*MEM(952 + MVR_992_STRUCT) - 100*MEM(960 + MVR_992_STRUCT) + 100*MEM(360 + MVR_992_STRUCT) + 100*MEM(368 + MVR_992_STRUCT), -MEM(356 + MVR_992_STRUCT) - MEM(364 + MVR_992_STRUCT) + MEM(360 + MVR_992_STRUCT) + MEM(368 + MVR_992_STRUCT)))
#define MVR_BUFFER_USAGE_SOUND div_maybe(-100*MEM(544 + MVR_992_STRUCT) + 100*MEM(532 + MVR_992_STRUCT), 0xa)
#define MVR_BUFFER_USAGE MAX(MVR_BUFFER_USAGE_FRAME, MVR_BUFFER_USAGE_SOUND)

#define MVR_FRAME_NUMBER (*(int*)(332 + MVR_992_STRUCT))
#define MVR_BYTES_WRITTEN MEM((296 + MVR_992_STRUCT))

#define MOV_RES_AND_FPS_COMBINATIONS 9
#define MOV_OPT_NUM_PARAMS 2
#define MOV_GOP_OPT_NUM_PARAMS 5
#define MOV_OPT_STEP 5
#define MOV_GOP_OPT_STEP 5

#define AUDIO_MONITORING_HEADPHONES_CONNECTED 0

// 720x480, changes when external monitor is connected
#define YUV422_LV_BUFFER_1 0x40d07800
#define YUV422_LV_BUFFER_2 0x4c233800
#define YUV422_LV_BUFFER_3 0x4f11d800

#define REG_EDMAC_WRITE_LV_ADDR 0xc0f04308 // SDRAM address of LV buffer (aka VRAM)
#define REG_EDMAC_WRITE_HD_ADDR 0xc0f04208 // SDRAM address of HD buffer (aka YUV)

#define YUV422_LV_BUFFER_DISPLAY_ADDR (*(uint32_t*)0x318C8) // 0x31818+0xB0 (verified @ SetBitmapVramAddress 0xfe113c28)
#define YUV422_HD_BUFFER_DMA_ADDR (shamem_read(REG_EDMAC_WRITE_HD_ADDR))

// changes during record
#define YUV422_HD_BUFFER_1 0x44000080
#define YUV422_HD_BUFFER_2 0x46000080
#define YUV422_HD_BUFFER_3 0x48000080
#define YUV422_HD_BUFFER_4 0x4e000080
#define YUV422_HD_BUFFER_5 0x50000080

#define FOCUS_CONFIRMATION (*(int*)(0x36e24 + 0x4))      // verified in focusinfo (0xfe165c58)
#define HALFSHUTTER_PRESSED (*(int*)(0x359A8 + 0x1C))    // verified in "[MC] permit LV instant" (0xfe12c9d0)
#define DISPLAY_SENSOR_POWERED (*(int*)(0x359A8 + 0x18)) // verified in "ForceDisableDisplay (%d)" (0xfe12d584)

// for gui_main_task (verified @ 0xfe0cc4f0 -> 0xFE872864, 7 function pointers)
#define GMT_NFUNCS 7
#define GMT_FUNCTABLE 0xFE872864

#define LV_BOTTOM_BAR_DISPLAYED (((*(int8_t*)0x38310) == 0xF) || ((*(int8_t*)0x3FD9C) != 0x17))
#define LV_BOTTOM_BAR_STATE (*(uint8_t*)(0x3AA08 + 0x3C)) // verified in JudgeBottomInfoDispTimerState -> 0xfe2e0d28
#define ISO_ADJUSTMENT_ACTIVE ((*(int*)0x38310) == 0xF)
#define SHOOTING_MODE (*(int*)(0x66180 + 0x58)) // verified @ 0xfe2e8a54
#define UNAVI_FEEDBACK_TIMER_ACTIVE (MEM(0x3FD9C) != 0x17) // verified in CancelUnaviFeedBackTimer (0xfe490dac: 0x3fd88+0x14)

#define AE_STATE (*(int8_t*)(0x3AA08 + 0x1C))
#define AE_VALUE (*(int8_t*)(0x3AA08 + 0x1D))

#define CURRENT_GUI_MODE (*(int*)(0x3647c + 0x48)) // verified in SetGUIRequestMode (0xfe14df50: 0x3647c + 0x48)

#define COLOR_FG_NONLV 80
#define GUIMODE_WB 5
#define GUIMODE_FOCUS_MODE 9
#define GUIMODE_DRIVE_MODE 8
#define GUIMODE_PICTURE_STYLE 4

#define GUIMODE_PLAY 1
#define GUIMODE_MENU 2
#define GUIMODE_Q_UNAVI 0x1F
#define GUIMODE_FLASH_AE 0x22
#define GUIMODE_PICQ 6
#define GUIMODE_MOVIE_ENSURE_A_LENS_IS_ATTACHED (CURRENT_GUI_MODE == 0x1e)
#define GUIMODE_MOVIE_PRESS_LV_TO_RESUME (CURRENT_GUI_MODE == 0x1f)

#define PLAY_MODE (gui_state == GUISTATE_PLAYMENU && CURRENT_GUI_MODE == GUIMODE_PLAY)
#define MENU_MODE (gui_state == GUISTATE_PLAYMENU && CURRENT_GUI_MODE == GUIMODE_MENU)

// position for ML ISO disp outside LV
#define MENU_DISP_ISO_POS_X 527
#define MENU_DISP_ISO_POS_Y 45

// position for ML MAX ISO
#define MAX_ISO_POS_X 590
#define MAX_ISO_POS_Y 28

// for ML hdr display
#define HDR_STATUS_POS_X 562
#define HDR_STATUS_POS_Y 100

// for HTP mode on display
#define HTP_STATUS_POS_X 500
#define HTP_STATUS_POS_Y 233

// for Mirror Lock Up enabled on display
#define MLU_STATUS_POS_X 316
#define MLU_STATUS_POS_Y 310

#define WBS_GM_POS_X 365
#define WBS_GM_POS_Y 230

#define WBS_POS_X 365
#define WBS_POS_Y 260

// Audio remote shot position info photo mode
#define AUDIO_REM_SHOT_POS_X 200
#define AUDIO_REM_SHOT_POS_Y 386

// position for displaying clock outside LV
#define DISPLAY_CLOCK_POS_X 440
#define DISPLAY_CLOCK_POS_Y 400

#define DISPLAY_DATE_POS_X 425
#define DISPLAY_DATE_POS_Y 430

#define DISPLAY_BATTERY_POS_X 350
#define DISPLAY_BATTERY_POS_Y 400

// position for displaying K icon in photo info display
#define WB_K_ICON_POS_X 307
#define WB_K_ICON_POS_Y 226

// position for displaying K values in photo info display
#define WB_KELVIN_POS_X 307
#define WB_KELVIN_POS_Y 260

// position for displaying card size remain outside LV
#define DISPLAY_GB_POS_X 305
#define DISPLAY_GB_POS_Y 410

// for displaying TRAP FOCUS msg outside LV
#define DISPLAY_TRAP_FOCUS_POS_X 65
#define DISPLAY_TRAP_FOCUS_POS_Y 360
#define DISPLAY_TRAP_FOCUS_MSG       "TRAP FOCUS"
#define DISPLAY_TRAP_FOCUS_MSG_BLANK "          "

#define GUIMODE_ML_MENU (lv ? 68 : 2)

#define NUM_PICSTYLES 10

#define FLASH_MAX_EV 3
#define FLASH_MIN_EV -5
#define FASTEST_SHUTTER_SPEED_RAW 152
#define MAX_AE_EV 5
#define DIALOG_MnCardFormatBegin   (0x4640c+4) // verified @ StartMnCardFormatBeginApp (0xfe588424)
#define DIALOG_MnCardFormatExecute (0x49d74+4) // verified @ StartMnCardFormatExcuteApp (0xfe675c44)
#define FORMAT_BTN_NAME "[Q]"
#define FORMAT_BTN BGMT_Q
#define FORMAT_STR_LOC 11

#define BULB_MIN_EXPOSURE 1000

// CanonGothic BFNT font @ 0xFF23EAA8 + 0x24 header (verified in ROM1.BIN)
#define BFNT_CHAR_CODES    0xff23eacc
#define BFNT_BITMAP_OFFSET 0xff241a08
#define BFNT_BITMAP_DATA   0xff244944

// from CFn
#define AF_BTN_HALFSHUTTER 0
#define AF_BTN_STAR 1

#define IMGPLAY_ZOOM_LEVEL_ADDR (0x3b050+12) // verified @ GuiImageZoomDown (0xfe30e8c4)
#define IMGPLAY_ZOOM_LEVEL_MAX 14
#define IMGPLAY_ZOOM_POS_X MEM(0x6f038)     // verified (-0x980, 3 refs)
#define IMGPLAY_ZOOM_POS_Y MEM(0x6f038+0x4)
#define IMGPLAY_ZOOM_POS_X_CENTER 0x144
#define IMGPLAY_ZOOM_POS_Y_CENTER 0xd8
#define IMGPLAY_ZOOM_POS_DELTA_X (0x144 - 0x93)
#define IMGPLAY_ZOOM_POS_DELTA_Y (0xd8 - 0x7d)

#define BULB_EXPOSURE_CORRECTION 100

#define WINSYS_BMP_DIRTY_BIT_NEG MEM(0x3da64+0x2C) // verified @ Winsys_TransferDirtyBit (0xfe40e7f0)

// manual exposure overrides (verified in EP_SetControlBv @ 0xfe364620 -> 0x3b770)
#define LVAE_STRUCT 0x3B770
#define CONTROL_BV      (*(uint16_t*)(LVAE_STRUCT+0x1c))
#define CONTROL_BV_TV   (*(uint16_t*)(LVAE_STRUCT+0x1e))
#define CONTROL_BV_AV   (*(uint16_t*)(LVAE_STRUCT+0x20))
#define CONTROL_BV_ISO  (*(uint16_t*)(LVAE_STRUCT+0x22))
#define CONTROL_BV_ZERO (*(uint16_t*)(LVAE_STRUCT+0x24))
#define LVAE_ISO_SPEED  (*(uint8_t* )(LVAE_STRUCT))
#define LVAE_ISO_MIN    (*(uint8_t* )(LVAE_STRUCT+0x2a))
#define LVAE_ISO_HIS    (*(uint8_t* )(LVAE_STRUCT+0x2c))
#define LVAE_DISP_GAIN  (*(uint16_t*)(LVAE_STRUCT+0x26))
#define LVAE_MOV_M_CTRL (*(uint8_t* )(LVAE_STRUCT+0x78))

#define DISPLAY_ORIENTATION MEM(0x31818+0x80) // verified in UpdateReverseTFT @ 0xfe116a0c

#define MIN_MSLEEP 20

#define INFO_BTN_NAME "DISP"
#define Q_BTN_NAME (RECORDING ? "INFO" : "[Q]")
#define ARROW_MODE_TOGGLE_KEY ""

#define DISPLAY_STATEOBJ (*(struct state_object **)0x318BC) // 0x31818+0xA4 (verified @ 0xfe116b80)
#define DISPLAY_IS_ON (DISPLAY_STATEOBJ->current_state != 0)

#define VIDEO_PARAMETERS_SRC_3 0x69c54 // verified (-0x980)
#define FRAME_SHUTTER_TIMER (*(uint16_t*)(VIDEO_PARAMETERS_SRC_3+0xC))
#define FRAME_ISO (*(uint8_t*)(VIDEO_PARAMETERS_SRC_3+0x8))
#define FRAME_APERTURE (*(uint8_t*)(VIDEO_PARAMETERS_SRC_3+0x9))
#define FRAME_SHUTTER (*(uint8_t*)(VIDEO_PARAMETERS_SRC_3+0xa))
#define FRAME_BV ((int)FRAME_SHUTTER + (int)FRAME_APERTURE - (int)FRAME_ISO)

#define FRAME_SHUTTER_BLANKING_ZOOM   (*(uint16_t*)0x40481B20)
#define FRAME_SHUTTER_BLANKING_NOZOOM (*(uint16_t*)0x40481B24)
#define FRAME_SHUTTER_BLANKING_READ   (lv_dispsize > 1 ? FRAME_SHUTTER_BLANKING_NOZOOM : FRAME_SHUTTER_BLANKING_ZOOM)
#define FRAME_SHUTTER_BLANKING_WRITE  (lv_dispsize > 1 ? &FRAME_SHUTTER_BLANKING_ZOOM : &FRAME_SHUTTER_BLANKING_NOZOOM)

// see "Malloc Information" (verified @ 0xfe12b564 & _malloc 0xfe2c6be0 -> 0x65de0)
#define MALLOC_STRUCT 0x65de0
#define MALLOC_FREE_MEMORY (MEM(MALLOC_STRUCT + 8) - MEM(MALLOC_STRUCT + 0x1C))
#define SRM_BUFFER_SIZE 0x1f68000

#define BRAMP_CALIBRATION_DELAY 1000
#define ASIF_MAX_VOL 5

// verified in JudgeBottomInfoDispTimerState (0xfe48adec: 0x3fd88 + 0x5c)
#define JUDGE_BOTTOM_INFO_DISP_TIMER_STATE 0x3fde4

#define EFIC_CELSIUS ((int)efic_temp * 55 / 100 - 68)
