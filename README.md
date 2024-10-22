# IPMI Fan Control Daemon for IBM System x3650
  3650M5 are notorious for their excessive fan speeds. Especially when encountering unsupported hardware fans ramp up, to cover power hungry peripherals like graphics cards. While that's surely the safer option, it is rather annoying to hear the box screaming multiple floors below, when the card you've added is just some low power stuff.
  
  This script will monitor CPU temperatures and overwrite fan speeds accordingly. If the card you've added has an internal temperature sensor (like most NVMEs and some NICs) you might want to add them manually.
  
  IMM2 still mantains a partial control over the fans actual speed, so actual speeds may deviate and control behaves sluggish at best.

  This python script is loosely based on [IPMI Fan Control Daemon For IBM x3650 M5](https://github.com/bubba925/IBM_System_x3650_M5_ipmi_fancontrol-ng) and it's upstream repositories.
  
  **THIS IS STILL WORK IN PROGRESS.** Don't expect the code to work properly.

  #### NOTE: 
  You use this script at your own risk, and no warranty is provided. Do not use in produciton environments.

  * Original Maintainer: Brian Wilson <brian@wiltech.org>
  * Original Author: Layla Mah <layla@insightfulvr.com>
  * Original Version: https://github.com/missmah/ipmi_tools
