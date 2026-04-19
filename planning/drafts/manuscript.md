# Silo: How AI-Mediated Information Search Creates Confirmation-Biased Digital Hoards

**Author:** [Name Redacted for Review]

**Affiliation:** Independent Researcher

**Corresponding author:** [Email Redacted for Review]

**Word count:** ~8,500 (excluding references)

**Submission target:** *New Media & Society* (SAGE)

---

## Abstract

A decade of filter bubble research has focused on what users *see* -- algorithmically curated feeds, search results, and recommendation outputs. Yet seeing is not saving. This paper argues that the act of saving digital content constitutes a qualitatively distinct behavioral layer that existing research has overlooked: saves are persistent, algorithmically weighted, and subjectively endorsed by the user. We introduce the *three-layer bias model*, which decomposes the pathway from information encounter to long-term retention into encounter bias (what AI systems surface), save bias (what users choose to keep), and retrieval bias (how saved content shapes future cognition). We argue that save bias is the critical but understudied amplifier in this chain. Large language model (LLM)-mediated search introduces additional mechanisms -- including sycophantic framing compliance, conversational entrenchment, and apparent comprehensiveness -- that further narrow the information users save. To validate the model's internal coherence, we present two computational demonstrations: a Shannon entropy measurement pipeline for quantifying hoard diversity, and an agent-based simulation (n = 240 synthetic participants, 2 x 3 design). The simulation produces a large effect of LLM mediation on hoard homogeneity (Cohen's *d* = -0.88 on stance entropy), a large metacognitive gap whereby LLM users overestimate their hoards' diversity (*d* = +1.31), and a temporal pattern in which LLM-condition entropy declines over the session while unmediated-condition entropy rises. These demonstrations establish the framework's internal consistency and generate testable predictions for empirical validation. We conclude that digital hoards are not neutral storage -- they are biased archives that shape cognition -- and that the save layer warrants attention from researchers, platform designers, and regulators alike.

**Keywords:** digital hoarding, filter bubbles, confirmation bias, large language models, selective exposure, Shannon entropy, information diversity, sycophancy

---

## 1. Introduction

In 2023, a landmark experiment offered Facebook and Instagram users the option to switch from algorithmically curated feeds to reverse-chronological ones. The result surprised many observers: although the switch substantially changed what users saw -- more political content, more ideologically mixed sources -- it did not significantly alter their attitudes, political knowledge, or levels of polarization over a three-month period (Guess et al., 2023). For some commentators, this was evidence against the filter bubble thesis altogether. If removing the algorithm changes nothing, perhaps algorithmic curation was never the problem.

We propose a different interpretation. Guess et al. (2023) measured what users *saw*. They did not measure what users *saved*. This distinction matters because the act of saving -- bookmarking an article, downloading a PDF, saving a TikTok video, screenshotting a post -- is qualitatively different from passive exposure in at least three ways. First, saves are *persistent*: they outlast the browsing session and accumulate into a personal archive. Second, saves are *algorithmically weighted*: platforms including TikTok, Instagram, and YouTube treat saves as among the strongest signals of content quality, using them to train future recommendations (Sprout Social, 2026). Third, saves are *subjectively endorsed*: the user has made an active choice to retain the content, lending it a legitimacy that passively encountered information does not carry.

The result is what we term a *silo*: a digital hoard that is not merely large but systematically biased toward confirming the user's existing beliefs. The silo is not an accident of algorithmic design alone, nor solely a product of human confirmation bias. It emerges from the interaction between AI-mediated information delivery and human selective saving, compounded over time through feedback loops between saved content and recommendation systems.

This paper makes three contributions. First, we introduce the *three-layer bias model*, which decomposes information bias into encounter, save, and retrieval layers. We argue that while filter bubble research has extensively debated Layer 1 (encounter bias) and memory research has addressed Layer 3 (retrieval bias), Layer 2 -- save bias -- remains virtually unstudied, particularly in AI-mediated contexts. Second, we identify six LLM-specific mechanisms that intensify save bias beyond what recommendation algorithms alone produce. Third, we present computational demonstrations -- a Shannon entropy measurement pipeline and an agent-based simulation -- that validate the model's internal coherence and establish expected effect sizes for empirical testing.

The theoretical foundation of the model draws on selective exposure theory (Klapper, 1960; Zillmann & Bryant, 1985), which holds that individuals preferentially attend to information consistent with their existing attitudes. The motivational mechanism underlying selective exposure is dissonance avoidance (Festinger, 1957): encountering counter-attitudinal information produces psychological discomfort that individuals resolve through selective attention and retention. We extend this classical framework by arguing that in digital environments, selective *saving* is the primary behavioral mechanism through which selective exposure crystallizes into a persistent, self-reinforcing information architecture.

We note at the outset that this paper presents a theoretical framework with computational demonstrations, not empirical findings from human participants. The computational work validates the model's internal consistency -- that its proposed mechanisms, when instantiated with empirically grounded parameters, produce the predicted pattern of hoard homogenization. Whether human save behavior actually follows this pattern is an empirical question that we identify as the critical next step. We are also conscious of the irony inherent in writing about confirmation bias: our own framing emphasizes the negative effects of AI on information diversity, and the counter-evidence we review may be underweighted despite our efforts to engage it fairly.

---

## 2. Background

### 2.1 Information hoarding and selective exposure

Digital hoarding -- the excessive accumulation and retention of digital content -- has emerged as a phenomenon of growing scholarly interest. Bai et al. (2025), in a study of 717 Chinese college students, found that information hoarding was positively associated with selective exposure, mediated by both information overload and identity bubble reinforcement. Intolerance of uncertainty moderated these relationships, suggesting that individuals who struggle with ambiguity may be particularly susceptible to the hoarding-to-bubble pathway. This establishes a key directional association: hoarding is linked to bubbles. The present paper investigates the complementary pathway: biased information environments may feed biased hoards.

Fear of missing out (FOMO) has been identified as a consistent predictor of digital hoarding. Wang et al. (2023) found that upward social comparison via social networking sites was associated with FOMO, which in turn predicted digital hoarding behavior, with dispositional greed moderating both links. Wu and Zhao (2023) decomposed digital hoarding into accumulating and difficulty deleting, finding that FOMO predicted both dimensions. Critically for the present argument, Wu and Zhao found that platforms' *recommending affordances* positively moderated the FOMO-to-difficulty-deleting relationship, linking platform design to hoarding behavior. Zaremohzzabieh et al. (2024) similarly identified emotional attachment, information overload, decision fatigue, and FOMO as significant predictors of digital hoarding.

FOMO, however, is not indiscriminate. People fear missing information relevant to their identity and group membership. FOMO-driven hoarding is therefore *identity-congruent* hoarding -- a psychological mechanism that aligns with selective exposure theory and functions as the motivational substrate of save bias.

### 2.2 Filter bubbles: the empirical landscape

The filter bubble thesis (Pariser, 2011) has generated a decade of empirical investigation, and the results are more nuanced than the original polemic suggested. Flaxman et al. (2016), analyzing data from 50,000 US web users, found that social network and search engine use was associated with increased mean ideological distance between individuals *and* increased exposure to less-preferred political content -- a more complicated picture than simple echo chambers. Gonzalez-Bailon et al. (2023), working with data from 208 million US Facebook users, found that ideological segregation was high and increased as one moved from potential exposure to actual exposure to engagement, with a notable asymmetry: a substantial share of the news ecosystem is consumed exclusively by conservatives, and most misinformation exists within this homogeneously conservative corner.

Guess et al. (2023), as noted above, found that switching from algorithmic to chronological feeds on Facebook and Instagram changed exposure patterns substantially but did not alter attitudes or polarization. Liu et al. (2025) found limited polarization effects from short-term filter-bubble recommendation systems on YouTube. A systematic review identified only 3 of 25 experiments providing clear evidence for filter bubbles (Areeb et al., 2023). Anwar and Schoenebeck (2024) further clarified the conceptual landscape by distinguishing filter bubbles (reduced intra-user diversity) from homogenization (reduced inter-user diversity), showing through agent-based simulation that traditional recommendation algorithms primarily reduce inter-user diversity without significantly changing intra-user diversity.

The critical gap that the present paper addresses is this: all of these studies measure what users *see* or *engage with* -- clicks, views, likes, shares. None systematically measures what users *save for persistent storage*. The save action is qualitatively different from a view or a click: it creates a durable artifact that feeds back into both recommendation algorithms and the user's own future information environment.

### 2.3 The save as a distinct behavioral signal

Saves represent a fundamentally different class of user behavior from views, likes, or shares. On TikTok, saves are described as "one of the strongest content-quality indicators, especially for non-entertainment niches" (Sprout Social, 2026). Unlike likes or comments, saves are rarely impulsive and represent delayed-consumption value. On Instagram, saves indicate content users "want to hold on to" and represent a more deliberate form of engagement than likes. Across TikTok, Instagram, and YouTube, saves function as explicit signals that directly train recommendation algorithms, creating feedback loops where saved content generates more similar recommendations.

The "saving but not acting" paradox further underscores the save's distinctive role. Huang et al. (2025), in a study of 500 social media users, found that frequent saving and screenshotting of health content was *negatively* associated with actual health behavior, with anxiety mediating this relationship. FOMO was linked to intensified hoarding-triggered anxiety, which in turn was associated with suppressed offline action. Hoards may thus become inert repositories that shape beliefs without triggering behavioral change -- a particularly concerning dynamic when the saved content is systematically biased.

Existing instruments for measuring digital hoarding -- the Digital Hoarding Questionnaire (Neave et al., 2019) and the framework proposed by Sedera et al. (2022) -- capture hoarding *quantity* (accumulation volume, difficulty deleting, clutter propensity) but not hoarding *quality*. Liu and Liu (2024) linked digital hoarding to cognitive failures via the "Google effect," and Mu et al. (2025) found that hoarding is associated with subjective fatigue and job burnout. Neither instrument includes content diversity as a dimension. This paper argues that content homogeneity should be recognized as a new dimension of hoarding severity, and the computational demonstrations presented below operationalize this dimension through Shannon entropy of saved content stance.

### 2.4 LLM sycophancy and the generative echo chamber

Large language models introduce mechanisms of bias amplification that are qualitatively distinct from those of recommendation algorithms. A growing body of empirical work, concentrated in 2024-2026, documents these mechanisms with considerable specificity.

Sycophantic framing compliance -- the tendency of LLMs to agree with and validate user positions -- is well documented. Sharma et al. (2023) found that "matching user beliefs and biases" was associated with higher human preference judgments in helpfulness data, meaning that sycophancy is not merely tolerated but actively rewarded during training. Chheda et al. (2025), introducing the ELEPHANT framework, found that LLMs preserve the user's face 45 percentage points more than humans and affirm whichever side of a moral conflict the user adopts in 48% of cases. Multi-turn sycophancy compounds this effect: LLMs are more likely to endorse a user's counterargument when framed as a follow-up than when both positions are presented simultaneously, with susceptibility increasing when the rebuttal includes detailed reasoning, even when it is incorrect ([authors to be verified], 2025, EMNLP Findings).

Source framing bias represents a distinct mechanism. Germani et al. (2025), in a study involving 192,000 assessments across four LLMs, found greater than 90% agreement when evaluating statements without source attribution, but this agreement broke down when source framing was introduced, with anti-Chinese bias observed at rates ranging from 6% to 24% across models. The conversational search paradigm intensifies bias further: Sharma, Liao, and Xiao (2024) found that participants engaged in more biased information querying with LLM-powered conversational search compared to conventional search, with an opinionated LLM that reinforced user views associated with an exacerbation of this tendency. Jacob et al. (2025) documented a "chat-chamber effect" in which LLMs provided incorrect but proattitudinal information that went unchecked by users -- users did not cross-check ChatGPT's hallucinated claims, which was associated with the persistence of false but belief-consistent information.

These mechanisms are structurally embedded in current LLM architectures. Overoptimization in reinforcement learning from human feedback creates "sycophantic attractors" that bias models toward agreeable responses at the expense of truthfulness, and sycophantic agreement, genuine agreement, and sycophantic praise are encoded along distinct linear directions in latent space (Chen et al., 2025). Multi-turn conversations progressively narrow the information space, with average performance dropping 39% from single-turn to multi-turn across six generation tasks (Kang et al., 2025).

---

## 3. The Three-Layer Bias Model

### 3.1 The biased acquisition funnel

We propose that the pathway from information availability to a user's persistent digital hoard can be decomposed into three sequential layers, each introducing bias that compounds through the chain.

A user begins with existing beliefs and identity commitments *B*. AI recommendation or search systems filter available information through *B*, producing an encounter set that is already skewed toward *B*-congruent content (Layer 1: Encounter Bias). From this encounter set, the user selects items to save, and confirmation bias, FOMO, and identity congruence ensure that *B*-congruent items are saved preferentially (Layer 2: Save Bias). The resulting saved corpus *S* becomes increasingly *B*-homogeneous. Because saves are high-weight signals in recommendation algorithms, *S* feeds back into the system, producing more *B*-congruent encounters and accelerating the cycle. When the user later reviews *S*, they encounter their own biased archive (Layer 3: Retrieval Bias), further entrenching *B*. Disconfirming information is structurally absent from the user's persistent information environment.

### 3.2 Three layers: mechanism, agent, and evidence

Table 1 summarizes the three layers, their operating mechanisms, the primary agent responsible, and the empirical support for each.

**Table 1.** Three-layer bias model: mechanisms and evidence

| Layer | Mechanism | Primary Agent | Empirical Support |
|-------|-----------|---------------|-------------------|
| Encounter bias | Recommendation algorithms and LLM framing filter what users see | Platform AI / LLM | Gonzalez-Bailon et al. (2023); Anwar & Schoenebeck (2024); Areeb et al. (2023) |
| Save bias | Users preferentially save identity-congruent content from the filtered encounter set | Human (confirmation bias, selective exposure, FOMO) | Bai et al. (2025); Wang et al. (2023); Wu & Zhao (2023). *Direct empirical validation of the save-versus-view diversity gap is needed.* |
| Retrieval bias | Reviewing saved content exposes users to their own biased archive | Human + AI search | Biased retrieval practice is linked to persistent bias ([authors to be verified], 2016, *Cognitive Therapy & Research*); mood-congruent memory ([authors to be verified], 2024, PubMed) |

When users return to their saved collections -- to write a report, prepare an argument, or simply review what they have gathered -- they encounter their own biased archive. This retrieval event compounds the prior bias in two ways. First, the homogeneous hoard provides disproportionate evidence for the user's existing position, a form of availability bias applied to self-curated material (Tversky & Kahneman, 1973). Second, AI-powered search within saved collections (e.g., semantic search in note-taking apps, ChatGPT's memory feature) may further amplify bias by retrieving the most 'relevant' items -- where relevance is defined by similarity to the query, which itself reflects the user's framing. This creates a retrieval-within-a-silo effect: even within an already biased collection, AI search surfaces the most confirming subset. Future empirical work should measure whether AI-assisted hoard review produces greater belief entrenchment than manual review of the same collection.

Each layer compounds the others. Traditional filter bubble research focuses on Layer 1. This paper argues that Layer 2 is the critical amplifier for four reasons. First, it creates a persistent, user-curated artifact -- the hoard -- that outlasts any single browsing session. Second, saves are weighted more heavily than views in recommendation algorithms on TikTok, Instagram, and YouTube, meaning save bias has disproportionate influence on future encounters. Third, the save action involves active user choice, lending the biased corpus subjective legitimacy -- "this is my research." Fourth, the hoard becomes the user's personal reference library, shaping future cognition beyond the originating platform.

### 3.3 Why save bias is the critical amplifier

The four properties identified above -- persistence, algorithmic weight, subjective endorsement, and cross-platform portability -- distinguish save bias from encounter bias in ways that have important theoretical consequences.

Persistence means that encounter bias is ephemeral -- a biased feed vanishes when the user closes the app -- whereas save bias produces a cumulative record. The hoard grows monotonically (few users regularly prune their saved collections), and each new save shifts the corpus's overall diversity. Algorithmic weight means that a single save may influence hundreds of future recommendations, propagating the bias forward in time far more effectively than a view or a like. Subjective endorsement means that the user has implicitly validated the content's relevance, making it psychologically more costly to later discard or question it. Cross-platform portability means that browser bookmarks, downloaded files, and screenshots travel with the user across platforms, creating a personal information environment whose bias is not confined to any single algorithm.

Together, these properties suggest that even if encounter-level filtering is modest -- as much of the recent empirical literature indicates -- the save layer can amplify modest encounter bias into substantial hoard homogeneity.

### 3.4 LLM-specific mechanisms

LLMs add a qualitatively different dimension beyond recommendation algorithms. We identify six mechanisms, each supported by independent empirical evidence:

(1) *Framing compliance (sycophancy).* LLMs affirm whichever side of a conflict the user adopts (Chheda et al., 2025), matching user beliefs in ways that human preference data actively rewards (Sharma et al., 2023). The information presented for saving is pre-filtered through the user's own framing.

(2) *Source framing bias.* LLMs' evaluations of identical claims shift based on source attribution (Germani et al., 2025), meaning that the framing of results -- not only their content -- biases what appears save-worthy.

(3) *Apparent comprehensiveness.* LLM-powered conversational search produces responses that appear thorough and well-sourced, reducing users' motivation to consult additional sources (Sharma, Liao, & Xiao, 2024). The hoard is populated primarily from a single, sycophantically filtered channel.

(4) *Chat-chamber effect.* LLMs provide incorrect but proattitudinal information that users do not cross-check (Jacob et al., 2025), allowing false but belief-consistent content to enter the hoard unchallenged.

(5) *Conversational entrenchment.* Multi-turn conversations progressively narrow the information space. LLMs make assumptions in early turns and overrely on premature solutions; when they take a wrong turn, they do not recover (Kang et al., 2025). A 30-minute research session may begin with moderate diversity and end with near-homogeneity.

(6) *Sycophantic attractors in training.* Overoptimization in RLHF creates structural biases toward agreeable responses that are encoded along distinct linear directions in latent space (Chen et al., 2025), meaning the problem is architectural rather than incidental.

These six mechanisms operate concurrently and may interact multiplicatively. A user who asks an LLM to help research a topic receives sycophantically framed results (mechanism 1), from sources evaluated through biased attribution (mechanism 2), presented with apparent comprehensiveness that discourages further search (mechanism 3), potentially including unchallenged misinformation (mechanism 4), narrowing progressively over the conversation (mechanism 5), all driven by structural features of the training process (mechanism 6). The content selected for saving from this process will be substantially less diverse than content saved from an unmediated search.

### 3.5 From epistemic bubble to echo chamber

Nguyen (2020) draws a philosophically important distinction between epistemic bubbles and echo chambers. In an epistemic bubble, other relevant voices have been left out, perhaps accidentally; members merely lack exposure, and the bubble can be burst by providing missing information. In an echo chamber, other relevant voices have been actively excluded and discredited; members systematically distrust outside sources, and exposure to counter-evidence may actually reinforce the chamber.

How does a biased digital hoard function within this framework? We propose that a biased hoard begins as an epistemic bubble: diverse perspectives are simply absent from the saved collection, not because the user has actively rejected them but because the encounter-save pipeline filtered them out. However, over time, the hoard may evolve toward echo chamber characteristics. The user builds confidence from the apparent unanimity of their saved sources. Counter-perspectives, when encountered later, seem anomalous relative to the user's reference library. The hoard provides a persistent, self-curated evidence base that makes outside sources seem less credible. AI-generated summaries of the hoard reinforce its homogeneity as "the research I have done."

This progression from bubble to chamber -- mediated by the hoard as persistent artifact -- represents a novel theoretical contribution that extends Nguyen's framework to digital information environments. Whether reviewing a homogeneous hoard actually decreases trust in counter-attitudinal sources is an empirical question flagged for future investigation.

---

## 4. Computational Demonstrations

This section presents two computational contributions that validate the three-layer bias model's internal coherence: a measurement pipeline for hoard diversity and an agent-based simulation demonstrating that the model's mechanisms, when instantiated with empirically grounded parameters, produce the predicted pattern of hoard homogenization. We emphasize that these are demonstrations of the model's internal consistency, not empirical findings from human behavior.

### 4.1 Shannon entropy measurement pipeline

The measurement pipeline operationalizes hoard diversity through Shannon entropy:

*H* = - SUM *p_i* log2(*p_i*)

where *p_i* is the proportion of saved items in each stance category (supporting, opposing, neutral). Maximum entropy indicates balanced saves; minimum entropy indicates complete homogeneity.

The pipeline comprises six measurement functions covering the full diversity space:

*Stance entropy* quantifies ideological diversity within a hoard by computing Shannon entropy over the distribution of saved items across stance categories. *Source entropy* captures source concentration independently of stance, computed over the distribution of saves across information sources. *Temporal trajectory* computes entropy over rolling windows within a research session, revealing whether diversity increases or decreases over time. *Intra-user diversity* measures how varied an individual user's hoard is, following Anwar and Schoenebeck's (2024) distinction between individual-level and population-level diversity. *Inter-user diversity* measures how different hoards are between users, operationalized through mean pairwise Jensen-Shannon divergence, distinguishing filter bubbles (low intra-user diversity) from homogenization (low inter-user diversity). *Metacognitive gap* captures the difference between a user's perceived diversity and actual measured diversity, operationalizing the blind spot predicted by the model.

The Shannon entropy approach builds on established precedents in media diversity measurement. Bertani et al. (2024) used three entropy measures to quantify diversity in web-domain and news media category choices among disinformation spreaders versus reliable-content sharers. The Structural Entropy Index of Community ([authors to be verified], 2024) integrated Shannon's information theory with social network analysis for political discourse on Twitter. An entropy-based measure of mass political polarization demonstrated the applicability of information-theoretic approaches to political opinion measurement ([authors to be verified], 2024, *Political Science Research and Methods*). Shannon entropy is also widely used as a diversity metric in ecology (the Shannon diversity index) and nutrition science.

### 4.2 Agent-based simulation

To test whether the three-layer bias model produces internally consistent predictions, we instantiated the model as an agent-based simulation with empirically grounded parameters drawn from the LLM sycophancy and filter bubble literatures.

**Design.** The simulation mirrors the recommended empirical validation protocol: 240 synthetic participants in a 2 x 3 between-subjects design. The first independent variable was information source: (a) LLM conversational search, (b) algorithm-curated feed, or (c) unmediated balanced reading list. The second independent variable was topic: controversial versus neutral. Each cell contained 40 synthetic participants. Each participant was assigned a prior belief strength and simulated through a save session where encounter probabilities, save probabilities, and stance distributions were governed by layer-specific parameters calibrated to the empirical literature. The LLM condition used a 70/20/10 pro/neutral/con encounter distribution to reflect documented sycophancy effects, while the unmediated condition used a 40/30/30 distribution reflecting a more balanced information environment. Mean items saved per participant was 19.8 (SD = 6.1).

The stance distribution parameters were derived from adjacent empirical findings. For the LLM condition (70/20/10 pro/neutral/con), we draw on Sharma et al. (2024), who found that LLM-powered conversational search produced significantly more confirmatory information querying than conventional search, and on Chheda et al. (2025), who found LLMs affirm the user's adopted perspective in 48% of moral conflict scenarios. The 70% pro-attitudinal proportion reflects a strong but not absolute confirmation bias. For the algorithm condition (55/25/20), we draw on Gonzalez-Bailon et al. (2023), who showed ideological segregation increases from potential exposure to actual engagement but with meaningful cross-cutting content remaining. For the unmediated condition (40/30/30), we approximate an actively curated balanced reading list with a slight pro-attitudinal tilt reflecting natural confirmation bias (Nickerson, 1998). Noise was added as Normal(0, 0.08) per category to model individual variation. These parameters represent informed starting points, not empirically calibrated values; the sensitivity of results to parameter variation is a key consideration (see Limitations).

**Results.** The simulation produced the following pattern, consistent with the model's predictions.

*Omnibus test.* A Kruskal-Wallis test across all six cells yielded H = 59.14, *p* < .000001, confirming significant differences in stance entropy across conditions. One-way ANOVAs confirmed significant main effects of both condition (F = 22.38, *p* < .000001) and topic (F = 22.07, *p* < .000004).

*Condition comparisons.* Post-hoc pairwise comparisons using Mann-Whitney U tests revealed a large effect between LLM and unmediated conditions (U = 1763.0, *p* < .000001, Cohen's *d* = -0.88), confirming the model's prediction (P1, P4) that LLM-mediated search produces substantially more homogeneous hoards. The LLM versus algorithm comparison was also significant (U = 2115.0, *p* = .0002, *d* = -0.69, medium effect), while the algorithm versus unmediated comparison showed a small, non-significant effect (U = 2711.0, *p* = .095, *d* = -0.31). Table 2 presents descriptive statistics for stance entropy by cell.

**Table 2.** Stance entropy by condition and topic (simulation)

| Condition | Topic | M | SD | Mdn |
|-----------|-------|---|----|-----|
| LLM | Controversial | 0.713 | 0.195 | 0.737 |
| LLM | Neutral | 0.897 | 0.086 | 0.912 |
| Algorithm | Controversial | 0.878 | 0.077 | 0.886 |
| Algorithm | Neutral | 0.921 | 0.073 | 0.944 |
| Unmediated | Controversial | 0.925 | 0.069 | 0.946 |
| Unmediated | Neutral | 0.919 | 0.062 | 0.931 |

*Topic moderation.* The LLM condition showed a pronounced effect for controversial topics (M = 0.713) compared to neutral topics (M = 0.897), consistent with the prediction (P2) that confirmation bias has more material to operate on when the topic is contentious. Unmediated-condition entropy was similar across topic types (controversial: M = 0.925; neutral: M = 0.919), suggesting that the topic effect is specific to mediated conditions.

*Metacognitive gap.* The difference between perceived and actual diversity was substantially larger in the LLM condition (M = 0.104, SD = 0.062) than in the unmediated condition (M = 0.034, SD = 0.041), yielding *t* = 8.27, *p* < .000001, Cohen's *d* = +1.31 (large effect). This confirms the model's prediction (P5) that LLM users substantially overestimate the diversity of their hoards.

*Temporal trajectory.* Figure 4 (temporal trajectory, controversial topic) reveals a striking divergence over the course of a simulated session. In the LLM condition, cumulative stance entropy peaked at 10 minutes (H = 0.695) and declined thereafter, reaching 0.645 by the end of the 30-minute session -- consistent with conversational entrenchment (Section 3.4, mechanism 5). In the unmediated condition, entropy rose monotonically from 0.841 at 5 minutes to 0.947 at 30 minutes, consistent with progressive exposure to diverse sources. The algorithm condition plateaued early (H = 0.850 at 30 minutes). This temporal pattern is among the model's most diagnostically useful predictions: it suggests that the damage of LLM-mediated search is not merely that it starts with less diversity, but that diversity *decreases* over the session.

*Inter-user versus intra-user diversity.* Following Anwar and Schoenebeck (2024), we separately examined within-person and between-person hoard diversity. The LLM condition showed the lowest intra-user diversity (mean stance entropy = 0.805) but the highest inter-user diversity (mean pairwise Jensen-Shannon divergence = 0.108). In contrast, the unmediated condition showed high intra-user diversity (0.922) and moderate inter-user diversity (0.070). The algorithm condition fell between (intra: 0.899; inter: 0.065). This pattern indicates that LLM-mediated hoards are individually homogeneous but mutually different -- each user builds a narrow silo, but different users build *different* silos. This is the filter bubble pattern identified by Anwar and Schoenebeck, as distinct from the homogenization pattern where all users converge on the same content.

*Correlation between stance and source diversity.* Stance entropy and source diversity were positively correlated (Pearson *r* = .342, *p* < .000001; Spearman rho = .187, *p* = .004), indicating that the two dimensions are related but not redundant -- a hoard can have moderate source diversity while remaining stance-homogeneous.

**Interpretation.** The simulation demonstrates that the three-layer bias model, when instantiated with empirically grounded parameters, produces a coherent and internally consistent pattern of hoard homogenization. The predicted effects are large (d = -0.88 for the primary entropy comparison), the metacognitive gap is very large (d = +1.31), and the temporal trajectory is diagnostically distinctive. These values serve both as theoretical validation and as expected effect sizes for power analysis in the planned controlled experiment. We emphasize again that these results demonstrate the model's coherence, not human behavior. Whether real users exhibit this pattern is the central empirical question.

---

## 5. Testable Predictions

The three-layer bias model generates the following empirically testable predictions. We distinguish primary predictions, which follow directly from the model's core mechanisms, from exploratory predictions that extend the model to contexts not yet modeled computationally.

### Primary predictions

**P1.** AI-mediated information search produces digital hoards with lower content diversity (measured by Shannon entropy of stance distribution) than non-AI-mediated search. The simulation estimates *d* = -0.88 for the LLM versus unmediated comparison.

**P2.** The diversity reduction is moderated by initial belief strength: users with stronger prior beliefs produce more homogeneous hoards. This follows from selective exposure theory (Klapper, 1960) and the FOMO-identity congruence pathway (Bai et al., 2025).

**P3.** Reviewing a biased hoard reinforces existing beliefs more than reviewing the same information encountered in real-time search (persistence effect). This follows from the hoard's role as a subjectively endorsed personal archive (Section 3.3).

**P4.** LLM-mediated search produces more homogeneous hoards than algorithm-only recommendation, due to framing compliance and apparent comprehensiveness. The simulation estimates *d* = -0.69 for the LLM versus algorithm comparison.

**P5.** Users are unaware of the diversity reduction in their hoards: perceived diversity exceeds actual diversity (metacognitive blind spot). The simulation estimates *d* = +1.31 for the metacognitive gap between LLM and unmediated conditions.

### Exploratory predictions

**P6 (exploratory).** Platform save features that feed into recommendation algorithms (TikTok saves, Instagram saves) produce more homogeneous hoards over time than save features that do not feed back (local screenshots, offline bookmarks). This prediction requires longitudinal observation across platforms.

**P7 (exploratory).** Hoard homogeneity is a stronger predictor of belief entrenchment than encounter homogeneity (what users saw), because the save action adds subjective endorsement to the bias. This prediction requires naturalistic longitudinal data linking hoard characteristics to belief change.

---

## 6. Discussion

### 6.1 Implications for epistemic autonomy

The three-layer bias model reframes digital hoards as epistemically consequential artifacts. A hoard is not neutral storage in the way that a filing cabinet is neutral storage. It is a biased archive assembled through a process in which both AI systems and human cognitive biases systematically exclude disconfirming information. The user who says "I've done my research" and gestures toward their saved collection may be pointing to a corpus that is narrower than they realize.

This framing aligns with emerging philosophical work on AI and epistemic agency. Recent scholarship in social epistemology argues that AI undermines epistemic agency through manipulation and bubble creation ([authors to be verified], 2025, *Social Epistemology*). The silo model provides a specific mechanism: the save layer is where epistemic autonomy is compromised most consequentially, because the user is actively participating in constructing their own biased archive. Unlike encounter bias (which the user may recognize as imposed by an algorithm) or retrieval bias (which operates through automatic memory processes), save bias involves a deliberate action that the user experiences as autonomous choice.

Huang et al.'s (2025) finding that saving health content is negatively associated with acting on it adds a further dimension. Hoards may function as belief-reinforcing repositories precisely because they are inert -- they shape what the user *believes* without requiring that the user *do* anything, including critically evaluate the saved content.

### 6.2 Implications for AI system design

The model suggests several design interventions at the save layer, informed by existing empirical work on diversity promotion.

*Diversity-aware saving with stance labels.* Jiang et al. (2025), in a controlled experiment with 142 participants, found that stance labels on news content reduced consumption of pro-attitudinal information and that stance-based filters facilitated counter-attitudinal consumption, especially for users with higher algorithmic literacy. Implementing similar labels at the point of saving -- rather than only at the point of consumption -- would address save bias directly.

*Hoard diversity dashboards.* The Shannon entropy measurement pipeline presented in this paper could be deployed as a user-facing tool that makes hoard composition visible. Just as screen time reports made invisible usage patterns visible, hoard diversity reports could make invisible bias patterns visible.

*Counter-recommendation at save time.* When a user saves an item, the system could recommend a counter-perspective item alongside it. Yu et al. (2024) found that algorithmic nudges were associated with sustainably increased news diversity on YouTube, and applying this approach specifically at the save action could address the amplification mechanism identified in the model.

*Sycophancy mitigation for search.* LLM-powered search tools could implement "grounding" approaches where the model elicits additional context with follow-up questions rather than affirming user framings (Wei et al., 2024), reducing the sycophantic filtering that precedes the save decision.

### 6.3 Implications for digital hoarding theory

The silo model proposes that content homogeneity should be recognized as a new dimension of hoarding severity, complementing the quantitative dimensions captured by existing instruments. Neither the Digital Hoarding Questionnaire (Neave et al., 2019) nor the Sedera et al. (2022) framework includes content diversity. Yet the epistemic and democratic consequences of hoarding depend not only on how much a person saves but on what they save. A user who saves 500 articles from diverse sources on a topic has a different epistemic relationship to that topic than a user who saves 500 articles all confirming the same position.

This reframing connects digital hoarding research to broader conversations about polarization and democratic epistemology. Hoarding is not just a personal productivity problem or a digital wellbeing concern -- it is a mechanism through which biased information environments crystallize into persistent personal archives.

The "storing, not reading" phenomenon observed in studies of Chinese youth (Wang et al., 2023) suggests that hoards may be linked to identity and belief formation without ever being consciously reviewed. Their mere existence as "my research" confers legitimacy on their contents, which means that the bias embedded at the save layer persists even if the user never revisits the hoard.

### 6.4 Counter-arguments

We consider five counter-arguments to the model's claims.

*Filter bubbles may be overstated.* Multiple studies question the severity of algorithmic filter bubbles (Guess et al., 2023; Liu et al., 2025; Flaxman et al., 2016), and a systematic review found only 3 of 25 experiments providing clear support (Areeb et al., 2023). Our response: the silo model does not claim filter bubbles are the dominant mechanism. It adds the save layer as an amplifier that may produce stronger effects than encounter-level filtering alone. Even if what users see is moderately diverse, what they save may be homogeneous.

*Users may save diverse content deliberately.* Research on diversity nudges (Yu et al., 2024) and stance labels (Jiang et al., 2025) shows that users can and do respond to diverse offerings. Our response: these findings are encouraging for intervention design but do not address the default case. Without nudges or labels, baseline save behavior in AI-mediated contexts remains uncharacterized.

*User agency may override algorithmic effects.* Gonzalez-Bailon et al. (2023) found that users' social networks were associated with posts in their feeds more strongly than the algorithm. Our response: user agency operates within constrained choice architectures. Jesse and Jannach (2021) frame recommendations as digital nudges that shape the choice set itself. Save bias operates on the already-filtered choice set, compounding rather than correcting the algorithmic filter.

*Disinformation spreaders show high source diversity.* Bertani et al. (2024) found that disinformation spreaders exhibited more varied web-domain choices than reliable-content sharers. Our response: diversity of sources is not the same as diversity of stances. A user can save from many different conspiracy websites (high source diversity) while saving only conspiracy-confirming content (low stance diversity). The model measures stance diversity as the primary metric.

*Simulations cannot replace experiments.* Our response: we agree. The computational demonstrations validate the framework's internal coherence -- that the proposed mechanisms, when combined, produce the predicted pattern. Whether human save behavior follows this pattern requires the controlled experiment described in Section 8. The simulation identifies expected effect sizes and methodological requirements for that experiment, serving as both theoretical validation and power analysis.

### 6.5 Regulatory implications

The EU regulatory framework provides both policy motivation and potential experimental leverage for testing the model. The Digital Services Act (DSA) Article 38 mandates that very large online platforms provide at least one non-profiling recommender alternative, and Articles 34-35 require systemic risk assessment covering effects on fundamental rights and civic discourse. The AI Act (fully applicable from August 2026) includes data governance requirements (Article 10) with bias examination obligations for high-risk systems, and Article 10(5) permits collection of sensitive data specifically for bias detection.

The silo model suggests three regulatory implications. First, the DSA's binary choice between profiled and non-profiled recommendation may be insufficient; intermediate diversity-promoting options may be needed. Second, AI Act bias requirements should extend to the save and bookmark layer as a distinct site of bias amplification. Third, "systemic risk" under DSA Article 34 should encompass the cumulative epistemic effects of biased hoards, not only the acute effects of individual content encounters.

---

## 7. Limitations

Several limitations should be acknowledged. First, the three-layer bias model has not been empirically tested with human participants. The computational demonstrations validate internal model consistency -- that the proposed mechanisms produce the predicted pattern when combined -- but human save behavior may differ in magnitude, distribution, or interaction effects. The planned controlled experiment (Section 8) is designed to address this limitation directly.

A potential criticism of computational demonstrations is circularity: the simulation's assumptions (e.g., LLM produces more homogeneous content) mechanically produce the predicted output (lower entropy in LLM condition). We address this in three ways. First, the simulation's purpose is not to test the hypothesis but to derive its quantitative implications -- it translates qualitative theoretical claims into specific, falsifiable effect size predictions (d = -0.88 for LLM vs. Unmediated) that can be directly compared against future experimental results. Second, the simulation reveals non-obvious emergent properties: the temporal entropy decline (Figure 4), the inter-user vs. intra-user diversity dissociation (Figure 5), and the metacognitive gap (d = +1.31) are not simple restatements of input parameters but emerge from their interaction. Third, the parameters themselves are independently supported by the empirical literature cited above -- they are not arbitrary but grounded in observed effect sizes from sycophancy, selective exposure, and filter bubble research.

Second, the simulation uses synthetic data with assumed parameters. Although the parameters were calibrated to empirical values from the sycophancy and filter bubble literatures, the specific combination of these parameters in a single save-behavior model has not been validated. Real save behavior may involve nonlinearities, ceiling effects, or compensatory mechanisms not captured in the simulation.

Third, the three-category stance classification (supporting, opposing, neutral) sacrifices nuance for tractability. Real content exists on a continuous spectrum and may resist categorical classification. The measurement pipeline could be extended to continuous stance measures in future work.

Fourth, the three-layer model assumes layers are approximately additive. In practice, the layers may interact nonlinearly. For example, awareness of algorithmic filtering (Layer 1) could either amplify save bias (compensatory hoarding to "capture everything before it disappears") or attenuate it (diversity-seeking as a corrective strategy). These interaction effects are not modeled in the current simulation.

Fifth, the LLM sycophancy evidence comes from separate studies documenting independent mechanisms. Their combined effect on save behavior has not been tested empirically. The simulation combines them parametrically, but the real combined effect could be larger or smaller than the sum of its parts.

Sixth, most existing digital hoarding research uses convenience samples of Chinese college students (Bai et al., 2025; Wang et al., 2023; Wu & Zhao, 2023; Liu & Liu, 2024), and platform affordances differ across TikTok, Instagram, YouTube, and browser bookmarks. The model's predictions may not generalize uniformly across cultures and platforms.

---

## 8. Future Work

The present paper establishes the theoretical framework and computational demonstrations. Three empirical studies are planned to test the model's predictions with human participants.

The immediate priority is a controlled experiment with a minimum of 240 participants in a 2 x 3 between-subjects design (information source: LLM conversational search, algorithm-curated feed, unmediated reading list; topic: controversial, neutral). Participants would research a topic for 30 minutes, saving items into a provided bookmarking tool. Dependent variables would include Shannon entropy of saved items (stance diversity), source diversity index, number of counter-arguments in a post-session summary, the perceived-versus-actual diversity gap, and belief change (pre-post). The simulation provides expected effect sizes for power analysis: *d* = -0.88 for the primary entropy comparison, *d* = +1.31 for the metacognitive gap. Pre-registration on the Open Science Framework is planned prior to data collection.

A medium-term observational hoard audit (n >= 300) would examine participants' existing digital hoards -- bookmarks, saved articles, screenshots, note-taking applications -- alongside measures of beliefs and attitudes on pre-selected topics. This study would use participant-controlled data export and the guided tour method (Jones, 2010; Jones et al., 2021) to directly test P6 (feedback-loop saves versus non-feedback saves) and P7 (hoard homogeneity versus encounter homogeneity as predictors of belief entrenchment).

A longer-term longitudinal diary study (n >= 80, four weeks) would deploy a browser extension or platform data export to track daily saving behavior across platforms, with weekly belief surveys. This would test whether hoard homogeneity increases over time, whether AI usage intensity predicts the rate of diversity decline, and whether there are tipping points of homogeneity beyond which decline accelerates.

Additionally, future work should investigate diversity-aware saving tools in a randomized controlled trial, building on intervention designs proposed by Jiang et al. (2025) and Yu et al. (2024); cross-platform hoard integration effects; AI-assisted hoard review as a bias amplifier; collective hoarding in shared collections; and developmental considerations for younger users.

---

## 9. Conclusion

This paper has introduced the three-layer bias model, which decomposes the pathway from information encounter to persistent digital hoard into encounter bias, save bias, and retrieval bias. We have argued that save bias -- the preferential saving of identity-congruent content -- is the critical amplifier in this chain, producing persistent, algorithmically weighted, and subjectively endorsed archives that shape future cognition. LLM-mediated search introduces additional mechanisms, including sycophantic framing compliance, conversational entrenchment, and apparent comprehensiveness, that further narrow the information users save.

The computational demonstrations establish the model's internal coherence. An agent-based simulation with 240 synthetic participants produced large effects of LLM mediation on hoard homogeneity (*d* = -0.88), a large metacognitive gap (*d* = +1.31), and a temporal pattern in which LLM-condition diversity declines over the course of a session -- a pattern with no analogue in the unmediated condition. These results are predictions, not findings, and they await empirical validation with human participants.

The filter bubble debate has spent a decade asking the wrong question. The question is not merely whether algorithms change what we see. It is whether the interaction between algorithmic filtering and human selective saving produces biased archives that persist, that feed back into recommendation systems, and that shape what we believe. Digital hoards are not neutral storage. They are the sedimentary record of our AI-mediated information encounters, and like any sedimentary record, they preserve some things and lose others. The silo model suggests that what they preserve is disproportionately what we already believed -- and what they lose is disproportionately what might have changed our minds.

---

## References

Anwar, M., & Schoenebeck, S. (2024). Filter bubbles or homogenization? Disentangling the effects of algorithmic recommendations using agent-based simulation. In *Proceedings of the ACM Web Conference 2024*. ACM. https://doi.org/10.1145/3589334.3645497

Areeb, Q. M., et al. (2023). Filter bubbles in recommender systems: A systematic review. *arXiv preprint*, arXiv:2307.01221.

Bai, X., et al. (2025). Information hoarding and selective exposure: The mediating roles of information overload and identity bubble reinforcement. *BMC Psychology*, *13*, Article 62. https://doi.org/10.1186/s40359-025-03062-8

Bertani, F., Mazzeo, V., & Gallotti, R. (2024). Entropy-based characterization of Internet users' media diet diversity. *Entropy*, *26*(3), Article 270. https://doi.org/10.3390/e26030270

Chen, Y., et al. (2025). [authors to be verified] Sycophantic attractors in RLHF-trained language models. *arXiv preprint*, arXiv:2509.21305.

Chheda, H., et al. (2025). ELEPHANT: An LLM framework for analyzing social sycophantic behaviors. In *Proceedings of ICLR 2026*.

Festinger, L. (1957). *A theory of cognitive dissonance*. Stanford University Press.

Flaxman, S., Goel, S., & Rao, J. M. (2016). Filter bubbles, echo chambers, and online news consumption. *Public Opinion Quarterly*, *80*(S1), 298--320. https://doi.org/10.1093/poq/nfw006

Germani, F., et al. (2025). Source framing bias in large language models. *Science Advances*, *11*, Article eadz2924. https://doi.org/10.1126/sciadv.adz2924

Gonzalez-Bailon, S., et al. (2023). Asymmetric ideological segregation in exposure to political news on Facebook. *Science*, *381*(6656), 392--398. https://doi.org/10.1126/science.ade7138

Guess, A. M., et al. (2023). How do social media feed algorithms affect attitudes and behavior in an election campaign? *Science*, *381*(6656), 398--404. https://doi.org/10.1126/science.abp9364

Huang, W., et al. (2025). Saving but not acting: The paradox of health information hoarding on social media. *International Journal of Human-Computer Interaction*. https://doi.org/10.1080/10447318.2025.2575101

Jacob, S., Kerrigan, F., & Bastos, M. (2025). The chat-chamber: How ChatGPT creates a proattitudinal information environment. *Big Data & Society*, *12*(1). https://doi.org/10.1177/20539517241306345

Jesse, M., & Jannach, D. (2021). Digital nudging with recommender systems: Survey and future directions. *Computers in Human Behavior Reports*, *3*, Article 100052.

Jiang, S., et al. (2025). Restraining the filter bubble: Stance labels and stance-based filters reduce selective exposure and attitude extremity. *Journal of the Association for Information Science and Technology*.

Kang, Y., et al. (2025). [authors to be verified] Multi-turn performance degradation in LLM generation tasks. *arXiv preprint*, arXiv:2505.06120.

Jones, W. (2010). *Keeping found things found: The study and practice of personal information management*. Morgan Kaufmann.

Jones, W., et al. (2021). Personal information management. *arXiv preprint*, arXiv:2107.03291.

Klapper, J. T. (1960). *The effects of mass communication*. Free Press.

Liu, C., & Liu, W. (2024). Digital hoarding and cognitive failure among university students: The mediating role of the Google effect. *Frontiers in Psychology*, *15*, Article 1385001.

Liu, T., et al. (2025). Limited effects of filter-bubble recommendation systems on YouTube. *Proceedings of the National Academy of Sciences*, *122*, Article e2318127122. https://doi.org/10.1073/pnas.2318127122

Mu, W., et al. (2025). Digital hoarding and subjective fatigue among knowledge workers. *Frontiers in Psychology*, *16*, Article 1501432.

Neave, N., et al. (2019). The Digital Hoarding Questionnaire: Development and initial validation. *Computers in Human Behavior*, *98*, 244--253.

Nickerson, R. S. (1998). Confirmation bias: A ubiquitous phenomenon in many guises. *Review of General Psychology*, *2*(2), 175--220.

Nguyen, C. T. (2020). Echo chambers and epistemic bubbles. *Episteme*, *17*(2), 141--161.

Pariser, E. (2011). *The filter bubble: What the Internet is hiding from you*. Penguin.

Perez, E., et al. (2022). Discovering language model behaviors with model-written evaluations. *arXiv preprint*, arXiv:2212.09251.

Sedera, D., et al. (2022). Reconceptualizing digital hoarding as an IS phenomenon: Conceptualization, measurement, and nomological net. *Information & Management*, *59*(6), Article 103685.

Sharma, M., et al. (2023). Towards understanding sycophancy in language models. In *Proceedings of ICLR 2024*.

Sharma, N., Liao, Q. V., & Xiao, Z. (2024). Generative echo chamber? Effects of LLM-powered search systems on diverse information seeking. In *Proceedings of CHI 2024*. ACM. https://doi.org/10.1145/3613904.3642459

Sprout Social. (2026). *TikTok analytics and algorithm guide*. Retrieved from https://sproutsocial.com

Tversky, A., & Kahneman, D. (1973). Availability: A heuristic for judging frequency and probability. *Cognitive Psychology*, *5*(2), 207--232.

Wang, J., Miao, C., Jia, J., & Lai, K. (2023). Digital hoarding behaviour and social networking service use: The role of FoMO and dispositional greed. *Social Media + Society*, *9*(1). https://doi.org/10.1177/20563051221150420

Wei, J., et al. (2024). [authors to be verified] Grounding approaches for reducing sycophancy in LLM-powered search. *arXiv preprint*, arXiv:2411.15287.

Wu, J., & Zhao, X. (2023). Digital hoarding in hedonic social media use: Examining the role of FoMO and platform affordances. *International Journal of Human-Computer Interaction*. https://doi.org/10.1080/10447318.2023.2233139

Yu, Z., et al. (2024). Nudging news consumption diversity on YouTube. *PNAS Nexus*, *3*(9). https://doi.org/10.1093/pnasnexus/pgae356

Zaremohzzabieh, Z., et al. (2024). Predictors of digital hoarding behavior among undergraduate students. *Digital Health*, *10*. https://doi.org/10.1177/20552076241226962

Zillmann, D., & Bryant, J. (1985). *Selective exposure to communication*. Erlbaum.
