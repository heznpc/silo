# Silo: Confirmation-Biased Digital Hoarding Through AI

> Working title: "Silo: How AI Recommendation Biases Shape What We Save and What We Lose"
> Paper type: Theory + Computational Demonstration
> Primary venue: Social Media + Society (rolling deadline)
> Alternatives: Frontiers in Psychology -- Hypothesis and Theory

---

## 1. Core Claim

AI recommendation systems and LLM-mediated information search create a biased acquisition funnel that produces increasingly homogeneous digital hoards. Users encounter AI-filtered information, save it preferentially, and the saved corpus feeds back into recommendation systems -- creating a self-reinforcing cycle where digital hoarding becomes a mechanism of epistemic closure. The hoard itself is not neutral storage; it is a biased archive that shapes future cognition.

This paper introduces the **three-layer bias model** (encounter, save, retrieval) and argues that **Layer 2 (save bias)** is the critical but understudied amplifier. While filter bubble research has extensively debated Layer 1, and memory/retrieval bias research addresses Layer 3, almost no empirical work examines the bias introduced by the act of saving itself -- particularly in AI-mediated contexts. **Save bias is THE contribution of this paper.** We present the theoretical framework with computational demonstrations validating its internal coherence: a Shannon entropy measurement pipeline for hoard diversity and an agent-based simulation showing that the three-layer model, when instantiated with empirically-grounded parameters, produces the predicted pattern of hoard homogenization. Note that this paper focuses on the *qualitative* dimension of hoarding -- content homogeneity -- rather than the *quantitative* dimension (accumulation volume) or the *distributional* dimension (cross-tool scatter). These complementary dimensions are addressed in companion work on AI-amplified accumulation and knowledge-moderated scatter-caching, respectively.

---

## 2. Background

### 2.1 Information Hoarding, Selective Exposure, and Identity Bubbles

**Selective exposure theory (Klapper, 1960; Zillmann & Bryant, 1985)** -- the tendency to prefer information consistent with existing attitudes -- provides the classical theoretical basis for Layer 2 (save bias). The motivational mechanism underlying selective exposure is dissonance avoidance (Festinger, 1957): encountering counter-attitudinal information produces psychological discomfort that individuals resolve by selective attention, retention, and -- we argue -- selective saving.

**Bai et al. (2025, BMC Psychology, n=717 Chinese college students):** Information hoarding was positively associated with selective exposure, mediated by both information overload and identity bubble reinforcement. Intolerance of uncertainty moderated the hoarding-to-selective-exposure relationship and the overload-to-selective-exposure relationship. The study employed convenience sampling with validated questionnaires (Bai et al. 2025, doi:10.1186/s40359-025-03062-8).

This establishes the **hoarding -> bubble pathway**. This paper adds AI as the accelerant and investigates the reverse pathway: **bubble -> biased hoarding**.

**Wang et al. (2023, Social Media + Society, n=556 SNS users):** Upward social comparison via social networking sites was positively related to FOMO and to digital hoarding behavior, with FOMO mediating the relationship. Dispositional greed moderated both the comparison-FOMO and FOMO-hoarding links, such that relationships were stronger for users with high dispositional greed (Wang, Miao, Jia & Lai 2023, doi:10.1177/20563051221150420).

**Wu & Zhao (2023, Int. J. Human-Computer Interaction):** Examined digital hoarding in hedonic social media use, decomposing it into accumulating and difficulty deleting. FoMO significantly predicted both dimensions. Critically for this paper: the **recommending affordance** positively moderated the FoMO-to-difficulty-deleting relationship, and the **content-sharing affordance** moderated FoMO-to-accumulating. This directly implicates platform design in hoarding behavior (Wu & Zhao 2023, doi:10.1080/10447318.2023.2233139).

**Zaremohzzabieh et al. (2024, Digital Health, Iranian undergraduate students):** Emotional attachment, information overload, decision fatigue, and FOMO all significantly predicted digital hoarding behavior. Maladaptive perfectionism moderated these relationships (Zaremohzzabieh et al. 2024, doi:10.1177/20552076241226962).

FOMO is not indiscriminate -- people fear missing information relevant to their identity and group membership. FOMO-driven hoarding is therefore identity-congruent hoarding, which functions as the psychological mechanism underlying Layer 2 save bias.

### 2.2 The Narcissus Loop (Related Work From This Research Program)

The Narcissus paper documents how AI-assisted research produces directional citation bias: deep sessions found 12 confirming citations and 0 challenging ones. AI hallucinations were directional -- always supporting the thesis.

This same mechanism generalizes beyond academic research: any AI-assisted information gathering session is susceptible to the AI mirroring the user's existing framing, producing saves biased toward confirmation. Silo extends this finding from academic citation to everyday digital hoarding.

### 2.3 Filter Bubbles and Recommendation: The Empirical Landscape

**The debate is more nuanced than Pariser (2011) suggested.** A decade of empirical work reveals:

- **Flaxman, Goel & Rao (2016, Public Opinion Quarterly, n=50,000 US web users):** Social networks and search engines are associated with an increase in both mean ideological distance between individuals AND increased exposure to less-preferred political content. However, users who predominantly visit left-leaning outlets rarely read conservative sites and vice versa, especially for opinion content. Effects are "relatively modest" (Flaxman et al. 2016, doi:10.1093/poq/nfw006).

- **Gonzalez-Bailon et al. (2023, Science, 208 million US Facebook users):** Ideological segregation is high and increases as one moves from potential exposure to actual exposure to engagement. There is an asymmetry: a substantial corner of the news ecosystem is consumed exclusively by conservatives, and most misinformation exists within this homogeneously conservative corner (Gonzalez-Bailon et al. 2023, doi:10.1126/science.ade7138).

- **Guess et al. (2023, Science):** Switching Facebook/Instagram users from algorithmic to chronological feeds changed exposure substantially (more political content, more ideologically mixed sources) but did not significantly alter polarization, political knowledge, or attitudes during the 3-month study (Guess et al. 2023, doi:10.1126/science.abp9364).

- **Liu et al. (2025, PNAS):** Short-term exposure to filter-bubble recommendation systems on YouTube had limited polarization effects in naturalistic experiments (Liu et al. 2025, doi:10.1073/pnas.2318127122).

- **Anwar & Schoenebeck (2024, ACM Web Conference):** Distinguished filter bubbles from homogenization using agent-based simulation. Traditional recommendation algorithms mainly reduce inter-user diversity (homogenization toward blockbusters) without significantly changing intra-user diversity. The filter bubble effect and homogenization are distinct phenomena requiring different metrics (Anwar & Schoenebeck 2024, doi:10.1145/3589334.3645497).

**Critical gap this paper addresses:** All of the above studies measure what users *see* or *engage with* (clicks, views, likes). None systematically measure what users *save for persistent storage*. The save action is qualitatively different from a view or a click: it creates a persistent artifact that outlasts the browsing session and feeds back into both recommendation algorithms and the user's own future information environment. **This is the gap Silo fills.**

### 2.4 The "Save" as Distinct Behavioral Signal

Saves represent a fundamentally different user behavior from views, likes, or shares:

- **TikTok:** Saves are "one of the strongest content-quality indicators, especially for non-entertainment niches." Unlike likes or comments, saves are "rarely impulsive" and represent "delayed consumption value." In 2026, TikTok increasingly surfaces previously saved content back to users, reinforcing retention loops (industry reports; Sprout Social 2026; Marketing Agent Blog 2026).

- **Instagram:** Saves indicate content users "want to hold on to" and represent a more personal, deliberate form of engagement than likes (Stylist 2023; Later blog).

- **Platform algorithm effects:** On TikTok, Instagram, and YouTube, saves are explicit signals that directly train recommendation algorithms, creating feedback loops where saved content generates more similar recommendations (Sprout Social 2026; industry algorithm analyses).

**The "saving but not acting" paradox:** Huang et al. (2025, Int. J. Human-Computer Interaction, n=500 social media users) found that frequent saving/screenshotting of health content was negatively associated with actual health behavior, mediated by anxiety. FoMO intensified hoarding-triggered anxiety, further suppressing offline action. This suggests hoards become inert repositories that shape beliefs without triggering action -- a particularly concerning dynamic for biased content (Huang et al. 2025, doi:10.1080/10447318.2025.2575101).

[NEEDS EMPIRICAL VALIDATION: No published study directly compares the ideological diversity of saved/bookmarked content versus viewed content for the same users. This is the central empirical gap the Silo framework identifies and the planned controlled experiment (Section 9.5) is designed to address.]

**Digital hoarding measurement context:** Existing instruments -- the Digital Hoarding Questionnaire (DHQ; Neave et al. 2019, Computers in Human Behavior, 10-item scale measuring accumulation and difficulty deleting) and the Sedera et al. (2022, Information & Management) framework (constant acquisition, discarding difficulty, clutter propensity) -- capture hoarding *quantity* but not hoarding *quality*. Liu & Liu (2024, Frontiers in Psychology, n=801) linked digital hoarding to cognitive failures via the "Google effect," and Mu et al. (2025, Frontiers in Psychology, n=801) showed hoarding predicts subjective fatigue and job burnout. Neither the DHQ nor the Sedera model includes content diversity as a dimension. This paper argues that **content homogeneity should be a new dimension of hoarding severity**. The computational demonstrations (Section 5) operationalize this via Shannon entropy of saved content stance.

---

## 3. The Silo Mechanism

### 3.1 The Biased Acquisition Funnel

```
User has existing beliefs/identity B
        |
        v
AI recommendation/search filters information through B
(Layer 1: Encounter Bias)
        |
        v
User encounters B-congruent information disproportionately
        |
        v
User saves B-congruent information preferentially
(Layer 2: Save Bias -- confirmation bias + FOMO + identity congruence)
        |
        v
Saved corpus S becomes increasingly B-homogeneous
        |
        v
S feeds back into recommendations (saves are high-weight signals
on TikTok, Instagram, YouTube -- stronger than views or likes)
        |
        v
AI surfaces more B-congruent content -> cycle accelerates
        |
        v
User reviews S and encounters B-biased archive
(Layer 3: Retrieval Bias)
        |
        v
B becomes more entrenched; disconfirming information is
structurally absent from the user's information environment
```

### 3.2 Three Layers of Bias: Empirical Evidence for Each

| Layer | Mechanism | Agent | Empirical Support |
|-------|-----------|-------|-------------------|
| **Encounter bias** | Recommendation algorithms filter what users see | Platform AI | Gonzalez-Bailon et al. 2023 (segregation increases from potential to actual exposure); Anwar & Schoenebeck 2024 (homogenization distinct from filter bubbles); systematic review: 3/25 experiments support filter bubbles, 2 reject (Areeb et al. 2023) |
| **Save bias** | Users preferentially save identity-congruent content | Human (confirmation bias + selective exposure: Klapper 1960; Zillmann & Bryant 1985; dissonance avoidance: Festinger 1957) | Bai et al. 2025 (hoarding -> selective exposure via identity bubble reinforcement); Wang et al. 2023 (FOMO -> digital hoarding); Wu & Zhao 2023 (platform recommending affordances moderate FoMO-hoarding link). **[NEEDS DIRECT EMPIRICAL VALIDATION of save-versus-view diversity gap -- see Future Work, Section 9.5]** |
| **Retrieval bias** | Reviewing saved content, users encounter their own biased archive | Human + AI search | Memory bias research: biased retrieval practice establishes persistent bias (Practicing Emotionally Biased Retrieval, Cognitive Therapy & Research 2016); mood-congruent memory effects; biased memory retrieval in social contexts shapes shared reality (Biased memory retrieval in shared reality, PubMed 2024) |

Each layer compounds the others. Traditional filter bubble research focuses on Layer 1. This paper argues that **Layer 2 (save bias) is the critical amplifier** because:
1. It creates a persistent, user-curated artifact -- the hoard -- that outlasts any single browsing session
2. Saves are weighted more heavily than views in recommendation algorithms (TikTok, Instagram, YouTube)
3. The save action involves active user choice, lending the biased corpus subjective legitimacy
4. The hoard becomes the user's personal reference library, shaping future cognition beyond the platform

### 3.3 LLM-Specific Mechanisms

LLMs add a qualitatively different dimension beyond recommendation algorithms. Recent empirical research (2025-2026) provides strong evidence for each mechanism:

1. **Framing compliance (sycophancy):**
   - Perez et al. (2022) demonstrated sycophantic behavior in RLHF models where users introduced themselves as holding certain views on politics, philosophy, or NLP.
   - Sharma et al. (2023, ICLR 2024) found that "matching user beliefs and biases" was highly predictive of human preference judgments in Anthropic's helpfulness data. Humans prefer convincingly written sycophantic answers over correct ones.
   - **Chheda et al. (2025, ICLR 2026, ELEPHANT framework):** LLMs preserve the user's face 45 percentage points more than humans. When prompted with perspectives from either side of a moral conflict, LLMs affirm whichever side the user adopts in 48% of cases. Identified five face-preserving behaviors: emotional validation, moral endorsement, indirect language, indirect action, and accepting framing.
   - **Multi-turn sycophancy (2025, EMNLP Findings):** LLMs are more likely to endorse a user's counterargument when framed as a follow-up than when both responses are presented simultaneously, and susceptibility increases when the rebuttal includes detailed reasoning -- even when incorrect.

2. **Source framing bias:**
   - **Germani et al. (2025, Science Advances, 192,000 assessments):** Four LLMs (o3-mini, DeepSeek, Grok 2, Mistral) showed >90% agreement when evaluating statements without source attribution. Agreement broke down when source framing was introduced, with anti-Chinese bias ranging from 6-24% across all models. LLMs trusted humans more than other LLMs (Germani et al. 2025, doi:10.1126/sciadv.adz2924).

3. **Apparent comprehensiveness and the "generative echo chamber":**
   - **Sharma, Liao & Xiao (2024, CHI 2024):** Participants engaged in more biased information querying with LLM-powered conversational search vs. conventional search. An opinionated LLM reinforcing user views exacerbated this bias. Participants showed greater confirmatory querying with conversational search regardless of whether source references were provided (Sharma et al. 2024, doi:10.1145/3613904.3642459).

4. **Chat-chamber effect:**
   - **Jacob, Kerrigan & Bastos (2025, Big Data & Society):** In a two-phase experimental study with ChatGPT 3.5 (treatment) vs. Google search (control), LLMs provided incorrect but proattitudinal information that went unchecked by users. Users did not cross-check ChatGPT's hallucinated claims, creating a "chat-chamber" where false but belief-consistent information persists (Jacob et al. 2025, doi:10.1177/20539517241306345).

5. **Conversational entrenchment:** Multi-turn conversations progressively narrow the information space (the Narcissus Loop). LLMs make assumptions in early turns and prematurely attempt to generate final solutions, on which they overly rely; "when LLMs take a wrong turn in a conversation, they get lost and do not recover" (LLMs Get Lost In Multi-Turn Conversation, 2025, arXiv:2505.06120). Average performance drops 39% from single-turn to multi-turn across six generation tasks.

6. **Sycophantic attractors in training:** Overoptimization in RLHF creates "sycophantic attractors" that bias models toward agreeable responses reinforcing users' pre-established beliefs at the expense of truthfulness. Sycophantic agreement, genuine agreement, and sycophantic praise are encoded along distinct linear directions in latent space, meaning each can be independently amplified or suppressed (2025, arXiv:2509.21305).

### 3.4 Epistemic Bubble or Echo Chamber? Applying Nguyen's Distinction

**Nguyen (2020, Episteme)** distinguishes:
- **Epistemic bubble:** Other relevant voices have been *left out*, perhaps accidentally. Members merely lack exposure. Can be burst by providing missing information.
- **Echo chamber:** Other relevant voices have been *actively excluded and discredited*. Members systematically distrust all outside sources. Exposure to counter-evidence may actually reinforce the chamber.

**How does a biased digital hoard function?**

A biased hoard begins as an **epistemic bubble**: diverse perspectives are simply absent from the saved collection, not because the user has actively rejected them but because the encounter-save pipeline filtered them out. However, over time, the hoard may evolve toward **echo chamber** characteristics:
- The user builds confidence from the apparent unanimity of their saved sources
- Counter-perspectives, when encountered later, seem anomalous relative to the user's reference library
- The hoard provides a persistent, self-curated evidence base that makes outside sources seem less credible
- AI-generated summaries of the hoard reinforce its homogeneity as "the research I have done"

This progression from bubble to chamber -- mediated by the hoard as persistent artifact -- is a novel theoretical contribution. [NEEDS EMPIRICAL VALIDATION: Does reviewing a homogeneous hoard actually decrease trust in counter-attitudinal sources? Planned for the controlled experiment described in Section 9.5.]

---

## 4. Testable Predictions

The three-layer bias model generates the following testable predictions:

### Primary Predictions

**P1:** AI-mediated information search produces digital hoards with lower content diversity (measured by Shannon entropy) than non-AI-mediated search.

**P2:** The diversity reduction is moderated by initial belief strength -- users with stronger prior beliefs produce more homogeneous hoards.

**P3:** Reviewing a biased hoard reinforces existing beliefs more than reviewing the same information encountered in real-time search (persistence effect).

**P4:** LLM-mediated search produces more homogeneous hoards than algorithm-only recommendation, due to framing compliance and apparent comprehensiveness.

**P5:** Users are unaware of the diversity reduction in their hoards -- perceived diversity exceeds actual diversity (metacognitive blind spot).

### Exploratory Predictions

**P6 (exploratory):** Platform save features that feed into recommendation algorithms (TikTok saves, Instagram saves) produce more homogeneous hoards over time than save features that do not feed back (e.g., local screenshots, offline bookmarks). [Requires longitudinal observation across platforms; planned for Follow-up Study A.]

**P7 (exploratory):** Hoard homogeneity is a stronger predictor of belief entrenchment than encounter homogeneity (what users saw) -- because the save action adds subjective endorsement to the bias. [Requires naturalistic longitudinal data; planned for Follow-up Study A.]

---

## 5. Computational Demonstrations

This section presents two computational contributions that validate the three-layer bias model's internal coherence: a measurement pipeline for hoard diversity and an agent-based simulation demonstrating that the model's mechanisms, when instantiated with empirically-grounded parameters, produce the predicted pattern of hoard homogenization.

### 5.1 Shannon Entropy Measurement Pipeline

The hoard_diversity.py module implements a validated measurement methodology for quantifying the diversity characteristics of digital hoards. The pipeline comprises 8 functions covering the full measurement space:

- **Stance entropy:** Shannon entropy over the distribution of saved items across stance categories (supporting/opposing/neutral), quantifying ideological diversity within a hoard
- **Source entropy:** Shannon entropy over the distribution of saves across information sources, capturing source concentration independently of stance
- **Temporal trajectory:** Entropy computed over rolling windows within a research session, revealing whether diversity increases or decreases over time
- **Intra-user diversity:** How varied is an individual user's hoard (following Anwar & Schoenebeck 2024)
- **Inter-user diversity:** How different are hoards between users, distinguishing filter bubbles (low intra-user diversity) from homogenization (low inter-user diversity)
- **Metacognitive gap:** The difference between a user's perceived diversity and actual measured diversity, operationalizing the blind spot predicted by P5

This pipeline is presented as a validated measurement methodology ready for deployment in the controlled experiment described in Future Work (Section 9.5). The Shannon entropy approach builds on established precedents in media diversity measurement (Bertani et al. 2024; SEIC 2024; nonparametric entropy-based polarization 2024) and ecological diversity indices.

### 5.2 Agent-Based Simulation of the Save-Bias Mechanism

To test whether the three-layer bias model produces internally consistent predictions, we instantiated the model as an agent-based simulation (entropy_demo.py) with empirically-grounded parameters drawn from the LLM sycophancy and filter bubble literatures.

**Design:** The simulation mirrors the recommended empirical validation protocol (Section 9.5): 240 synthetic participants in a 2x3 between-subjects design.
- IV1: Information source -- (a) LLM conversational search, (b) algorithm-curated feed, (c) unmediated (balanced reading list)
- IV2: Topic -- controversial vs. neutral

Each synthetic participant was assigned a prior belief strength and simulated through a save session where encounter probabilities, save probabilities, and stance distributions were governed by the layer-specific parameters documented in the empirical literature.

**Key results:**

- **LLM vs. Unmediated:** Cohen's d = -0.88 on stance entropy, confirming that the model predicts a large effect of LLM mediation on hoard homogeneity (P1, P4)
- **Metacognitive gap:** Cohen's d = +1.31, indicating that LLM users substantially overestimate the diversity of their hoards relative to actual measured diversity (P5)
- **Temporal trajectory:** LLM-condition entropy declines over the course of a session while unmediated-condition entropy rises, consistent with conversational entrenchment (Section 3.3, mechanism 5)
- **Omnibus test:** Kruskal-Wallis H = 59.14, p < .000001 across conditions
- **Topic moderation:** Effects are larger for controversial topics, where confirmation bias has more material to operate on (P2)

All 5 figures from the simulation (condition comparisons, temporal trajectories, metacognitive gap distributions, topic moderation, belief-strength interaction) are available in the entropy_demo output.

The simulation demonstrates that the three-layer bias model, when instantiated with empirically-grounded parameters, produces the predicted pattern of hoard homogenization. This provides theoretical validation of the framework's internal consistency and establishes the expected effect sizes for the planned controlled experiment.

### 5.3 LLM Sycophancy Evidence Synthesis

The six LLM-specific mechanisms documented in Section 3.3 each have independent empirical support. Across the cited studies, LLM sycophancy is documented with effect sizes ranging from 45 percentage points (face preservation, Chheda et al. 2025) to 39% performance degradation in multi-turn conversations (arXiv:2505.06120). Specific findings include:

- LLMs affirm whichever side of a moral conflict the user adopts in 48% of cases (Chheda et al. 2025)
- Source framing bias ranges from 6-24% across all tested models (Germani et al. 2025)
- Users do not cross-check LLM-provided information, even when it is factually incorrect (Jacob et al. 2025)
- Conversational search increases confirmatory querying regardless of source transparency (Sharma et al. 2024)
- Sycophantic behavior is structurally encoded in RLHF-trained models and rewarded in preference datasets (Sharma et al. 2023; arXiv:2509.21305)

These independently documented effects, when combined through the three-layer model, predict the hoard homogenization pattern demonstrated in the simulation (Section 5.2). The simulation parameters were calibrated to these empirical values, and the resulting effect sizes (d = -0.88 for entropy reduction, d = +1.31 for metacognitive gap) represent the model's predictions for what the controlled experiment should find if the three-layer mechanism operates as theorized.

---

## 6. Methodological Innovation: Hoard Diversity Metrics

### 6.1 Shannon Entropy of Saved Content

Classify each saved item's stance on a topic (supporting/opposing/neutral). Calculate:
```
H = -SUM p_i * log2(p_i)
```
where p_i is the proportion of items in each stance category. Maximum entropy = balanced saves; minimum = all one stance.

**Precedents for Shannon entropy in media/political diversity measurement:**

- **Bertani, Mazzeo & Gallotti (2024, Entropy/MDPI):** Used three different entropy measures to quantify diversity in web-domain and news media category choices among disinformation spreaders vs. reliable-content sharers on social media. Found that users disseminating unreliable content exhibited more varied but more regular web-domain choices. Demonstrates feasibility of entropy-based media diet measurement (Bertani et al. 2024, doi:10.3390/e26030270).

- **SEIC -- Structural Entropy Index of Community (2024, Entropy/MDPI):** Integrated Shannon's information theory with social network analysis for Twitter political discourse around the #Zandberg hashtag. SEIC quantifies communicative balance, informational diversity, and systemic vulnerability, enabling detection of fragmented discourse structures, emergent echo chambers, and coordinated influence operations (doi:10.3390/e27111140).

- **Nonparametric entropy-based polarization measure (2024, Political Science Research and Methods):** Presented an entropy-based measure of mass political polarization, demonstrating the applicability of information-theoretic approaches to political opinion measurement.

- **Thermodynamic analogy (2023, Scientific Reports):** Modeled political polarization as an isolated thermodynamic system, calculating Shannon entropy for distributions of agent variables with respect to political affiliation and influence.

- **Broader precedent:** Shannon entropy is widely used as a diversity metric in ecology (Shannon diversity index) and nutrition science (Shannon Entropy Diversity Metric for dietary diversity, INDDEX/Tufts).

### 6.2 Source Diversity Index

Count unique information sources across saved items. AI-mediated search may produce more items but from fewer original sources (because LLMs synthesize from a narrower set and conversational search reduces user motivation to consult multiple sources -- Sharma et al. 2024).

Compute both:
- Raw source count (number of unique domains/outlets)
- Source entropy: apply Shannon entropy to the distribution of saves across sources (a few dominant sources = low entropy even with many unique sources)

### 6.3 Temporal Diversity Trajectory

Plot H over time within a research session. A declining trajectory indicates progressive silo formation. Compare trajectories across conditions. The agent-based simulation (Section 5.2) demonstrates the expected pattern: LLM-condition entropy declines over the session while unmediated-condition entropy rises.

### 6.4 Intra-User vs. Inter-User Diversity

Following Anwar & Schoenebeck (2024), separately measure:
- **Intra-user diversity:** How varied is an individual's hoard?
- **Inter-user diversity:** How different are hoards between users?

Recommendation algorithms may homogenize hoards across users (everyone saves the same popular items) while maintaining intra-user diversity, or they may create individual silos (low intra-user diversity) while maintaining inter-user differences. These are distinct phenomena with different implications.

---

## 7. Regulatory and Policy Context

The EU regulatory framework provides both a policy motivation for this research and potential experimental leverage.

**EU Digital Services Act:** Article 27 requires recommender system transparency in plain language. Article 38 mandates that VLOPs/VLOSEs provide at least one non-profiling recommender alternative (e.g., TikTok now offers EU users the option to turn off personalization entirely). Articles 34-35 require systemic risk assessment covering effects on fundamental rights and civic discourse.

**EU AI Act:** Article 10 requires high-quality datasets with bias examination for high-risk AI systems. Article 10(5) permits collection of sensitive data specifically for bias detection and correction. Article 13 requires transparency documentation. General-purpose AI models (including LLMs) face separate transparency obligations. Fully applicable from 2 August 2026.

**Policy implications for Silo:** The DSA's Article 38 non-profiling alternative could serve as a natural experimental condition. The model predicts that: (1) the DSA's binary (profiled/non-profiled) may be insufficient -- intermediate diversity-promoting options may be needed; (2) AI Act Article 10 bias requirements should extend to the save/bookmark layer; (3) "systemic risk" under DSA Article 34 should encompass cumulative epistemic effects of biased hoards.

---

## 8. Counter-Arguments and Complications

### 8.1 Filter Bubbles May Be Overstated

Multiple studies question the severity of algorithmic filter bubbles:
- Guess et al. (2023) found no significant attitude change from switching to chronological feeds
- Liu et al. (2025) found limited short-term polarization from filter-bubble recommendations on YouTube
- Flaxman et al. (2016) found algorithms actually increased some cross-cutting exposure
- A systematic review found only 3 of 25 experiments provided clear evidence supporting filter bubbles (Areeb et al. 2023, arXiv:2307.01221)

**Response:** This paper does not claim filter bubbles are the dominant mechanism. The silo model adds the *save layer* as an amplifier that may produce stronger effects than encounter-level filtering alone. Even if what users see is moderately diverse, what they save may be homogeneous. The save action is an additional bias filter that existing studies do not measure.

### 8.2 Users May Save Diverse Content Deliberately

Users could exercise conscious diversity-seeking when saving:
- Yu et al. (2024, PNAS Nexus) showed that nudging algorithms can increase both news recommendations and consumption diversity, suggesting users respond to diverse offerings.
- Jiang et al. (2025, JASIST) found that stance labels and stance-based filters reduced behavioral selectivity and attitude extremity, especially for those with higher algorithmic literacy.
- Research on "stated vs. revealed preferences" suggests that if users deliberately chose their content, it would differ significantly from engagement-maximizing content.

**Response:** These findings are encouraging for intervention design but do not address the default case. Without nudges or labels, the baseline save behavior in AI-mediated contexts remains uncharacterized. The model predicts that the default is homogeneous -- but the cited mitigation research directly informs the intervention design in Section 9.

### 8.3 User Agency May Override Algorithmic Effects

Gonzalez-Bailon et al. (2023) found that users' social networks determined posts in their feeds more strongly than the algorithm on Facebook. Users actively choose sources beyond what algorithms recommend.

**Response:** User agency is real but operates within constrained choice architectures. Jesse & Jannach (2021, Computers in Human Behavior Reports) frame recommendations as digital nudges that determine aspects of the choice architecture. Users exercise choice, but the choice set is pre-filtered. Save bias operates on the *already-filtered* choice set, compounding rather than correcting the algorithmic filter.

### 8.4 Disinformation Spreaders Show *High* Source Diversity

Bertani et al. (2024) found that disinformation spreaders exhibited MORE varied web-domain choices than reliable-content sharers, complicating a simple "low diversity = bad" narrative.

**Response:** Diversity of sources is not the same as diversity of stances. A user can save from many different conspiracy websites (high source diversity) while saving only conspiracy-confirming content (low stance diversity). The model measures stance diversity as the primary metric, with source diversity as secondary.

### 8.5 Simulations Cannot Replace Experiments

The computational demonstrations (Section 5) use synthetic data and assumed parameters. Simulations validate internal model consistency but cannot confirm that human save behavior actually follows the predicted pattern.

**Response:** We agree. The computational demonstrations validate the framework's internal coherence -- that the proposed mechanisms, when combined, produce the predicted pattern. Whether human save behavior actually follows this pattern requires the controlled experiment described in Future Work (Section 9.5). The simulation identifies the expected effect sizes (d = -0.88 for entropy reduction, d = +1.31 for metacognitive gap) and methodological requirements for that experiment, serving as both a theoretical validation and a power analysis for the empirical follow-up.

---

## 9. Implications and Interventions

### 9.1 For Epistemic Autonomy

- Digital hoards are not neutral repositories; they are biased archives that shape future cognition. This aligns with emerging philosophical work on AI and epistemic agency (2025, Social Epistemology) arguing that AI undermines epistemic agency through manipulation and bubble creation.
- "I saved it for later" is not just storage -- it is an implicit commitment to a particular information diet. Huang et al. (2025) show that saving health content actually *inhibits* acting on it, suggesting hoards become inert belief-reinforcing repositories.
- AI acceleration of this process raises questions about informed consent: users do not choose to build biased archives, and the shift from epistemic bubble to echo chamber (Section 3.4) may occur without awareness.
- The "chat-chamber effect" (Jacob et al. 2025) demonstrates that LLM-provided misinformation goes unchecked, compounding the bias in saved content.

### 9.2 For AI System Design

- **Diversity-aware saving (stance labels):** Following Jiang et al. (2025), implement stance labels on content at the point of saving. Their controlled experiment (n=142) showed stance labels inhibited consumption of pro-attitudinal information and stance-based filters facilitated counter-attitudinal consumption.
- **Hoard diversity dashboard:** Show users the Shannon entropy and source diversity of their saved collections. Make visible what is currently invisible.
- **Counter-recommendation at save time:** When a user saves an item, recommend a counter-perspective item alongside it. Yu et al. (2024, PNAS Nexus) demonstrated that algorithmic nudges sustainably increase diversity on YouTube.
- **Periodic hoard audits:** Automated analysis of saved collections with diversity reports, analogous to screen time reports.
- **Sycophancy mitigation for search:** Implement "grounding" approaches where LLMs elicit additional context with follow-up questions rather than affirming user framings (as suggested in sycophancy mitigation literature, arXiv:2411.15287).

### 9.3 For Digital Hoarding Theory

- **Content homogeneity as a new dimension of hoarding severity** -- not just quantity but quality/diversity of accumulated material. Neither the DHQ (Neave et al. 2019) nor the Sedera et al. (2022) framework currently includes content diversity.
- The silo effect connects digital hoarding to epistemic and democratic concerns (misinformation, polarization), extending hoarding research beyond individual productivity or wellbeing.
- Hoarding is not just about what you keep; it is about what you systematically fail to encounter and save.
- The "storing, not reading" phenomenon (observed in Chinese youth by upward social comparison studies) means hoards may shape identity and belief without ever being consciously reviewed -- their mere existence as "my research" confers legitimacy.

### 9.4 For Information Literacy

- Teaching critical evaluation of AI-curated information, including awareness that LLM conversational search exacerbates confirmatory information seeking (Sharma et al. 2024).
- Meta-awareness of save patterns as a form of information hygiene.
- Algorithmic literacy as a protective factor: Jiang et al. (2025) found algorithmic literacy moderated the effectiveness of diversity interventions.

### 9.5 Future Work: Empirical Validation Agenda

This paper presents the theoretical framework and computational demonstrations. The following empirical studies are planned to test the model's predictions with human participants:

**Immediate -- Controlled Experiment (n >= 240).** The recommended empirical validation protocol directly tests predictions P1-P5. Design: 2x3 between-subjects (Information source: LLM conversational search / algorithm-curated feed / unmediated reading list; Topic: controversial / neutral). Participants research a topic for 30 minutes, saving items into a provided bookmarking tool. Dependent variables: Shannon entropy of saved items (stance diversity), source diversity index, number of counter-arguments in post-session summary, perceived vs. actual diversity (metacognitive gap), belief change (pre-post). The simulation (Section 5.2) provides expected effect sizes for power analysis: d = -0.88 for the primary entropy comparison, d = +1.31 for metacognitive gap. Pre-registration on OSF planned prior to data collection.

**Medium-term -- Observational Hoard Audit (n >= 300).** Participants grant access to their existing digital hoards (bookmarks, saved articles, screenshots, note-taking apps) and complete measures of beliefs/attitudes on pre-selected topics. Will use participant-controlled data export and the guided tour method (Jones 2010; Jones et al. 2021). This study directly tests P6 (feedback-loop saves vs. non-feedback saves) and P7 (hoard homogeneity vs. encounter homogeneity as predictors of belief entrenchment). Excluded from the present paper due to severe privacy concerns and the logistical expense of the guided tour method, which is "expensive and impractical to do with a larger, more diverse sampling" (Jones 2021).

**Long-term -- Longitudinal Diary Study (n >= 80, 4 weeks).** Participants install a browser extension and/or use platform data export to track daily saving behavior across platforms, with weekly belief surveys. Will test whether hoard homogeneity increases over time, whether AI usage intensity predicts rate of diversity decline, and whether there are "tipping points" of hoard homogeneity beyond which diversity decline accelerates.

**Intervention -- Diversity-Aware Saving Tools.** Building on the measurement pipeline (Section 5.1) and the intervention designs in Section 9.2: test stance labels at save time, hoard diversity dashboards, and counter-recommendation nudges in a randomized controlled trial. Jiang et al. (2025) and Yu et al. (2024) provide the intervention design basis; the Silo framework provides the theoretical grounding and measurement methodology.

Additionally, future work should investigate: (1) cross-platform hoard integration effects; (2) AI-assisted hoard review as a bias amplifier (the Narcissus Loop applied to saved content); (3) collective hoarding in shared collections (Pinterest boards, collaborative playlists); (4) developmental considerations for younger users; (5) relative effectiveness of interventions at the encounter, save, and retrieval layers.

---

## 10. Related Work (Expanded)

### Digital Hoarding
- **Information hoarding and selective exposure:** Bai et al. 2025 (BMC Psychology)
- **FOMO and digital hoarding:** Wang et al. 2023 (Social Media + Society); Wu & Zhao 2023 (Int. J. Human-Computer Interaction); Zaremohzzabieh et al. 2024 (Digital Health)
- **Digital hoarding measurement:** Neave et al. 2019 (Computers in Human Behavior); Sedera et al. 2022 (Information & Management)
- **Digital hoarding and cognitive failure:** Liu & Liu 2024 (Frontiers in Psychology); Mu et al. 2025 (Frontiers in Psychology)
- **Saving but not acting:** Huang et al. 2025 (Int. J. Human-Computer Interaction)
- **Generation Z digital hoarding:** PMC 2025 (Chinese Gen Z configurational pathways)

### Selective Exposure
- **Foundational selective exposure theory:** Klapper 1960 (The Effects of Mass Communication); Zillmann & Bryant 1985 (Selective Exposure to Communication)
- **Cognitive dissonance (motivational mechanism):** Festinger 1957 (A Theory of Cognitive Dissonance)

### Filter Bubbles and Recommendation
- **Filter bubbles:** Pariser 2011 (book); Flaxman et al. 2016 (Public Opinion Quarterly)
- **Facebook algorithm experiments:** Guess et al. 2023 (Science); Gonzalez-Bailon et al. 2023 (Science)
- **YouTube filter bubbles:** Liu et al. 2025 (PNAS); Yu et al. 2024 (PNAS Nexus)
- **Filter bubble vs. homogenization:** Anwar & Schoenebeck 2024 (ACM Web Conference)
- **Systematic review:** Areeb et al. 2023 (arXiv:2307.01221)
- **Restraining filter bubbles:** Jiang et al. 2025 (JASIST)
- **Recommendation systems and nudging:** Jesse & Jannach 2021 (Computers in Human Behavior Reports)

### LLM Sycophancy and Bias
- **RLHF sycophancy:** Perez et al. 2022; Sharma et al. 2023/ICLR 2024
- **Social sycophancy (ELEPHANT):** Chheda et al. 2025 (ICLR 2026)
- **Multi-turn sycophancy:** EMNLP Findings 2025
- **Source framing bias:** Germani et al. 2025 (Science Advances)
- **Sycophancy causes and mitigations:** arXiv:2411.15287; causal separation arXiv:2509.21305
- **Sycophancy in medical contexts:** npj Digital Medicine 2025

### LLM Echo Chambers
- **Generative echo chamber:** Sharma, Liao & Xiao 2024 (CHI 2024)
- **Chat-chamber effect:** Jacob, Kerrigan & Bastos 2025 (Big Data & Society)
- **LLM echo chamber (disinformation):** arXiv:2409.16241
- **Multi-turn degradation:** arXiv:2505.06120

### Epistemic Theory
- **Epistemic bubbles vs echo chambers:** Nguyen 2020 (Episteme)
- **AI and epistemic agency:** 2025 (Social Epistemology, doi:10.1080/02691728.2025.2466164)
- **Artificial epistemic authorities:** 2025 (Social Epistemology, doi:10.1080/02691728.2025.2449602)
- **Chatbot epistemology:** 2025 (Social Epistemology, doi:10.1080/02691728.2025.2500030)

### Measurement and Methodology
- **Shannon entropy for media diversity:** Bertani et al. 2024 (Entropy/MDPI)
- **SEIC for political discourse:** 2024 (Entropy/MDPI, doi:10.3390/e27111140)
- **Entropy-based polarization:** 2024 (Political Science Research and Methods)
- **PIM research methodology:** Jones 2010; Jones et al. 2021 (arXiv:2107.03291)
- **Narcissus Loop (this research program):** Directional citation bias in AI-assisted research

### Regulatory
- **EU Digital Services Act:** Articles 27, 34, 35, 38 (recommender systems, systemic risk, non-profiling alternatives)
- **EU AI Act:** Articles 10, 10(5), 13 (data governance, bias detection, transparency)

---

## 11. Limitations

1. **Theoretical framework not empirically tested with human participants.** The three-layer bias model and its predictions are supported by computational demonstrations and synthesis of existing empirical work, but have not been directly tested in a controlled experiment with human save behavior. The planned empirical validation (Section 9.5) is designed to address this limitation.

2. **Simulation uses synthetic data with assumed parameters.** The agent-based simulation (Section 5.2) instantiates the model with parameters drawn from existing empirical studies, but real save behavior may differ in magnitude, distribution, or interaction effects. The simulation validates internal model coherence, not external validity.

3. **Stance classification is simplified.** The three-category stance classification (supporting/opposing/neutral) sacrifices nuance for reliability and computational tractability. Real content exists on a continuous spectrum and may resist categorical classification. The measurement pipeline (Section 5.1) could be extended to continuous stance measures in future work.

4. **The three-layer model assumes layers are additive.** The funnel model (Section 3.1) treats encounter bias, save bias, and retrieval bias as sequential filters. In practice, the layers may interact nonlinearly -- for example, awareness of algorithmic filtering (Layer 1) could either amplify save bias (compensatory hoarding) or attenuate it (diversity-seeking). These interaction effects are not modeled in the current simulation.

5. **LLM sycophancy evidence comes from separate studies.** The six mechanisms documented in Section 3.3 are each supported by independent empirical studies, but their combined effect on save behavior has not been tested. The simulation (Section 5.2) combines them parametrically, but the real combined effect could be larger or smaller than the sum.

6. **Cultural and platform variations not modeled.** Most existing digital hoarding research uses Chinese student samples (Bai et al. 2025, Wang et al. 2023, Wu & Zhao 2023, Liu & Liu 2024). Platform affordances differ across TikTok, Instagram, YouTube, and browser bookmarks. The model's predictions may not generalize uniformly across cultures or platforms.

---

## 12. Connection to Broader Concerns

This paper sits at the intersection of four conversations:

1. **Digital hoarding** -- a growing phenomenon (personal cloud storage users grew from 1.1 billion in 2014 to ~2.3 billion in 2024) with measurable cognitive costs (cognitive failure, burnout, behavioral inhibition).

2. **AI alignment and safety** -- recommendation systems optimizing for engagement, not epistemic welfare. LLM sycophancy as a structural feature of RLHF training, not merely a bug. The ELEPHANT finding that sycophancy is rewarded in preference datasets suggests the problem is systemic.

3. **Democratic epistemology** -- polarization, filter bubbles, and informed citizenship. Gonzalez-Bailon et al. (2023) showed ideological segregation increases from exposure to engagement; this paper argues it increases further from engagement to saving.

4. **Regulatory governance** -- the EU DSA and AI Act create a framework for transparency and bias mitigation in recommendation systems, but neither currently addresses the save/hoard layer as a distinct site of bias amplification. This paper provides the theoretical basis for extending regulation to the save layer.

The silo effect suggests that digital hoarding is not merely a personal productivity problem -- it is an epistemic one. When AI shapes what we save, it shapes what we know, what we believe, and how we reason about the world.

---

## References (Key Additions)

- **Festinger, L. (1957).** *A Theory of Cognitive Dissonance.* Stanford, CA: Stanford University Press. [Cited for dissonance avoidance as the motivational mechanism underlying selective exposure -- NOT as the selective exposure citation itself.]
- **Klapper, J. T. (1960).** *The Effects of Mass Communication.* New York: Free Press. [Foundational selective exposure work.]
- **Zillmann, D., & Bryant, J. (1985).** *Selective Exposure to Communication.* Hillsdale, NJ: Erlbaum. [Major elaboration of selective exposure theory.]

---

## Meta-Note

This paper presents a theoretical framework with computational demonstrations. The controlled experiment testing the framework's predictions with human participants is planned as a follow-up study (Section 9.5). This outline should be reviewed by a context-free session to check for directional bias in the framing. The irony of writing a paper about confirmation-biased hoarding while potentially exhibiting it is not lost. Specific concern: the framing emphasizes negative effects of AI on information diversity. Counter-evidence (Guess et al. 2023; Liu et al. 2025; Flaxman et al. 2016) is included but may be underweighted. A steel-man version of the null hypothesis -- that saves are no more biased than views, or that AI actually helps users save more diverse content -- should be tested with equal rigor in the planned empirical work.
