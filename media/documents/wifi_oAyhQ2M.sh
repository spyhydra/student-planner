#!/bin/bash

# Function to turn WiFi on
wifi_on() {
  nmcli radio wifi on
}

# Function to turn WiFi off
wifi_off() {
  nmcli radio wifi off
}

# Main loop
while true; do
  wifi_off
  wifi_on
  sleep 600
done
