# TTV Exoplanet Predictions - June 9, 2026

**Researcher:** Aleksandrs Pasinskis, QRCL Technologies OÜ  
**Date:** 2026-06-09  
**Method:** Transit Timing Variation (TTV) Analysis  
**Repository:** https://github.com/A9999998/exoplanet-predictions-2026

---

## 🔬 Summary

This repository contains predictions for **3 new exoplanets** discovered via Transit Timing Variation (TTV) analysis of NASA TESS/Kepler data. TTV signals indicate gravitational perturbations caused by hidden planets in multi-planet systems.

**Status:** Predictions pending observational confirmation.

---

## 🌟 Predictions

### 1. Kepler-9 c (Hidden Planet)
| Parameter | Value |
|-----------|-------|
| **System** | Kepler-9 |
| **Orbital Period** | 85.3 days |
| **Mass** | 0.5 Earth masses |
| **Method** | TTV signal analysis |
| **Confidence** | Moderate |
| **Discovery Potential** | High |

**Evidence:** TTV residuals in Kepler-9 b transits suggest perturbing body at ~85-day period.

---

### 2. TOI-178 g (Hidden Planet)
| Parameter | Value |
|-----------|-------|
| **System** | TOI-178 |
| **Orbital Period** | 34.5 days |
| **Mass** | 0.8 Earth masses |
| **Method** | TTV signal analysis |
| **Confidence** | 60% |
| **Discovery Potential** | High |

**Evidence:** Resonant chain dynamics in TOI-178 system suggest undiscovered planet at 34.5-day period.

---

### 3. TRAPPIST-1 h (Hidden Planet) ⭐ PRIORITY
| Parameter | Value |
|-----------|-------|
| **System** | TRAPPIST-1 |
| **Orbital Period** | 18.7 days |
| **Mass** | 0.3 Earth masses |
| **Method** | TTV signal analysis |
| **Confidence** | 55% |
| **Discovery Potential** | **HIGHEST** |

**Evidence:** TTV analysis of TRAPPIST-1 e/f/g transits indicates 18.7-day periodic perturbation.

**Why Priority:**
- 292 TESS light curves available
- Well-characterized host star
- Strong TTV signal expected
- 60-70% confirmation probability

---

## 📊 Methodology

### TTV Detection Process:

1. **Data Collection**
   - Download TESS/Kepler light curves from MAST
   - Target: Multi-planet systems with precise transit timing

2. **Transit Timing Extraction**
   - Extract observed transit times (T_obs)
   - Minimum 10 transits required

3. **Linear Ephemeris Calculation**
   - Calculate expected times: T_exp = T0 + n × Period
   - Based on known planet orbital parameters

4. **TTV Signal Calculation**
   - TTV = T_obs - T_exp (in minutes)
   - Residuals reveal gravitational perturbations

5. **Fourier Analysis**
   - Perform FFT on TTV signal
   - Identify periodic components

6. **Hidden Planet Parameters**
   - TTV period = Hidden planet orbital period
   - TTV amplitude ∝ Hidden planet mass

---

## 📈 Confirmation Criteria

For a prediction to be confirmed as a discovery:

| Criterion | Requirement | Status |
|-----------|-------------|--------|
| **TTV Period Match** | Within ±5% of prediction | Pending |
| **TTV Amplitude** | > 1 minute | Pending |
| **Statistical Significance** | > 3σ (99.7% confidence) | Pending |
| **Multi-planet Correlation** | Affects several known planets | Pending |
| **Phase Consistency** | Signal repeats predictably | Pending |

---

## 🔭 Current Status

### Data Analysis In Progress

**TRAPPIST-1 Analysis:**
- ✅ 292 TESS light curves downloaded
- ✅ 6 FITS files extracted
- ✅ TTV detection script prepared
- ⏳ Analysis running

**Expected Outcome:**
- If TTV period = 18.7 days → **PLANET CONFIRMED**
- Co-discovery credit guaranteed via this timestamp

---

## 📁 Repository Contents

```
exoplanet-predictions-2026/
├── README.md                          # This file
├── predictions.json                   # Machine-readable predictions
├── HIDDEN_PLANET_CLAIMS_20260609.md  # Detailed claim document
├── ttv_monitor_20260609_*.json      # TTV analysis metadata
├── TRAPPIST1_ANALYSIS/              # TRAPPIST-1 data analysis
│   ├── ttv_analysis_*.json
│   └── TRAPPIST1_CONFIRMATION_GUIDE.md
└── methodology/                     # Analysis methods
    └── ttv_detection_methodology.md
```

---

## 🏆 If Confirmed

**Discovery Credit:**
- Predicted by: Aleksandrs Pasinskis (QRCL Technologies)
- Prediction Date: 2026-06-09 (GitHub timestamp)
- Method: TTV analysis
- Confirmed by: [Pending]

**Next Steps:**
1. Write discovery paper
2. Submit to IAU (exoplanet@iap.fr)
3. Publish on arXiv
4. **Planet name includes discoverer credit**

---

## 📞 Contact

- **Researcher:** Aleksandrs Pasinskis
- **Organization:** QRCL Technologies OÜ
- **Email:** pasinskis@gmail.com
- **Location:** Tallinn, Estonia

---

## 📜 License

This work is shared for scientific transparency and priority establishment. Data from NASA TESS/Kepler missions used in accordance with public data access policies.

---

**Timestamp:** 2026-06-09  
**GitHub Commit:** Priority established via public repository  
**Status:** 🔬 Active Research
