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
A good practise (reported also on ) is to write the primary type of modulation (if known) and not all the possible variants. A practical example is reported on [Signal Identification Wiki](https://www.sigidwiki.com/wiki/Signal_Identification_Guide): there is no need to write **8-PSK** or **QPSK**, **PSK** is enough.

Historically, this value was strictly limited to the primary modulation type. However, its scope has evolved to also encompass related technical schemes, including advanced pulse shaping, multiplexing, and multiple access techniques.

The recognized modulations and schemes are listed below:

### Analog Modulation
* **AM**: Amplitude Modulation
* **FM**: Frequency Modulation
* **PM**: Phase Modulation
* **DSB**: Double-Sideband Modulation
* **DSB-WC**: Double-Sideband with Carrier
* **DSB-SC**: Double-Sideband Suppressed Carrier
* **DSB-RC**: Double-Sideband Reduced Carrier
* **SSB**: Single-Sideband Modulation
* **SSB-WC**: Single-Sideband with Carrier
* **SSB-SC**: Single-Sideband Suppressed Carrier
* **SSB-RC**: Single-Sideband Reduced Carrier
* **LSB**: Lower Sideband *(Often part of SSB)*
* **USB**: Upper Sideband *(Often part of SSB)*
* **VSB**: Vestigial Sideband Modulation

### Digital Keying / Digital Modulation
* **ASK**: Amplitude-Shift Keying
* **BASK**: Binary Amplitude-Shift Keying *(Equivalent to OOK)*
* **OOK**: On-Off Keying *(Equivalent to BASK)*
* **M-ary ASK**: M-ary Amplitude-Shift Keying
* **MP‑DASK**: Experimental Multi‑Parallel Differential Amplitude Shift Keying
* **FSK**: Frequency-Shift Keying
* **AFSK**: Audio Frequency-Shift Keying
* **BFSK**: Binary Frequency-Shift Keying
* **M-ary FSK**: M-ary Frequency-Shift Keying
* **GFSK**: Gaussian Frequency-Shift Keying
* **CPFSK**: Continuous Phase Frequency-Shift Keying
* **CWFSK**: Continuous Wave - Frequency Shift Keying
* **MSK**: Minimum-Shift Keying *(A type of CPFSK)*
* **GMSK**: Gaussian Minimum-Shift Keying
* **C4FM**: 4-level FSK Technology *(Introduced by Yaesu)*
* **FSK-CW**: Frequency-Shift Keying Continuous Wave
* **IFK**: Incremental Frequency Keying
* **PSK**: Phase-Shift Keying
* **BPSK**: Binary Phase-Shift Keying
* **QPSK**: Quadrature Phase-Shift Keying
* **OQPSK**: Offset Quadrature Phase-Shift Keying
* **DPSK**: Differential Phase-Shift Keying
* **SDPSK**: Symmetric Differential Phase-Shift Keying
* **DQPSK**: Differential Quadrature Phase-Shift Keying
* **D8PSK**: Differential 8-Phase-Shift Keying
* **M-ary PSK**: M-ary Phase-Shift Keying
* **APSK**: Amplitude Phase-Shift Keying *(Hybrid ASK and PSK)*
* **QAM**: Quadrature Amplitude Modulation *(Hybrid ASK and PSK)*
* **TCM**: Trellis Coded Modulation *(Modulation + Coding)*

### Pulse Modulation
* **PCM**: Pulse Code Modulation
* **PFM**: Pulse Frequency Modulation
* **DPCM**: Differential Pulse Code Modulation
* **ADPCM**: Adaptive Differential Pulse Code Modulation
* **DM**: Delta Modulation
* **ADM**: Adaptive Delta Modulation
* **CVSDM**: Continuously Variable Slope Delta Modulation
* **ΣΔ**: Sigma-Delta Modulation *(Corrected name order, kept key)*
* **PAM**: Pulse Amplitude Modulation
* **PAM4**: 4-Level Pulse Amplitude Modulation
* **PWM**: Pulse Width Modulation *(Often synonymous with PDM/PLM)*
* **PPM**: Pulse Position Modulation
* **PDM**: Pulse Duration Modulation *(Often synonymous with PWM/PLM)*
* **PLM**: Pulse Length Modulation *(Often synonymous with PWM/PDM)*
* **Pulse**: Undisclosed Pulse Modulation

### Spread Spectrum & Advanced Techniques
* **CW**: Continuous Wave *(Often baseline for other modulations like OOK)*
* **CSS**: Chirp Spread Spectrum
* **LFM**: Linear Frequency Modulation *(Type of chirp)*
* **FMCW**: Frequency-Modulated Continuous Wave *(Often used in Radar)*
* **DSSS**: Direct Sequence Spread Spectrum
* **FHSS**: Frequency Hopping Spread Spectrum
* **THSS**: Time Hopping Spread Spectrum
* **BOC**: Binary Offset Carrier Modulation *(Used in GNSS)*
* **TMBOC**: Time-Multiplexed Binary Offset Carrier Modulation
* **IM/DD**: Intensity Modulation with Direct Detection *(Optical only)*

### Multiplexing / Multiple Access / Carrier Schemes
* **FDM**: Frequency-Division Multiplexing
* **SC-FDMA**: Single-carrier Frequency-Division Multiplexing Access
* **OFDM**: Orthogonal Frequency-Division Multiplexing
* **DMT**: Discrete Multitone *(Often used with/as OFDM, e.g., in DSL)*
* **FBMC**: Filter Bank Multi-Carrier
* **UFMC**: Universal Filtered Multi-Carrier
* **OTFS**: Orthogonal Time Frequency Space
* **TDMA**: Time-Division Multiple Access
* **CDMA**: Code-Division Multiple Access
* **NOMA**: Non-Orthogonal Multiple Access

### Pulse Shaping / Modulation on Pulse (Less common stand-alone terms)
* **FMOP**: Frequency Modulation on Pulse
* **PMOP**: Phase Modulation on Pulse

### Special
* **IRIG**: Inter-range instrumentation group timecodes

## Locations
Locations are either countries or special token (`Worldwide`, `Europe`, etc.) . Precise location of the TX station, towns and cities are converted to their respective countries.
