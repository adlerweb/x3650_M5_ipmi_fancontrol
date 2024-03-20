# IPMI Fan Control Daemon for IBM System x3650
  Forked to work with an M5 variant that has 6 fans all labeled 1A-6A.

  Two CPUs in my system. 

  Required config to have 6 fans with 2 banks even though all fans labeled A. 

  Adjusted fan curve for my system to ensure PCIE devices had enough airflow. 

  Idle CPU temps are about 41c. 

  Currently running on Unraid via User Scripts and IPMItools installed via Nerd Tools. 

# ORIGINAL FORKED README

  This port was made in an attempt to quiet down an IBM system x3650 M4.

  #### NOTE:
  I'm NOT a developer and i know nothing about perl and the unix system.
  What i did was figuring out how to modify the script according to the raw ipmi commands i've found on reddit posts and learning the tiny bit of perl i needed to know.

  The porting involved changing the raw commands, removing the get GetFanRPM as it was useless in my scenario and IBM lists their fans as 1A 1B 2A 2B.

  Also the imm2 mantains a partial control over the fans actual speed, for example:
    - setting the fans at 30% result in an actual fan speed of roughly 24%
    - sometimes the script fails to update and the imm2 takes control back over the fans speed controls.
    - Overall the real speed settings feels very coarse.

# ORIGINAL DESCRIPTION
  # IPMI Fan Control Daemon

  This script controls IPMI compatible server's fan speeds in response to CPU Temperatures provided by lm-sensors.
  This script has been tested on a Dell PowerEdge R210 II in a homelab environment, but should work on any IPMI compatible server.

  ![](what_to_expect.PNG)
  ![](sample_curve.PNG)

  #### NOTE: 
  The script puts your server into "Full Fan Speed Mode", and then modifies what "Full Speed" means,
  You have to manually use IPMI to set it to e.g. "Optimal" when you're not using the script.

  #### NOTE: 
  You use this script at your own risk, and no warranty is provided. Do not use in produciton environments.

  * Maintainer: Brian Wilson <brian@wiltech.org>
  * Original Author: Layla Mah <layla@insightfulvr.com>
  * Original Version: https://github.com/missmah/ipmi_tools

  ### What's new?
  The original script provided a "step" approach where fans would take large "steps" depending on the temps.
  In this version, scalar equations are generated to provide an easy (and quiet) slope to follow to the next step.
  These equations are simple Y=mx+b linear slopes that effectivly provide a fan "curve" based on the entries in the
  `%cpu_temp_to_fan_speed` hash table.

  ### Installation and Usage
  ```sh
  # Install dependencies (Debian, your pkg names may be different)
  apt install lm-sensors ipmitool

  # Verify IPMI modules are loaded
  lsmod | grep -i ipmi

  # Install
  cp ipmi_fancontrol-ng /usr/bin/
  cp ipmi_fancontrol-ng.service /usr/lib/systemd/system/
  chmod +x /usr/bin/ipmi_fancontrol-ng

  # Enable on boot and start
  systemctl enable ipmi_fancontrol-ng
  systemctl start ipmi_fancontrol-ng
  ```

  ### InfluxDB & Telegraf
  Metrics are output to the file `/tmp/fan_speed_telegraf` by default and can be input into InfluxDB with the following Telegraf config block:
  ```
  [[inputs.exec]]
    commands = [
      "/usr/bin/cat /tmp/fan_speed_telegraf"
    ]

    timeout = "5s"
    data_format = "influx"
  ```
  #### Metrics Available
  * Fan Speed %
  * Fan Speed HEX

  ---
  More documentation is planned, however I am available to answer basic configuration questions in the mean time.

