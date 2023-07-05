#!/bin/bash

for ((i = 3; i <= 32; i ++ ))
do
  tr181 del Device.PeriodicStatistics.SampleSet.${i}.
done

