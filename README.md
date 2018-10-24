# NetOps---Day-N-Automation

**Cisco Partner Architect Exchange - Sample code**


This repo includes the sample code used durign the demo at PCAE

This application will monitor device configuration changes. 
It could be executed on demand as in this lab, periodically (every 60 minutes, for example) or continuously.
It will collect the configuration file for each DNA Center managed device, compare with the existing cached file, and detect if any changes.
 - When changes detected, identify the last user that configured the device, and create a new ServiceNoe incident.
 - Automatically roll back all non-compliant configurations, or save new configurations if approved in ServiceNow.
 - Send Exec commands to devices using PubNub.
 - Compliance checks included:
    - no Access Control Lists changes
    - no logging changes
    - no duplicated IPv4 addresses
    
 This code is to be used for learning and in labs environment only.
