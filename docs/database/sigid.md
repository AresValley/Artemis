# SigID Wiki Database

<div align="center" markdown>

  ![GitHub Release](https://img.shields.io/github/v/release/AresValley/Artemis-DB?label=Latest%20release)
  ![GitHub repo file or directory count (in path)](https://img.shields.io/github/directory-file-count/aresvalley/artemis-db/static?type=dir&label=DB%20signals)
  ![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/AresValley/Artemis-DB/total?label=DB%20requests)
  ![GitHub Release Date](https://img.shields.io/github/release-date/AresValley/Artemis-DB)

</div>

Artemis serves as a valuable resource for both personal signal collection and leveraging a vast repository of pre-identified signals. This software application allows users to curate their own collections, but its true strength lies in its integration with a comprehensive database of known signals. This database is directly sourced from the [Signal Identification Wiki](https://www.sigidwiki.com/wiki/Signal_Identification_Guide), an open-source resource collaboratively maintained by a global community of radio enthusiasts.

!!! tip "Database Revision"
    For quality control purposes, the database undergoes a rigorous review process before integration into Artemis. This review adheres to established [guidelines](https://github.com/AresValley/Artemis-DB), ensuring the accuracy and completeness of the information presented to users. The specifics of this review process are outlined in the following section.

## Modulation
A good practise (reported also on ) is to write the primary type of modulation (if known) and not all the possible variants. A practical example is reported on [Signal Identification Wiki](https://www.sigidwiki.com/wiki/Signal_Identification_Guide): there is no need to write **8-PSK** or **QPSK**, **PSK** is enough. The Artemis SigID database is provided without any modulation variants included. The recognized modulations are listed below:

### Analog
* **AM:** Amplitude Modulation
* **FM:** Frequency Modulation
* **PM:** Phase Modulation
* **LSB:** Lower Sideband
* **USB:** Upper Sideband
* **VSB:** Vestigial Sideband
* **CW:** Continuous Wave
  
### Digital
* **QAM:** Quadrature Amplitude Modulation
* **PSK:** Phase-Shift Keying
* **FSK:** Frequency-Shift Keying
* **ASK:** Amplitude-Shift Keying
* **MSK:** Minimum-Shift Keying
* **IFK:** Incremental Frequency Keying
* **OOK:** On-Off Keying
* **FDM:** Frequency-Division Multiplexing
* **BOC:** Binary Offset Carrier Modulation
* **CDMA:** Code Division Multiple Access
* **TDMA:** Time Division Multiple Access
* **FBMC:** Filter Bank Multi Carrier
* **UFMC:** Universal Filtered Multi Carrier
* **PCM:** Pulse Code Modulation
* **PPM:** Pulse Position Modulation
* **FMCW:** Frequency-Modulated Continuous Wave
* **Pulse:** Pulse

### Spread Spectrum
* **CSS:** Chirp Spread Spectrum
* **DSSS:** Direct Sequence Spread Spectrum
* **FHSS:** Frequency Hopping Spread Spectrum
* **THSS:** Time Hopping Spread Spectrum

## Locations
Locations are either countries or special token (`Worldwide`, `Europe`, etc.) . Precise location of the TX station, towns and cities are converted to their respective countries.
