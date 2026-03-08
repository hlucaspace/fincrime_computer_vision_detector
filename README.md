# FinCrime Bank Check AI Fraud Detection — Computer Vision POC

## PROBLEM STATEMENT

Despite digital fraud prevention has matured, physical and scanned document fraud remains widely used and continues to be a critical exposure, which remains largely unaddressed. The volumes of bank checks in the US have declined by over 80% over the last 30 years, yet banks reported 680,000 cases of checks fraud in the US in 2023, which nearly doubled the number reported in 2021 (Federal Reserve Bank of Boston, 2023).
According to the survey provided by the Federal Reserve Risk Officer Survey (2024), check fraud loss expense accounted for 31% of reported fraud loss categories, followed by debit card fraud at 39%. Senior risk specialists at institutions using services offered by Federal Reserve stated how checks fraud remains more challenging to detect than other fraud types and still requires additional resources to review.
The operational burden remains active and measurable - Southern First Bank, a mid-size retail bank, was manually reviewing approximately 2,400 checks per month before implementing an AI-assisted solution (Nasdaq Verafin, 2025). This equates to roughly 80 checks per day, a process that is slow, inconsistent, and unscalable as fraud volume grows, and expensive relative to the value it delivers at the triage stage.
The emergence of AI has accelerated rapidly and continues to evolve, and it is increasingly on banks' radar as a potential solution to scale fraud detection to the next level. The question is no longer whether AI can support checks fraud screening, but which direction offers the longevity to deliver sufficient accuracy and reliability to be trusted in a regulated financial environment.


## ABOUT THIS PROJECT
Built as a portfolio project to demonstrate applied AI product thinking in financial crime prevention. <br />

The following is covered as **in-scope**:
- Identifying a real business problem with quantified impact
- Experimenting with appropriate AI tooling using a pre-trained CV model via API
- Building a working proof of concept without an ML engineering background
- Thinking critically about model limitations, production requirements, and risk
- Articulating a credible path from proof of concept to production
- 
**Out of Scope:**
- Building a production fraud detection system - the model used is publicly available and is not suitable for production fraud detection without significant further validation.
- Fine-tuning the model from the result
- Real bank checks containing actual PII
- PII, SPI and their regulatory bindings
- Measuring how accurate the pre-trained CV model is in production conditions
*This is an AI PM portfolio project. 




## OBJECTIVE
This POC investigates whether a Computer Vision object detection model can serve as a reliable automated first-pass triage layer for checks fraud detection — reducing manual intervention workload while maintaining sufficient accuracy to be trusted in a financial sector context.
It is not the intention of this POC to build a model from scratch, nor to fine-tune it. Fine-tuning would require a bank's own proprietary labeled checks dataset, which is outside the scope of this exercise. Instead, this POC experiments with a publicly available pre-trained model to evaluate whether it meets the accuracy thresholds defined in the hypothesis — determining if it is a plausible candidate for a pilot, without the overhead of building or the need to fine-tune a model.
This POC evaluates one candidate model. A rigorous model selection process would evaluate multiple candidates before proceeding to pilot. The evaluation framework is described in the Recommendations section below.


## HYPOTHESIS

>The core belief is that Computer Vision has the capability to support the bank checks screening process. If object detection is applied as an automated first-pass triage layer in checks verification workflows, then banks will be better positioned to detect and mitigate checks fraud by surfacing incomplete or anomalous documents before they reach a human fraud reviewer.
As a POC, this hypothesis has two distinct and independently measurable components:

**1. Speed**

Fast verification takes around 1 to 3 minutes utilising automated processing (Fourthline, 2025). Multiple parties and rounds of verification contribute to clearing times that add to the validation time exponentially.
An automated CV triage layer should reduce that first-pass field detection check from minutes to seconds. The speed component of this hypothesis is considered validated when mean time from checks image submission to initial risk flag stays consistently under 5,000ms — compared to an estimated 1 to 3 minutes for a trained human reviewer performing the same first-pass check.

**2. Accuracy**

The core essence of the value is when a model is reliable enough to trust. As a POC, the following conditions should be met for a model to be considered viable to move to pilot:
- Precision: achieve a mean of 75% or above
- Recall: achieve a mean of 85% or above
- F1 Score: achieve a mean of 0.80 or above

Precision, recall, and F1 targets above are the criteria used to evaluate whether the model itself is suitable for a pilot.


## SOLUTION OVERVIEW

The pre-trained model was built to detect and measure 8 specific check fields. 

**Fields Checked on Every checks**

| Field |
|---|
| Signature 
| Account Number 
| Amount in Digits 
| Amount in Words 
| checks Number
| Issue Date
| Issuing Bank 
| Receiver Name 

Based on the model, the following additional features were added:

1. Detect the presence or absence of critical document fields
2. Report a confidence score for each detected field
3. Assign an overall risk rating of Low, Medium, or High based on completeness
4. Visually annotate the document with bounding boxes showing what was detected. <br />

**Note: bounding boxes doesn't always reflect accurately. It is only a visualisation feature to help detecting the fields while calculating the metrics. This does not affect precision, recall, or F1 calculations. Boxes are categorized into green (if the original model's field confidence returns higher than 65%) or orange (if the original model's field confidence returns less than 65%)**

**Risk Rating Logic** 

| Rating | Condition |
|---|---|
| HIGH RISK | 3 or more fields missing |
| MEDIUM RISK | 1 to 2 fields missing or 2 or more low confidence detections |
| LOW RISK | All fields detected with ≥ 65% confidence |



**On Ground Truth and Manual Calculation**

Precision, recall, and F1 scores in this POC were calculated manually. The pre-trained model was trained on approximately 300 images across different check formats. This led to this exercise requiring manual inspection to experiment the hypothesis.

**Experiment Limitation**

20 sample fake bank checks images were used, not from the pre-trained model's training images, due to the following:
- Fast MVP to validate demand
- Low cost for experimentation
- Accuracy tradeoff is acceptable at this stage
- Focus on learning the baseline, not achieving near production deployment



## MODEL LIMITATION
This is a POC where real bank checks were not used since they contain PII, and also to avoid breaching security and privacy. Therefore, deploying this to production as-is would not be appropriate.

**Dataset Size**

The model was trained on approximately 300 images. Production-grade document fraud detection would require tens of thousands of labeled examples across diverse document types, print qualities, lighting conditions, and scanner resolutions.

**Detection Only, Not Verification**

The model detects whether a field exists, not whether the field content is valid, which is out of scope. The model is not capable to perform the following:

- Verify that a signature matches a stored reference signature
- Confirm the amount in digits matches amount in words numerically
- Confirm an account number against a live banking system


**Single Document Type**

This model was trained specifically on bank checks. While a single document type model can be used in production with constraints, ideally a multimodal approach would be needed covering a wider range of document types and accuracies as listed in the "Detection Only, Not Verification" sub-section above.





## POC PERFORMANCE

Manually inspecting the sampled 20 checks provided the following results:

**Detection Summary**

| Metric | Result |
|---|---|
| Total fields detected above 65% confidence | 54 of 160 possible |
| Total fields detected below 65% confidence | 19 of 160 possible |
| Total fields not detected | 87 of 160 possible |
| Average fields detected per checks | 2.7 of 8 |

**Accuracy Metrics**

| Metric | Result | Hypothesis Target | Pass / Fail |
|---|---|---|---|
| Mean Precision | 86.00% | ≥ 75% | PASS |
| Mean Recall | 38.81% | ≥ 85% | FAIL |
| Mean F1 Score | 0.53 | ≥ 0.80 | FAIL |
| Mean Inference Speed | 0.06s | < 5,000ms | PASS |

**What These Results Mean**

While precision resulted at 86% means, recall was at 38.81%, which flagged as "Missing" fields most of the time. Rather than hallucination, it drifted toward False Negative, essentially forming blindness. At this stage, due to limitations in the pre-trained model documentation, it is uncertain what types of bank checks the model was trained on. Speed at 60ms surpasses the hypothesis target of under 5,000ms, confirming the architecture is fast enough for real-time triage use.


## CONCLUSION

This POC determined whether a publicly available pre-trained Computer Vision model could serve as a reliable first-pass triage layer for bank check fraud detection by measuring the accuracy thresholds required to be considered a viable pilot candidate.
While 86% precision supports the model not generating false detections, significant recall failure at 38.81% (even Mean F1 Score was 0.53, which is still low) caused explaining how the model was nearly blind to most fields on unfamiliar bank check formats.
 This model can be kept as a reference point, but it is nowhere near meeting the needs of the challenges that banks face.
On the other side, the infrastructure operates as expected.The end-to-end architecture correctly ingests bank check images, calls the API, applies business logic, surfaces a structured risk rating, and visually annotates detections in under average 60 milliseconds. 


## RECOMMENDATION
The following three recommendations are proposed as next steps:

1. A few additional pre-trained models need to be experimented by going through a similar  process. The models need to pass the hypothesis thresholds above to ensure more rigorous experiments can be conducted before moving to pilot.

2. When experimenting other models, a standardized set of fields (compared to the 8 fields of this POC) should be defined before evaluating additional models to reduce biased evaluation.


3. Each candidate model should be evaluated across the following dimensions:

| Dimension | What to Measure |
|---|---|
| Accuracy | Mean Precision, Recall, F1 across 20 sample checks |
| Speed | Mean inference time per image |
| Field Coverage | How many of the standard field set does the model detect |
| Dataset Size | How many images was the model trained on |
| Failure Modes | Which fields does it consistently miss and why |


If no publicly available pre-trained model meets the hypothesis thresholds, the recommendation is the following:

1. Fine-tune the models from the result and reiterate going through the same process

2. Evaluate commercial document verification APIs such as AWS, GCP, Azure before any decision to build a custom model.



## Sources
- Nasdaq Verafin Global Financial Crime Report, 2024
- Federal Reserve Bank of Boston, 2023
- Federal Reserve Risk Officer Survey, 2024