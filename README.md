# AQI Map

An interactive map that displays AQI scores for US cities with a population >= 100,000.

Last updated: 7/18/2024

## Table of Contents
- [Installation](#installation)
- [About the Data](#about-the-data)
- [Methods of Calculation](#methods-of-calculation)
- [Accuracy](#accuracy)
- [Sources](#sources)

## Installation

Detailed instructions on how to install and set up the project. A working API key can be obtained for free on OpenWeatherMap.org

```bash
git clone https://github.com/cadenpayne83/aqimap.git
cd projectname
npm install
```

## About the Data

Data is sourced from OpenWeatherMap.org

## Methods of Calculation

AQI scores are calculated in accordance with US EPA standards.

O3 and CO are converted from µg/m3 to ppm (parts per million), and SO2 and NO2 are converted from µg/m3 to ppb (parts per billion). Pollutants are converted using the EPA's conversion equation: (ppm) = 24.45 x concentration (µg/m3) ÷ molecular weight.

Individual AQI scores are calculated for each pollutant using the following formula:

$$
I_p = \frac{I_{Hi} - I_{Lo}}{BP_{Hi} - BP_{Lo}} (C_p - BP_{Lo}) + I_{Lo}
$$

Where Ip = the index for pollutant p

Cp = the truncated concentration of pollutant p

BPHi = the concentration breakpoint that is greater than or equal to Cp

BPLo = the concentration breakpoint that is less than or equal to Cp

IHi = the AQI value corresponding to BPHi

ILo = the AQI value corresponding to BPLo


The maximum of the individual AQI scores is reported.

The AQI breakpoints table can be found at the bottom of the file.

## Accuracy

I recognize this tool may not display fully accurate AQI data. I sourced the most accurate and detailed air quality data at my disposal, which may not be up-to-par with commercial/paid APIs. I complied with EPA standards for AQI calculations as much as possible given the limited data. This is not intended to be a commercial product, but is merely a personal project I made out of enjoyement. I look to use my skills to make the most accurate and useful tools possible.

## Sources

https://www.airnow.gov/sites/default/files/2020-05/aqi-technical-assistance-document-sept2018.pdf

https://www.epa.gov/sites/default/files/2019-11/documents/mthd-2-4.pdf

https://cfpub.epa.gov/ncer_abstracts/index.cfm/fuseaction/display.files/fileid/14285 
