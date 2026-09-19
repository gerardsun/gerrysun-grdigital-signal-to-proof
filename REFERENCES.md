# References

Signal-to-Proof is a public reference implementation informed by established work on advertising measurement, causal inference, geo experimentation, and counterfactual estimation.

## Observational measurement versus randomized experiments

Brett R. Gordon, Florian Zettelmeyer, Neha Bhargava, and Dan Chapsky. “A Comparison of Approaches to Advertising Measurement: Evidence from Big Field Experiments at Facebook.” *Marketing Science* 38(2), 2019, 193–225.  
https://doi.org/10.1287/mksc.2018.1135

The paper compares common observational approaches with randomized field experiments and documents how observational estimates can diverge materially from experimental effects even with rich covariates.

## Bayesian structural time-series counterfactuals

Kay H. Brodersen, Fabian Gallusser, Jim Koehler, Nicolas Remy, and Steven L. Scott. “Inferring causal impact using Bayesian structural time-series models.” *Annals of Applied Statistics* 9, 2015, 247–274.  
https://research.google/pubs/inferring-causal-impact-using-bayesian-structural-time-series-models/

## Geo experimentation

Google Meridian GeoX. Open-source geographic incrementality experimentation.  
https://developers.google.com/meridian/geox  
https://github.com/google/meridian-geox

Meta GeoLift. Open-source geo-experimental methodology using synthetic-control methods.  
https://github.com/facebookincubator/GeoLift

## Interpretation principle used in this repository

These references support a common measurement discipline: attribution and association can be operationally useful, but causal claims require an identification strategy capable of constructing a credible counterfactual.
