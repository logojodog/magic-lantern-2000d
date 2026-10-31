/** \file
 * Entry points into the firmware image for Canon EOS 2000D / Rebel T7 1.2.1 (K432).
 *
 * All ROM & RAM addresses below have been binary-verified against the 1.2.1 ROM1 dump
 * (MD5: 4db8f7780983b1890b50cd305ba74b8b, ROMBASEADDR: 0xFE0C0000).
 */
/*
 * Copyright (C) 2021 Magic Lantern Team
 * GPLv2+
 */

#include <stub.h>

/** Startup **/
NSTUB( ROMBASEADDR, firmware_entry )                        // 0xFE0C0000
NSTUB(0xfe0c3a38,  cstart)                                  // verified @ 0xFE0C0638 B 0xFE0C3A38
NSTUB(   0x29898,  bzero32)                                 // RAM (ROM copy 0xFEA1D47C -> 0x1900), called @ 0xFE0C3A6C
NSTUB(    0x5254,  create_init_task)                        // RAM, called @ 0xFE0C3B0C
NSTUB(0xfe12a098,  init_task)                               // ptr @ 0xFE0C3B34, refs "dmSetup"
NSTUB(   0x66068,  additional_version)                      // 1.1.0 0x669e8 - 0x980 (2 ROM refs verified)

/** File I/O (+0x99c vs 1.1.0, 13/13 prologues verified) **/
NSTUB(0xfe2a3f48,  FIO_CloseFile)
NSTUB(0xfe2a4f1c,  FIO_FindClose)
NSTUB(0xfe2a4e3c,  FIO_FindNextEx)
NSTUB(0xfe2a3cf8, _FIO_ReadFile)
NSTUB(0xfe2a3da8,  FIO_SeekSkipFile)
NSTUB(0xfe2a3e98, _FIO_WriteFile)
NSTUB(0xfe2a4788, _FIO_CreateDirectory)
NSTUB(0xfe2a3ba4, _FIO_CreateFile)
NSTUB(0xfe2a4d48, _FIO_FindFirstEx)
NSTUB(0xfe2a40c4, _FIO_GetFileSize)
NSTUB(0xfe2a3ae8, _FIO_OpenFile)
NSTUB(0xfe2a3c50, _FIO_RemoveFile)
NSTUB(0xfe2a45c0, _FIO_RenameFile)

/** GUI **/
NSTUB(   0x3136c,  gui_main_struct)                         // verified in gui_main_task (0xFE0CC504)
NSTUB(   0x3d914,  gui_task_list)                           // verified @ gui_task_create 0xFE3EF348 (+0x0 lock, +0x8 current)
NSTUB(0xfe0cca74,  GUI_ChangeMode)                          // verified (+0x0)
NSTUB(0xfe0cc8b8,  GUI_Control)                             // verified "GUI_Control:%d 0x%x"
NSTUB(0xfe14df34,  SetGUIRequestMode)                       // verified "SetGUIRequestMode(%d)" (+0x980)
NSTUB(0xfe0ccf28,  gui_init_end)                            // verified "EndGuiInit"
NSTUB(0xfe0cc4e8,  gui_main_task)                           // verified "GuiMainTask"
NSTUB(0xfe1507ac,  gui_massive_event_loop)                  // verified "GUI_Control_Post(%d)" (+0x980)
NSTUB(0xfe2eb9e0,  GUI_SetLvMode)                           // verified "GUI_SetLvMode (%d)" (+0xd98)
NSTUB(0xfe2ebc14,  Gui_SetSoundRecord)                      // verified (+0xd98)

/** ASIF **/
NSTUB(0xfe11db80,  PowerAudioOutput)                        // +0x980
NSTUB(0xfe11c2ec,  SetAudioVolumeOut)                       // +0x980
NSTUB(0xfe106ac8,  SetNextASIFADCBuffer)                    // verified prologue @ 0xFE106AC8 (+0x4 fix)
NSTUB(0xfe106cb0,  SetNextASIFDACBuffer)                    // +0x0
NSTUB(0xfe11d044,  SetSamplingRate)                         // +0x980
NSTUB(0xfe105fac,  StartASIFDMAADC)                         // +0x0
NSTUB(0xfe106380,  StartASIFDMADAC)                         // +0x0
NSTUB(0xfe106600,  StopASIFDMADAC)                          // +0x0
NSTUB(0xfe11d6b8,  PowerMicAmp)                             // +0x980
NSTUB(0xfe106728,  SetASIFMode)                             // +0x0
NSTUB(0xfe108aa0,  SoundDevActiveIn)                        // +0x0
NSTUB(0xfe108cf8,  SoundDevShutDownIn)                      // +0x0
NSTUB(0xfe106258,  StopASIFDMAADC)                          // +0x0

/** Audio **/
NSTUB(   0x31604,  sounddev)                                // verified in sounddev_task @ 0xFE1086B0
NSTUB(0xfe2b3a5c, _audio_ic_read)                           // +0xd00
NSTUB(0xfe2b36f4, _audio_ic_write)                          // +0xd00
NSTUB(0xfe8e380c,  audio_thresholds)                        // verified after "AudioLevel" ptr @ 0xFE8E37FC
NSTUB(0xfe108aa0,  sounddev_active_in)                      // +0x0
NSTUB(0xfe108690,  sounddev_task)                           // verified "[SND] _SoundDeviceTask"

/** Bitmap **/
NSTUB(   0x536a0,  LCD_Palette)                             // verified in InitializeBitmapDisplayDevice @ 0xFE117D94
NSTUB(   0x54ea0,  bmp_vram_info)                           // verified in SetBitmapVramAddress @ 0xFE113BD8

/** CFN **/
NSTUB(0xfe7152b4,  GetCFnData)                              // verified "Illegal Data GetCFnData (%d)" (+0x23e0)
NSTUB(0xfe7154e0,  SetCFnData)                              // verified "Illegal Data SetCFnData (%d)" (+0x23e0)

/** Camera interface **/
NSTUB(0xC0220000,  camera_engine)

/** MPU communication **/
NSTUB(0xfe298f00, _mpu_send)                                // verified "dwSize < TXBD_DATA_SIZE"
NSTUB(0xfe10faa0, _mpu_recv)                                // verified CBR in InitializeIntercom -> 0xFE10FBE8

/** DMA **/
NSTUB(0xfe124eb0,  dma_memcpy)                              // +0x980

/** Debug messages **/
NSTUB(   0x31bf8,  dm_names)                                // verified in DryosDebugMsg @ 0xFE11FDB8
NSTUB(0xfe11fd48,  DryosDebugMsg)                           // verified (24,687 BL calls, +0x980)
NSTUB(0xfe1200b0,  dm_set_store_level)                      // +0x980
NSTUB(0xfe120048,  dm_set_print_level)                      // +0x980

/** Dialog API **/
NSTUB(0xfe3f10cc,  dialog_redraw)                           // verified (+0xd98, called by StartPlayMovieGuideApp)
NSTUB(0xfe2f8e14,  dialog_set_property_str)                 // +0xd98

/** Dialog handlers **/
NSTUB(0xfe5ae4d4,  ErrCardForLVApp_handler)                 // verified in StartLiveViewErrorApp @ 0xFE5AE5C8
NSTUB(0xfe4561dc,  ErrForCamera_handler)                    // verified "DlgErrForCamera.c" (+0x11a4)
NSTUB(0xfe48904c,  HideUnaviFeedBack_maybe)                 // +0x11a4
NSTUB(0xfe48dc04,  LiveViewApp_handler)                     // verified (+0x11a4)
NSTUB(0xfe48e270,  LiveViewApp_handler_BL_JudgeBottomInfoDispTimerState) // verified BL 0xFE48ADC4
NSTUB(0xfe48f8ac,  LiveViewApp_handler_end)                 // verified start of next fn (+0x11a4)
NSTUB(0xfe4a96e8,  PlayMain_handler)                        // +0x11a4
NSTUB(0xfe5e9da8,  PlayMovieGuideApp_handler)               // verified in StartPlayMovieGuideApp @ 0xFE5EA204
NSTUB(0xfe49cdbc,  ShootOlcApp_handler)                     // +0x11a4

/** Display **/
NSTUB(0xfe40f06c,  MirrorDisplay)                           // +0xd98
NSTUB(0xfe40f0cc,  NormalDisplay)                           // +0xd98
NSTUB(0xfe40f09c,  ReverseDisplay)                          // +0xd98

/** EDMAC (+0x99c, verified "SetEDmac(~~)") **/
NSTUB(0xfe29e3f4,  AbortEDmac)
NSTUB(0xfe29e100,  ConnectReadEDmac)
NSTUB(0xfe29e03c,  ConnectWriteEDmac)
NSTUB(0xfe29e4bc,  RegisterEDmacAbortCBR)
NSTUB(0xfe29e494,  RegisterEDmacCompleteCBR)
NSTUB(0xfe29e5c0,  RegisterEDmacPopCBR)
NSTUB(0xfe29df84,  SetEDmac)
NSTUB(0xfe29e2a0,  StartEDmac)
NSTUB(0xfe29e4fc,  UnregisterEDmacAbortCBR)
NSTUB(0xfe29e4a8,  UnregisterEDmacCompleteCBR)
NSTUB(0xfe29e5d4,  UnregisterEDmacPopCBR)

/** Electronic Level **/
NSTUB(0xfe2eb224,  GUI_SetRollingPitchingLevelStatus)       // verified "GUI_SetRollingPitchingLevelStatus" (+0xd9c)

/** Engio (+0x99c, verified "EngDrvOut") **/
NSTUB(0xfe29f390, _EngDrvOut)
NSTUB(0xfe29f73c, _engio_write)
NSTUB(0xfe29f280,  shamem_read)

/** Eventprocs (call by name) **/
NSTUB(0xfe120c3c,  call)                                    // +0x980

/** Events (+0xd00, verified prologues & epilogues) **/
NSTUB(0xfe2c232c,  TryPostEvent)
NSTUB(0xfe2c2388,  TryPostEvent_end)
NSTUB(0xfe2be754,  TryPostStageEvent)
NSTUB(0xfe2be7b0,  TryPostStageEvent_end)

/** ExMem (+0x980) **/
NSTUB(0xfe123638,  AddMemoryChunk)
NSTUB(0xfe125ae8,  AllocateContinuousMemoryResource)
NSTUB(0xfe125a9c,  AllocateMemoryResource)
NSTUB(0xfe122bb4,  CreateMemoryChunk)
NSTUB(0xfe123398,  CreateMemorySuite)
NSTUB(0xfe1231cc,  DeleteMemorySuite)
NSTUB(0xfe125c00,  FreeMemoryResource)
NSTUB(0xfe123708,  GetFirstChunkFromSuite)
NSTUB(0xfe123158,  GetMemoryAddressOfMemoryChunk)
NSTUB(0xfe123e94,  GetNextMemoryChunk)
NSTUB(0xfe0d54fc,  SRM_AllocateMemoryResourceFor1stJob)     // +0x0
NSTUB(0xfe0d58d0,  SRM_FreeMemoryResourceFor1stJob)         // +0x0

/** GUI for old cameras (+0x980) **/
NSTUB(   0x36c10,  gui_timer_struct)                        // verified in GUI_Control_Post @ 0xFE1507FC (+0x4)
NSTUB(0xfe15264c,  gui_change_mode)
NSTUB(0xfe152e2c,  gui_local_post)
NSTUB(0xfe153454,  gui_other_post)
NSTUB(0xfe15383c,  gui_change_shoot_type_post)
NSTUB(0xfe1540c8,  gui_init_event)
NSTUB(0xfe1537b4,  gui_post_10000085)

/** GUI timers **/
NSTUB(0xfe483a9c,  CancelDateTimer)                         // verified "CancelDateTimer" (+0x11a4)
NSTUB(0xfe129a48,  CancelTimer)                             // +0x980
NSTUB(0xfe1216a0,  SetHPTimerAfterNow)                      // +0x980
NSTUB(0xfe121790,  SetHPTimerNextTick)                      // +0x980
NSTUB(0xfe129978,  SetTimerAfter)                           // +0x980

/** H264 Encoder (+0x99c) **/
NSTUB(   0x38a3c,  mvr_config)                              // verified in mvrSetDefQScale @ 0xFE281348
NSTUB(0xfe281878,  mvrFixQScale)
NSTUB(0xfe28133c,  mvrSetDefQScale)
NSTUB(0xfe281384,  mvrSetFullHDOptSize)
NSTUB(0xfe281568,  mvrSetGopOptSizeFULLHD)

/** LCD Sensor **/
NSTUB(0xfe12c598,  DispSensorStart)                         // verified "DispSensorStart" (+0x980)

/** Making the card bootable **/
NSTUB(   0x490d4,  cf_device)                               // sd_device - 0x24
NSTUB(   0x490f8,  sd_device)                               // verified in sdReadBlk @ 0xFE636B00
NSTUB(0xfe544fc8,  fsuDecodePartitionTable)                 // +0x11a4

/** Memory allocation **/
NSTUB(0xfe128298,  GetMemoryInformation)                    // +0x980
NSTUB(0xfe128244,  GetSizeOfMaxRegion)                      // +0x980
NSTUB(0xfe1284f8, _AllocateMemory)                          // verified "[MEM] NG AllocateMemory %d" (+0x980)
NSTUB(0xfe128894, _FreeMemory)                              // +0x980
NSTUB(0xfe2c254c, _alloc_dma_memory)                        // FIXED (was broken 0xfe11f3c8 in 1.1.0!)
NSTUB(0xfe2c6c28, _free)                                    // verified (+0xd00)
NSTUB(0xfe2c2588, _free_dma_memory)                         // +0xd00
NSTUB(0xfe2c6bd0, _malloc)                                  // verified (+0xd00)

/** Message queues (RAM, 100% verified) **/
NSTUB(    0x7868,  msg_queue_count)
NSTUB(    0x7480,  msg_queue_create)
NSTUB(    0x7814,  msg_queue_post)
NSTUB(    0x75d0,  msg_queue_receive)

/** PTP **/
NSTUB(0xfe36f604,  ptp_register_handler)                    // +0xd98
NSTUB(0xfe1fd318,  ptpPropSetUILock)                        // +0x99c

/** Properties (+0x0, verified) **/
NSTUB(0xfe10c5e0, _prop_cleanup)
NSTUB(0xfe10be44, _prop_request_change)
NSTUB(0xfe10c438,  prop_deliver)
NSTUB(0xfe10c4c0,  prop_register_slave)

/** Recursive locks (RAM, 100% verified) **/
NSTUB(    0xbcb8,  AcquireRecursiveLock)
NSTUB(    0xbbf8,  CreateRecursiveLock)
NSTUB(    0xbe28,  ReleaseRecursiveLock)

/** ResLock (+0x99c, verified "CreateResLockEntry") **/
NSTUB(0xfe2a21b4,  CreateResLockEntry)
NSTUB(0xfe2a26f4,  LockEngineResources)
NSTUB(0xfe2a282c,  UnLockEngineResources)

/** Semaphores (RAM, 100% verified) **/
NSTUB(    0x30c8,  create_named_semaphore)
NSTUB(    0x3358,  give_semaphore)
NSTUB(    0x3270,  take_semaphore)

/** Task info (RAM, 100% verified) **/
NSTUB(   0x358f0,  task_max)                                // FIXED: verified @ RAM 0x40A4 (+0x4 vs 1.1.0)
NSTUB(    0x4080,  get_task_by_id)
NSTUB(    0x24c4, _get_task_info_by_id)
NSTUB(    0x24c4,  is_taskid_valid)
NSTUB(   0x31170,  current_task)
NSTUB(     0x640,  current_interrupt)

/** Task sleep (RAM, 100% verified) **/
NSTUB(    0x3780,  msleep)

/** Tasks (RAM, 100% verified) **/
NSTUB(   0x3592c,  task_dispatch_hook)                      // FIXED: verified @ RAM 0x1D04 (+0x8 vs 1.1.0!)
NSTUB(    0x38fc,  task_create)
NSTUB(    0x41dc,  task_trampoline)

/** Misc **/
NSTUB(   0x6c720,  lv_path_struct)                          // verified (-0x980)
NSTUB(0xfe11b5a4,  LoadCalendarFromRTC)                     // +0x980
NSTUB(0xfe2bc8c8,  vsnprintf)                               // verified in DryosDebugMsg @ 0xFE11FE08 (+0xd00)
NSTUB(0xfe114d6c,  EnableImagePhysicalScreenParameter)      // verified "EnableImagePhysicalScreenParameter" (+0x218)
NSTUB(0xfe0d48e4,  TryReceiveMessageQueue)                  // +0x0
