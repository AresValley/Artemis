# Frequently Asked Questions

### What about an automatic signal recognition feature?
This question has been asked countless times, and for good reason: in many fields, machine learning (ML) has disrupted the way we solve problems, and when applied to the right field, you can get outstanding results. **So why not on signals?**

Well, the story dates back to at least 2017 when I started discussing it with several people on the rtl-sdr blog: at first, it seemed promising, but like many things, all that glitters is not gold. Let us proceed in order: 

#### ML / Deep Learning approach
A machine learning/neural network approach would not be complex (from a technical standpoint) if there were not the problem of the dataframe completeness. To be effective, neural models need to be trained on a large number of entries. The precise number can vary and strongly depends on the nature of data used for training, but commonly, numbers can be tens of thousands of entries or even more, for example. This would not be a significant concern in the case of RF signals because the various encodings that differentiate can be created artificially using for example [Fldigi](http://www.w1hkj.com/). To make these synthetic signals more like a real one, noise and artificial distortions can be added. However, this approach allows us to have a spectrum that ranges only over civilian, non-proprietary, and non-military signals (a little bit more than 150 out of 500, in the best-case scenario). Many efforts have been made in this field and some excellent results have been reported below:

- [O’Shea, Corgan, and Clancy](https://arxiv.org/pdf/1602.04105) - Training Size: 900000 signals, 11 modulations
- [Stefan Scholl](https://arxiv.org/pdf/1906.04459) - Training Size: 120000 signals, 18 modulations
- [Stefan Scholl](https://panoradio-sdr.de/automatic-identification-of-160-shortwave-rf-signals-with-deep-learning/) - Training Size: 1.2 million signals, 143 modulations tested in HF

Therefore, The main point is to have a good quality data frame to train the model; this is not always an easy task for the above reasons. Subsequently, as Stefan Scholl pointed out on his blog, similar modulations (MFSK-32 vs Olivia 16/500) can significantly decrease the effectiveness of discrimination. The quality of reception can also influence the result as well:  high SNR cannot always be an ideal point since the reception can be disrupted by interference or fading.

#### Classical Audio Analysis
More classical methods, such as similarity recognition between audio samples (such as using Mel-frequency cepstral coefficients, for example), could be effective, albeit marginally, if applied to the 500 signals audio sample library from sigID wiki. With the same signal encoding, the content of the signal alone can affect the similarity index and, thus, the method's effectiveness. Listening to a signal with the same modulation but encoding different information can significantly decrease the accuracy of signal recognition.
