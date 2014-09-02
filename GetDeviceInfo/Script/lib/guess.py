#********************************************************************************
# Guess project name based on specified parameters
#
# Parameters:
#   settings - settings should be used to guess project name
#
# Return:
#   Project name
#
#********************************************************************************
def projectName(settings):
  distr, name = '???', '???'

  if settings.get('HAL') == 'ATMEGA1281':
    if settings.get('ZCL_SUPPORT'):
      if settings.get('BOARD') == 'BOARD_RCB':
        if settings.get('RFCHIP') == 'AT86RF212':
          distr, name = 'INTERNAL', 'RCB_212_Zcl'
        elif settings.get('RFCHIP') == 'AT86RF230':
          distr, name = 'INTERNAL', 'RCB_230_Zcl'
        else:
          distr, name = 'INTERNAL', 'RCB_231_Zcl'
      elif settings.get('BOARD') == 'BOARD_MESHBEAN':
        if settings.get('RFCHIP') == 'AT86RF212':
          distr, name = 'INTERNAL', 'MeshBean_1281_900_Zcl'
        elif settings.get('HAL_USE_AMPLIFIER') == 'TRUE':
          distr, name = 'INTERNAL', 'MeshBean_1281_Amp_Zcl'
        else:
          distr, name = 'INTERNAL', 'MeshBean_1281_Zcl'
      else:
          distr, name = 'INTERNAL', 'MeshBean_1281_Zcl'
    else:
      if settings.get('BOARD') == 'BOARD_RCB':
        if settings.get('USE_KF_MAC') == 'TRUE':
          distr, name = 'KF', 'Kf_RcbAtm1281_231'
        elif settings.get('RFCHIP') == 'AT86RF212':
          distr, name = 'INTERNAL', 'RCB_212'
        elif settings.get('RFCHIP') == 'AT86RF230':
          distr, name = 'INTERNAL', 'RCB_230'
        else:
          distr, name = 'INTERNAL', 'RCB_231'
      elif settings.get('BOARD') == 'BOARD_MESHBEAN':
        if settings.get('RFCHIP') == 'AT86RF212':
          distr, name = 'INTERNAL', 'MeshBean_1281_900'
        elif settings.get('HAL_USE_AMPLIFIER') == 'TRUE':
          distr, name = 'INTERNAL', 'MeshBean_1281_Amp'
        else:
          distr, name = 'INTERNAL', 'MeshBean_1281'
      else:
          distr, name = 'INTERNAL', 'MeshBean_1281'

  elif settings.get('HAL') == 'ATMEGA2561':
    if settings.get('ZCL_SUPPORT'):
      distr, name = 'INTERNAL', 'MeshBean_2561_Zcl'
    else:
      distr, name = 'INTERNAL', 'MeshBean_2561'

  elif settings.get('HAL') == 'ATMEGA128RFA1':
    if settings.get('ZCL_SUPPORT'):
      if settings.get('BOARD') == 'BOARD_RCB':
        distr, name = 'INTERNAL', 'RCB_MegaRf_Zcl'
      else:
        distr, name = 'PS_MEGARF', 'STK600'

    elif settings.get('BUILD_TARGET') == 'TARGET_MAC':
      if settings.get('BOARD') == 'BOARD_RCB':
        distr, name = 'INTERNAL', 'RCB_MegaRf_Mac'

    elif settings.get('BOARD') == 'BOARD_RCB':
      if settings.get('USE_KF_MAC') == 'TRUE':
        distr, name = 'KF', 'Kf_RcbAtm128rfa1'
      else:  
        distr, name = 'INTERNAL', 'RCB_MegaRf'

    else:
      distr, name = 'MEGARF', 'STK600'

  elif settings.get('HAL') == 'AT91SAM7X256':
    if settings.get('ZCL_SUPPORT'):
      distr, name = 'PS_SAM7X_EK', 'SAM7X_EK'
    else:
      distr, name = 'SAM7X_EK', 'SAM7X_EK'

  elif settings.get('HAL') == 'AT32UC3A0512':
    if settings.get('ZCL_SUPPORT'):
      distr, name = 'PS_AVR32_EVK1105', 'AVR32_EVK1105'

  elif settings.get('HAL') == 'AT91SAM3S4C':
    if settings.get('BOARD') == 'BOARD_CUSTOM_3':
      distr, name = 'CUSTOM_3', 'CUSTOM_3'
    elif settings.get('BOARD') == 'BOARD_SAM3S_EK':
      distr, name = 'PS_SAM3S_EK', 'SAM3S_EK'

  elif settings.get('HAL') in ['ATXMEGA128A1', 'ATXMEGA256A3', 'ATXMEGA256D3']:
    if settings.get('ZCL_SUPPORT'):
      if settings.get('BOARD') == 'BOARD_STK600':
        if settings.get('HAL') == 'ATXMEGA256A3':
          distr, name = 'PS_XMEGA', 'STK600_xmega256a3'
        elif settings.get('HAL') == 'ATXMEGA256D3':
          distr, name = 'PS_XMEGA', 'STK600_xmega256d3'

      elif settings.get('BOARD') == 'BOARD_REB_CBB':
        if settings.get('RF_EXTENDER') == REB230:
          distr, name = 'PS_XMEGA', 'REB_CBB_230'
        elif settings.get('RF_EXTENDER') == REB231:
          distr, name = 'PS_XMEGA', 'REB_CBB_231'
        elif settings.get('RF_EXTENDER') == REB212:
          distr, name = 'PS_XMEGA', 'REB_CBB_212'

    else: # ZCL_SUPPORT != 1
      distr, name = 'INTERNAL', 'REB_CBB_212'

  return distr + '_' + name

#********************************************************************************
# Guess configuration name based on specified parameters
#
# Parameters:
#   settings - settings should be used to guess configuration name
#
# Return:
#   Configuration name
#
#********************************************************************************
def configName(settings):
  stack = {
    None               : 'All',
    'ALL_DEVICES_TYPES': 'All',
    'COORDINATOR'      : 'Coordinator',
    'ROUTER'           : 'Router',
    'ENDDEVICE'        : 'EndDevice',
  }[settings.get('STACK_TYPE')]

  security = {
    None                    : '',
    'NO_SECURITY_MODE'      : '',
    'STANDARD_SECURITY_MODE': '_Sec',
    'STDLINK_SECURITY_MODE' : '_StdlinkSec',
    'HIGH_SECURITY_MODE'    : '_HighSec',
    'CERTICOM_SECURITY_MODE': '_SESec',
  }[settings.get('SECURITY_MODE')]

  board = {
    None                 : '???',
    'BOARD_MESHBEAN'     : '_ZigBit',
    'BOARD_STK600'       : '_Stk600',
    'BOARD_RAVEN'        : '_Raven',
    'BOARD_USB_DONGLE'   : '_UsbDongle',
    'BOARD_SAM7X_EK'     : '_Sam7xEk',
    'BOARD_SAM3S_EK'     : '_Sam3sEk',
    'BOARD_RCB'          : '_Rcb',
    'BOARD_AVR32_EVK1105': '_Avr32Evk1105',
    'BOARD_XPLAIN'       : '_Xplain',
    'BOARD_CUSTOM_3'     : '_Custom3',
    'BOARD_REB_CBB'      : '_RebCbb',
  }[settings.get('BOARD')]

  cpu, arch = {
    None           : ('???', '???'),
    'ATMEGA1281'   : ('_Atmega1281', 'avr'),
    'ATMEGA2561'   : ('_Atmega2561', 'avr'),
    'AT90USB1287'  : ('_At90usb1287', 'avr'),
    'ATMEGA1284'   : ('_Atmega1284', 'avr'),
    'ATXMEGA128A1' : ('_Atxmega128A1', 'avr'),
    'ATXMEGA256A3' : ('_Atxmega256A3', 'avr'),
    'ATXMEGA256D3' : ('_Atxmega256D3', 'avr'),
    'ATMEGA128RFA1': ('_Atmega128rfa1', 'avr'),
    'AT91SAM7X256' : ('_At91sam7x256', 'arm'),
    'AT91SAM3S4C'  : ('_At91sam3s4c', 'arm'),
    'AT32UC3A0512' : ('_At32uc3a0512', 'avr32'),
  }[settings.get('HAL')]

  rf_chip = {
    None           : '???',
    'AT86RF212'    : '_Rf212',
    'AT86RF230'    : '_Rf230',
    'AT86RF230B'   : '_Rf230B',
    'AT86RF231'    : '_Rf231',
    'CUSTOMRF3'    : '_CustomRf3',
    'ATMEGA128RFA1': ''
  }[settings.get('RFCHIP')]

  freq = {
    None       : '_8Mhz',
    'HAL_0MHz' : '_0Mhz',
    'HAL_4MHz' : '_4Mhz',
    'HAL_8MHz' : '_8Mhz',
    'HAL_12MHz': '_12Mhz',
    'HAL_16MHz': '_16Mhz',
    'HAL_32MHz': '_32Mhz',
    'HAL_48MHz': '_48MHz',
    'HAL_64MHz': '_64Mhz',
  }[settings.get('HAL_FREQUENCY')]

  compiler = {
    None : '_Gcc',
    'GCC': '_Gcc',
    'IAR': '_Iar',
  }[settings.get('COMPILER_TYPE')]

  configName = stack + security + board + cpu + rf_chip + freq + compiler

  return configName

#********************************************************************************
# Form certification precompiled image name based on specified configuration name
#
# Parameters:
#   confName - configuration name
#
# Return:
#   Configuration name
#
#********************************************************************************
def certPrecompiledImageName(confName):
  testConf = {
    None : '???',
    'ManyToOne': '_ManyToOne',
    'NoSecFrag': '_NoSecFrag',
    'StdLinkSec': '_StdLinkSec',
    'StdSecPermTable': '_StdSecPermTable',
  }[confName]

  return 'Runner_RCB_MegaRfA1' + testConf + '.srec'

#********************************************************************************
# Guess project name and configuration name based on specified parameters
#
# Parameters:
#   settings - settings should be used to guess project and configuration names
#
# Return:
#   Tuple containing project and configuration name
#
#********************************************************************************
def projectAndConfigName(settings):
  return (projectName(settings), configName(settings))

