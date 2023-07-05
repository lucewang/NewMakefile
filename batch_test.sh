#!/bin/bash

paths=(
  "Device.DeviceInfo.MemoryStatus.Free"
  "Device.DeviceInfo.MemoryStatus.Free"
  "Device.DeviceInfo.MemoryStatus.Free"
  "Device.DeviceInfo.MemoryStatus.X_ALU-COM_FreeFlash"
  "Device.DeviceInfo.MemoryStatus.X_ALU-COM_FreeFlash"
  "Device.DeviceInfo.MemoryStatus.X_ALU-COM_FreeFlash"
  "Device.DeviceInfo.ProcessStatus.CPUUsage"
  "Device.DeviceInfo.ProcessStatus.CPUUsage"
  "Device.DeviceInfo.ProcessStatus.CPUUsage"
  "Device.Cellular.Interface.1.X_ALU-COM_AttachedLteCellStat.ECI"
  "Device.Cellular.Interface.1.X_ALU-COM_AttachedLteCellStat.PhysicalCellID"
  "Device.Cellular.Interface.1.X_ALU-COM_AttachedLteCellStat.DownlinkEarfcn"
  "Device.Cellular.Interface.1.X_ALU-COM_AttachedLteCellStat.RSSICurrent"
  "Device.Cellular.Interface.1.X_ALU-COM_AttachedLteCellStat.SNRCurrent"
  "Device.Cellular.Interface.1.X_ALU-COM_AttachedLteCellStat.RSRPCurrent"
  "Device.Cellular.Interface.1.X_ALU-COM_AttachedLteCellStat.RSRQCurrent"
  "Device.Cellular.Interface.1.X_ALU-COM_AttachedLteCellStat.Txpower"
  "Device.Cellular.Interface.1.X_ALU-COM_AttachedLteCellStat.Cw0CQI"
  "Device.Cellular.Interface.1.X_ALU-COM_AttachedLteCellStat.Cw1CQI"
  "Device.Cellular.Interface.1.X_ALU-COM_AttachedLteCellStat.RSRQCurrent"
)

modes=(
  "Average"
  "Maximum"
  "Minimum"
  "Average"
  "Maximum"
  "Minimum"
  "Average"
  "Maximum"
  "Minimum"
  "Latest"
  "Latest"
  "Latest"
  "Latest"
  "Latest"
  "Latest"
  "Latest"
  "Latest"
  "Latest"
  "Latest"
  "Latest"
)

for ((i = 3; i <= 32; i ++ ))
do
  tr181 add Device.PeriodicStatistics.SampleSet.
  
  # Loop through the array and execute the code
  for ((j=0; j<${#paths[@]}; j++)); do
    tr181 add Device.PeriodicStatistics.SampleSet.${i}.Parameter.
    reference="${paths[j]}"
    mode="${modes[j]}"
    tr181 -fs Device.PeriodicStatistics.SampleSet.${i}.Parameter.$((j+1)).Reference "$reference"
    tr181 -fs Device.PeriodicStatistics.SampleSet.${i}.Parameter.$((j+1)).CalculationMode "$mode"
    tr181 -fs Device.PeriodicStatistics.SampleSet.${i}.Parameter.$((j+1)).Enable 1
  done
  
  tr181 -s Device.PeriodicStatistics.SampleSet.${i}.X_ALU-COM_InternalFrequency 60
  tr181 -s Device.PeriodicStatistics.SampleSet.${i}.SampleInterval 900
  tr181 -s Device.PeriodicStatistics.SampleSet.${i}.ReportSamples 673
  tr181 -s Device.PeriodicStatistics.SampleSet.${i}.Name "ODU-Test"
  tr181 -s Device.PeriodicStatistics.SampleSet.${i}.Enable 1
done

