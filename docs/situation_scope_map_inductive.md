# Inductive Situation Scope Map

Built from 62 `_pos.csv` files (5,211 total rows). Each scope below was induced solely from the curated examples in that Situation's pos file — verb inventories, ON sense annotations, VN classes, and sentence samples. Boundary analysis compares all pairs that share at least one verb lemma.

## Per-Situation Scopes

### Aggression (100 ex, 6+ verbs)
- **Realm**: Social (some Physical overlap when violent)
- **Cluster**: Aggression
- **Event type**: An agent directs hostile action (verbal, physical, or political) against a target.
- **Subject role**: Aggressor (animate or institutional).
- **Verb senses**: goad (sense 1 — badgering), abuse (abuse-v 1 — mistreatment, incl. sexual), invade (invade-v 1 — hostile entry), greet (greet-v 1 — often ironic/hostile), bless (bless-v 1 — inverse performative), shock (shock-v 1 — startle/offend).
- **VN classes**: judgement-33 (28), bully-59.5 (9), + NM (11).
- **Frames**: Transitive (agent Vs patient); occasional passive.
- **NOT**: Induction (agents don't influence behavior here; they harm). Not Contact (no required physical contact). Not Hurt (outcome-neutral — a failed invasion still counts).
- **Croft/Kalm consulted**: No.

### Buying (79 ex, 6 verbs)
- **Realm**: Social (Possession cluster).
- **Event type**: Agent acquires goods/services from a source in exchange for payment (or implicitly so).
- **Subject role**: Buyer.
- **Verb senses**: buy (1), order (order-v 2 — commercial ordering, not imperative), purchase (purchase-v 1), acquire (acquire-v 3 — commercial acquisition), book, charter.
- **VN classes**: obtain-13.5.2-1 (15), get-13.5.1 (7).
- **Frames**: Transitive (agent Vs theme), sometimes `from X` PP, `for $N` PP.
- **NOT**: Selling (opposite agent role). Not Dynamic_Possession (no commercial frame). Not Payment (theme is goods, not money). Not Request (no speech-act framing).
- **Croft/Kalm consulted**: No.

### Capacity (95 ex, 6 verbs)
- **Realm**: Physical.
- **Cluster**: Creation / Existence (dispositional).
- **Event type**: A container or space has the capacity to hold/house/seat a specified quantity or entity.
- **Subject role**: Container/Space.
- **Verb senses**: store (store-v 1), hold (hold-v 2 — capacity, not grip), contain (contain-v 1 — include), accommodate (accommodate-v 1/2 — seat/house), house (house-v 1), seat.
- **VN classes**: contiguous_location-47.8;fit-54.3 (15), keep-15.2 (14), NP (15).
- **Frames**: Transitive with a quantified theme ("holds 5 gallons"; "seats 200 people"; "houses the archives").
- **NOT**: Possession (Capacity is dispositional/potential, not ownership). Not Location (Capacity entails fit/quantity). Not Constrain (no agent imposing).
- **Croft/Kalm consulted**: No.

### Carrying (100 ex, 6+ verbs)
- **Realm**: Physical (Motion cluster).
- **Event type**: Agent co-moves a theme through space (accompanying transport).
- **Subject role**: Carrier (agent or vehicle, co-moving with theme).
- **Verb senses**: carry (1), take (4 — conveyance), haul (haul-v 2), ferry (ferry-v 1), transport (transport-v 1), kick (kick-v 9 — propel along, secondary).
- **VN classes**: carry-11.4 (18), bring-11.3 (10), NM (6).
- **Frames**: Transitive + PP (path/goal/source); optional comitative.
- **NOT**: Sending (Sending dispatches theme without agent co-motion). Not Pick_Up_and_Drop_Off (endpoint-focused, Carrying is whole-trajectory). Not Vehicular_Motion (VM is self-motion in a vehicle).
- **Croft/Kalm consulted**: No.

### Cause_Change_of_State (100 ex, 6+ verbs)
- **Realm**: Physical (Change of State cluster).
- **Event type**: Agent causes a theme to undergo a named state change (cut, bake, kill, paint, boil...).
- **Subject role**: Causer/Agent.
- **Verb senses**: cut (cut-v 1/2 — severing), bake, dice, kill (kill-v 1), boil (boil-v 2/5), paint (paint-v 2).
- **VN classes**: destroy-44 (7), murder-42.1 (7), NM (9); many sub-classes for specific changes.
- **Frames**: Transitive with a telic result implied; causative/inchoative alternations available ("Jennifer baked the potatoes" / "the potatoes baked").
- **NOT**: Change_of_State (uncaused/inchoative variant). Not Cause_Creation (no new entity produced — same entity altered). Not Hurt (CCoS is result-focused on the theme's state; Hurt is targeted harm with an experiencer).
- **Croft/Kalm consulted**: No.

### Cause_Creation (85 ex, 6+ verbs)
- **Realm**: Physical (Creation cluster).
- **Event type**: Agent causes a new entity to come into existence (build, make, design, compose, produce).
- **Subject role**: Creator/Maker.
- **Verb senses**: make (2 — fabricate), play (5/4 — perform/play a part), construct, publish, design, cut (cut-v — "cut a record").
- **VN classes**: build-26.1 (34), create-26.4 (31), performance-26.7 (10).
- **Frames**: Transitive with created theme ("made films", "constructed the subway").
- **NOT**: Cause_Change_of_State (CCoS transforms an existing entity; CCrx yields a novel one). Not Form (Form is often dispositional/developmental — grow, cultivate — without a discrete agentive making event). Not Image_Creation (IC = reproductions/representations).
- **Croft/Kalm consulted**: No.

### Cause_Incremental (100 ex, 6+ verbs)
- **Realm**: Physical (Incremental cluster).
- **Event type**: Agent applies/removes/places material along a surface or into a container, with a scale of coverage, location, or embedment.
- **Subject role**: Agent.
- **Verb senses**: bury (1/2 — cover by heaping), put (1 — locate), rub (1 — apply to surface), plant (1/3/4), stick (1/2), strengthen (intensify — abstract extension).
- **VN classes**: put-9.1 (8), remove-10.1 (9), other_cos-45.4 (8), spray-9.7, tape-22.4.
- **Frames**: Transitive + locative PP; spray/load alternation common (material vs. location focus).
- **NOT**: Incremental (uncaused/stative variant — "paint sprayed onto the wall" vs. "she sprayed paint"). Not Pick_Up_and_Drop_Off (POD is endpoint-delivery, not scalar application). Not Cause_Change_of_State (no named result state).
- **Croft/Kalm consulted**: No.

### Cause_Membership (100 ex, 6+ verbs)
- **Realm**: Social (Affiliation cluster).
- **Event type**: Agent causes a person/entity to enter or leave a group/role (hire, fire, admit, remove, recall, accept, incorporate).
- **Subject role**: Authority/Organization.
- **Verb senses**: hire (1), remove (remove-v 1), recall (3 — call back from post), admit (admit-v 1), accept (accept-v 4 — grant membership), incorporate.
- **VN classes**: hire-13.5.3 (25), banish-10.2 (15), NM (7).
- **Frames**: Transitive; frequent PP `from/to/as X` for the role/group.
- **NOT**: Cause_Participation (CP = appointing to an office/role; CM = joining a group). Not Membership (CM is the causative; M is the stative). Not Transfer_of_Possession (no ownership transfer).
- **Croft/Kalm consulted**: Yes — pairs with Cause_Participation share verbs at role boundary; see Shared-Verb Boundaries.

### Cause_Participation (73 ex, 6+ verbs)
- **Realm**: Social (Affiliation cluster).
- **Event type**: Agent designates/elects/nominates a person to a specific role or disqualifies them (elect, appoint, nominate, designate, outlaw, recruit).
- **Subject role**: Electorate/Authority.
- **Verb senses**: elect (1), appoint (1), nominate (1), designate (1/2), outlaw (1), recruit (1).
- **VN classes**: appoint-29.1 (62), orphan-29.7 (11).
- **Frames**: Transitive with role complement: "elected him Speaker", "appointed as chair".
- **NOT**: Cause_Membership (CM is joining a group; CP is taking a specific office). Not Induction (Induction influences behavior; CP assigns formal roles).
- **Croft/Kalm consulted**: No.

### Cause_and_Effect (75 ex, 5 verbs)
- **Realm**: Mental/abstract (Causation cluster).
- **Event type**: Event/entity/action brings about an outcome (effect unspecified in type — general causation).
- **Subject role**: Cause (often an event nominal or abstract entity).
- **Verb senses**: cause (1), provoke (1), raise (3), generate (1), incite (1). All "engender" semantics.
- **VN classes**: engender-27.1 (75).
- **Frames**: Transitive ("caused damage"), infinitival ("caused X to V"), nominalized effect.
- **NOT**: Cause_Change_of_State (CCoS names a specific result state). Not Cause_Creation (CCrx produces an entity). Not Induction (Induction targets an agent's behavior).
- **Croft/Kalm consulted**: No.

### Change_of_State (100 ex, 6+ verbs)
- **Realm**: Physical (Change of State cluster).
- **Event type**: A theme undergoes a state change without an overt causer (grow, darken, tighten, change, sink, harmonize).
- **Subject role**: Theme/Patient (the entity that changes).
- **Verb senses**: grow (2/3 — increase/develop), darken (1), tighten (tighten-v 2 — become strict), change (1), sink (1), harmonize.
- **VN classes**: other_cos-45.4 (35), NM (16), NP (6).
- **Frames**: Intransitive / anticausative; copular + adjective for resulting state.
- **NOT**: Cause_Change_of_State (has overt causer). Not Form (Form = development of shape/structure; CoS = state property change).
- **Croft/Kalm consulted**: Yes — inchoative/causative alternation is the central boundary for CoS vs. CCoS.

### Charge (100 ex, 6+ verbs)
- **Realm**: Social (Possession cluster).
- **Event type**: Agent imposes a financial/material debit on a recipient (charge, fine, tax, bill) OR the inverse (save, spare, cost).
- **Subject role**: Agent imposing cost, or transaction itself (cost as subject).
- **Verb senses**: charge (charge-v 1 — financial, NOT accusation or rushing), save (save-v 3 — spare from expense), cost (cost-v 1), spare (spare-v 1/2), fine (fine-v 1), tax (tax-v 1).
- **VN classes**: bill-54.5 (45), cost-54.2 (15), bill-54.5;judgement-33 (15).
- **Frames**: Ditransitive ("charged him $500"), transitive cost-subject ("it cost me $5").
- **NOT**: Payment (Payment is the payer's action of remitting money; Charge is the imposer's action). Not Request (no speech-act; Charge imposes, doesn't solicit). Not Aggression (charge-v 1 ≠ charge-v "attack").
- **Croft/Kalm consulted**: No.

### Collective (66 ex, 2 verbs)
- **Realm**: Social (Affiliation cluster).
- **Event type**: Agent(s) join or participate in a group/activity.
- **Subject role**: Joiner/Participant.
- **Verb senses**: join (4 — become part of; 3 — combine with), participate (1).
- **VN classes**: cooperate-73.1 (66).
- **Frames**: Transitive "join X" or intransitive + `in` PP.
- **NOT**: Reciprocal (Collective admits unilateral joining; Reciprocal requires symmetry). Not Participation (Participation is role-fulfillment; Collective is categorical entry).
- **Croft/Kalm consulted**: No.

### Communicate (71 ex, 6 verbs)
- **Realm**: Social (Communication cluster).
- **Event type**: Agent transmits information to a recipient (tell, ask, warn, inquire, quote, teach).
- **Subject role**: Speaker/Sender.
- **Verb senses**: tell (1), ask (1 — inquire, not request), warn (1), inquire (1), quote (1), teach (1).
- **VN classes**: transfer_mesg-37.1.1 (34), inquire-37.1.2 (26), advise-37.9 (8).
- **Frames**: Ditransitive / prepositional complement / embedded clause.
- **NOT**: Statement (Statement = monologic assertion; Communicate = directed transfer with recipient). Not Request (Request demands a specific action; Communicate transmits info). Not Joint_Statement (JS is bilateral/reciprocal speech).
- **Croft/Kalm consulted**: No.

### Concealment (93 ex, 6+ verbs)
- **Realm**: Physical/Social (Incremental cluster — concealment is spatial/perceptual obstruction).
- **Event type**: Agent or element hides, blocks, or masks something from view/access.
- **Subject role**: Concealer (agent or inanimate obstructor).
- **Verb senses**: hide (1), block (block-v 1 — obstruct view/access), cover (cover-v 1/2), shroud, sequester (sequester-v 3 — isolate), mask (mask-v 1/2 — cover / disguise).
- **VN classes**: concealment-16 (34), fill-9.8 (17), NM (14).
- **Frames**: Transitive + source/perceiver PP; passive common ("shrouded in fog").
- **NOT**: Limitation (Limitation restricts quantity/permission; Concealment restricts perception). Not Protection (Protection shields from harm; Concealment hides from view).
- **Croft/Kalm consulted**: No.

### Constrain (66 ex, 2 verbs)
- **Realm**: Physical/Social (Force cluster — bodily dressing, wearing).
- **Event type**: Agent wears or dons an item of clothing/accessory; rare: contains.
- **Subject role**: Wearer.
- **Verb senses**: wear (1 — have on the body; 65 rows), hold (6 — contain a person, 1 row).
- **VN classes**: simple_dressing-41.3.1 (65), contain-15.4 (1).
- **Frames**: Transitive (subject wears item).
- **NOT**: Possession (wearing is not owning; the worn item is held-on, not held-as-property). Not Protection (no harm-avoidance inferred). Not Capacity (hold-v 6 here = "accommodate one person"; Capacity is hold-v 2).
- **Croft/Kalm consulted**: Yes — "Constrain" label is counter-intuitive given verb inventory (almost entirely `wear`); example sentences anchor the scope to dressing, not binding/restraining.

### Contact (50 ex, 6+ verbs)
- **Realm**: Physical (Force cluster).
- **Event type**: Agent makes physical contact with a theme, typically with short, bounded force (punch, touch, gouge, beat, prick, peck).
- **Subject role**: Contactor/Agent.
- **Verb senses**: punch (1), touch (1), gouge (1), beat (3 — strike repeatedly), prick, peck.
- **VN classes**: swat-18.2 (14), touch-20 (13), carve-21.2 (6).
- **Frames**: Transitive; locative/instrument PP optional.
- **NOT**: Hurt (Hurt is outcome-focused on harm; Contact is the contact event itself). Not Throwing (no projectile phase). Not Manipulation (Manipulation entails continued use/operation of an instrument).
- **Croft/Kalm consulted**: No.

### Counting (58 ex, 2 verbs)
- **Realm**: Mental (Evaluation cluster).
- **Event type**: Agent enumerates or tallies items in a collection.
- **Subject role**: Counter.
- **Verb senses**: count (1 — enumerate), add (2 — mathematically combine).
- **VN classes**: multiply-108 (58).
- **Frames**: Transitive with a countable theme.
- **NOT**: Measurement (Measurement quantifies magnitude; Counting tallies discrete items). Not Evaluation (Evaluation judges worth; Counting is pure enumeration).
- **Croft/Kalm consulted**: No.

### Desire (100 ex, 6+ verbs)
- **Realm**: Mental (Intention cluster — desire subcategory).
- **Event type**: Experiencer has an attitude toward a wanted/preferred outcome (need, prefer, hope, want, wish, love).
- **Subject role**: Experiencer.
- **Verb senses**: need (1), prefer, hope (hope-v 1 — wish outcome), want (want-v 1), wish, love (love-v 1 — strong preference).
- **VN classes**: want-32.1 (25), long-32.2-1;wish-62 (14).
- **Frames**: Transitive + theme; infinitival ("want to V"); small clause ("prefer X to Y").
- **NOT**: Intention (Intention is aim-directed action planning; Desire is static preference/longing). Not Emotion_(exp. subj.) (Emotion centers on a felt state, not an object of wanting).
- **Croft/Kalm consulted**: Yes — Desire vs. Intention distinction is the central boundary; see Shared-Verb Boundaries.

### Discovery (66 ex, 6+ verbs)
- **Realm**: Mental (Cognition cluster).
- **Event type**: Experiencer comes to know something — by finding, learning (stative), guessing, or ascertaining.
- **Subject role**: Discoverer/Knower.
- **Verb senses**: learn (2 — "come to know", ALSO 1 — "study"), guess (2 — conjecture), find (1 — locate), read (1 — gather info from text), discover, ascertain (1).
- **VN classes**: learn-14 (26), discover-84 (23).
- **Frames**: Transitive with theme clause ("learned that X", "found the number").
- **NOT**: Learning (Learning is the process/act of studying; Discovery is the outcome of coming-to-know, often sudden). Not Perception_(exp._subj.) (Perception is direct sensory; Discovery is cognitive).
- **Croft/Kalm consulted**: Yes — `learn` crosses Discovery and Learning; ON sense 1 (study) vs 2 (come-to-know) is the split.

### Dynamic_Possession (100 ex, 6+ verbs)
- **Realm**: Social (Possession cluster).
- **Event type**: Agent gains, transfers, or holds a theme transiently; non-commercial change of possession.
- **Subject role**: Recipient/Holder (or sometimes source).
- **Verb senses**: borrow (1), donate (1), collect (collect-v 1/2), receive (1), catch (catch-v 2 — grasp/acquire), distribute (1).
- **VN classes**: obtain-13.5.2 (24), get-13.5.1 (12), get-13.5.1-1 (10).
- **Frames**: Transitive + `from/to/for` PP.
- **NOT**: Buying/Selling (no commerce frame). Not Possession (DP is dynamic event, Possession is stative). Not Transfer_of_Possession (ToP here is coercive/illicit — steal/rob — while DP is volitional).
- **Croft/Kalm consulted**: No.

### Emission (100 ex, 6+ verbs)
- **Realm**: Physical (Creation cluster — ouput/emission subcategory).
- **Event type**: Source emits light, sound, smell, or substance (flicker, shine, leak, ring, bleed, reek).
- **Subject role**: Emitter.
- **Verb senses**: flicker (1), shine (1), leak (leak-v 1 — substance escape), ring (ring-v 1 — sound), bleed (bleed-v 1), reek (reek-v 2 — smell strongly).
- **VN classes**: light_emission-43.1 (26), sound_emission-43.2 (17), substance_emission-43.4 (11).
- **Frames**: Intransitive (emission event) or transitive (source V something).
- **NOT**: Perception_(stim._subj.) (reek crosses — PSS frames the emitted property as a predicate over the subject; Emission frames the release itself).
- **Croft/Kalm consulted**: Yes — `reek` is the shared verb; reek-v 1 (smells-like, Perception) vs reek-v 2 (emits smell, Emission).

### Emotion_(exp. subj.) (55 ex, 6 verbs)
- **Realm**: Mental (Emotion cluster).
- **Event type**: Experiencer has an emotion directed at/concerning a theme (like, support, enjoy, fear, worry, care).
- **Subject role**: Experiencer.
- **Verb senses**: like (2 — be fond of), support (2 — back emotionally), enjoy (1), fear (2), worry (1 — be anxious), care (1).
- **VN classes**: admire-31.2 (41), marvel-31.3 (14).
- **Frames**: Transitive; prepositional ("care about", "worry about").
- **NOT**: Emotion_(stim. subj.) (linking-reversal: in ESS the stimulus is subject). Not Desire (Desire is want-directed; EES is felt state).
- **Croft/Kalm consulted**: No.

### Emotion_(stim. subj.) (100 ex, 6+ verbs)
- **Realm**: Mental (Emotion cluster).
- **Event type**: Stimulus causes an experiencer to feel an emotion (motivate, impress, depress, concern, worry, please).
- **Subject role**: Stimulus.
- **Verb senses**: motivate (1), impress (1), depress (depress-v 2), concern (concern-v 1/2 — trouble), worry (worry-v 1 — cause anxiety), please (please-v 1/2).
- **VN classes**: amuse-31.1 (52), NM (9), force-59 (6).
- **Frames**: Transitive (X V Y), passive common ("Y was impressed by X").
- **NOT**: Emotion_(exp. subj.) (linking-reversal). Not Induction (Induction changes behavior via argument/persuasion; ESS changes feeling).
- **Croft/Kalm consulted**: No.

### Enforcement (64 ex, 2 verbs)
- **Realm**: Social (Control cluster).
- **Event type**: Agent/institution exerts authority to maintain rules, regulations, or conditions (control, enforce).
- **Subject role**: Enforcer/Authority.
- **Verb senses**: control (1 — exercise authority over), enforce (1).
- **VN classes**: enforce-63 (64).
- **Frames**: Transitive with a governed theme (rules, institutions).
- **NOT**: Constrain (Constrain in this dataset = `wear`; Enforcement is institutional power). Not Limitation (Limitation restricts extent/quantity; Enforcement maintains compliance). Not Induction (Induction persuades; Enforcement imposes).
- **Croft/Kalm consulted**: No.

### Evaluation (107 ex, 6+ verbs)
- **Realm**: Mental (Evaluation cluster).
- **Event type**: Agent assesses the value, quality, or nature of a theme (estimate, consider, evaluate, analyze, judge, rate).
- **Subject role**: Evaluator.
- **Verb senses**: estimate (1 — compute approximate value), consider (2 — think about as), evaluate, analyze, judge, rate.
- **VN classes**: estimate-34.2 (74), consider-29.9 (14), assessment-34.1 (1).
- **Frames**: Transitive with theme; "consider X (as) Y" complex complement.
- **NOT**: Counting (Counting tallies discrete items; Evaluation assigns a judgment). Not Measurement (Measurement reports objective quantity; Evaluation includes subjective assessment). Not Learning/Discovery (no come-to-know).
- **Croft/Kalm consulted**: No.

### Existence (100 ex, 6+ verbs)
- **Realm**: Mental/abstract (Existence cluster).
- **Event type**: An entity exists, persists, or is located/present (be, wait, remain, flex, laugh, kick — the latter are peripheral physical/expressive presence).
- **Subject role**: Existent.
- **Verb senses**: be (4 — exist/be present), wait (1), remain (2 — stay), flex (1 — show/display), laugh (1 — express by laughing), kick (kick-v 1/5).
- **VN classes**: exist-47.1 (35), nonverbal_expression-40.2 (5), crane-40.3.2 (4).
- **Frames**: Copular; intransitive; existential "there V X".
- **NOT**: Location (Location involves a specified place). Not Possession (Possession is a relation, not a state of being). Not Capacity (dispositional vs. factual).
- **Note**: This Situation corresponds to Croft's "Internal" (§4.8): a physical entity undergoing some mode of existence. This encompasses internal bodily phenomena (shiver, hiccup, snooze) as well as inanimate modes of being (flutter, wobble, swarm). The common thread is a single physical entity in an undirected, non-relational process. This is NOT an abstract existential category.
- **Croft/Kalm consulted**: Yes (§4.8).

### Feeding (65 ex, 6+ verbs)
- **Realm**: Physical (Ingestion cluster — other-directed).
- **Event type**: Agent provides food/nourishment to a consumer (feed, bottle-feed, nurse, wean, sustain, breast-feed).
- **Subject role**: Feeder.
- **Verb senses**: feed (1). Others are single-sense.
- **VN classes**: feeding-39.7 (15).
- **Frames**: Transitive + theme (the fed entity); optional `X to Y` PP for food.
- **NOT**: Ingestion (self-directed consumption; Feeding is other-directed provision).
- **Croft/Kalm consulted**: No.

### Form (100 ex, 6+ verbs)
- **Realm**: Physical (Creation cluster — developmental/structural).
- **Event type**: Agent or natural process brings a structure/organism into shape or arrangement (assemble, cultivate, shape, grow, arrange, form).
- **Subject role**: Shaper or Forming-entity (natural or agentive).
- **Verb senses**: assemble (1/2), cultivate (cultivate-v 1 — raise crops), shape (shape-v 1/2/3), grow (grow-v 2 — cultivate, not self-grow), arrange (1/2), form (form-v 1/2/3).
- **VN classes**: NP (18), NM (16), build-26.1 (7).
- **Frames**: Transitive (agent shapes X); intransitive ("that acorn will grow").
- **NOT**: Cause_Creation (CCrx produces a discrete new entity; Form develops structure/shape over time or from parts). Not Change_of_State (Form includes agentive shaping; CoS is bare change).
- **Croft/Kalm consulted**: Yes — `grow`/`form`/`develop` straddle Form, Cause_Creation, Change_of_State, Location.

### Future_Having (100 ex, 6+ verbs)
- **Realm**: Social (Possession cluster).
- **Event type**: Agent provides a future claim or entitlement to a recipient (offer, issue, award, guarantee, owe, grant).
- **Subject role**: Grantor/Debtor.
- **Verb senses**: offer (1/4), issue (1), award (1), guarantee (1), owe (1/2), grant (1).
- **VN classes**: future_having-13.3 (58), NP (8), conjecture-29.5-2;future_having-13.3 (5).
- **Frames**: Ditransitive / prepositional goal.
- **NOT**: Buying/Selling (no completed commercial transaction). Not Transfer_of_Possession (no completed transfer — the having is prospective).
- **Croft/Kalm consulted**: No.

### Hurt (100 ex, 6+ verbs)
- **Realm**: Physical/Social (Change of State cluster — harm-focused).
- **Event type**: Agent or event causes physical/emotional harm to an entity (hurt, cut, burn, damage, injure, nick).
- **Subject role**: Harmer (agent or impersonal source).
- **Verb senses**: hurt (1), cut (cut-v 1 — cause cut), burn (burn-v 1), damage (1), injure (1), nick.
- **VN classes**: hurt-40.8.3 (26), amuse-31.1 (11), destroy-44 (10).
- **Frames**: Transitive; reflexive common ("Tessa hurt herself").
- **NOT**: Cause_Change_of_State (CCoS targets a state change; Hurt specifically targets harm/injury). Not Aggression (Aggression is attack-oriented; Hurt is outcome-of-harm).
- **Croft/Kalm consulted**: Yes — `cut`/`burn` span Hurt, Cause_Change_of_State, and Cause_Creation; see Shared-Verb Boundaries.

### Image_Creation (64 ex, 6 verbs)
- **Realm**: Physical (Creation cluster — representational output).
- **Event type**: Agent produces a durable representation/record (record, print, copy, tape, engrave, sign).
- **Subject role**: Recorder.
- **Verb senses**: record (1), print (1), copy (1/2), tape (2 — record), engrave (1), sign (3 — inscribe).
- **VN classes**: transcribe-25.4 (23), scribble-25.2 (20), image_impression-25.1 (8).
- **Frames**: Transitive (V theme); V on/onto PP for medium.
- **NOT**: Cause_Creation (CCrx produces physical/abstract original entities; IC produces reproductions/representations). Not Statement (no speech-event).
- **Croft/Kalm consulted**: No.

### Incremental (100 ex, 6+ verbs)
- **Realm**: Physical (Incremental cluster).
- **Event type**: Substance/material fills, covers, or distributes across a surface or along a path (hang, plaster, spray, seal, rivet, cling) — often uncaused/stative.
- **Subject role**: Theme (the distributed substance) OR a ground that is covered.
- **Verb senses**: hang (1/8), plaster (2 — coat), spray (1), seal (1/5 — close), rivet (2), cling (1).
- **VN classes**: spray-9.7 (7), tape-22.4 (5), herd-47.5.2 (5).
- **Frames**: Intransitive with ground+theme (spray/load alternation — subject can be theme OR surface).
- **NOT**: Cause_Incremental (CInc has overt causer). Not Concealment (covering for hiding vs. material distribution).
- **Croft/Kalm consulted**: No.

### Induction (100 ex, 6+ verbs)
- **Realm**: Social (Control cluster).
- **Event type**: Agent influences another agent's behavior through argument, pressure, or manipulation (goad, compel, prompt, manipulate, cheat, persuade).
- **Subject role**: Inducer.
- **Verb senses**: goad (1), compel (1), prompt (1), manipulate (1 — influence deceptively), cheat (2 — deceive for gain), persuade (1).
- **VN classes**: compel-59.1 (11), bully-59.5 (11), appoint-29.1 (11).
- **Frames**: Transitive + infinitival ("compel X to V"); transitive + PP ("manipulate X into V-ing").
- **NOT**: Enforcement (Enforcement imposes institutional rules; Induction works on individual behavior). Not Cause_Participation (CP assigns a formal role; Induction changes behavior without role-assignment). Not Aggression (Aggression: `goad` at sense 1 also here — overlap — the inducer intends behavior change, the aggressor intends harm/insult).
- **Croft/Kalm consulted**: Yes — `goad` and `manipulate` are shared with Aggression / Manipulation.

### Ingestion (73 ex, 6+ verbs)
- **Realm**: Physical (Ingestion cluster — self-directed).
- **Event type**: Agent consumes food or a substance (eat, drink, graze, smoke, chew, dine).
- **Subject role**: Consumer (self-directed).
- **Verb senses**: eat (1), drink (1), graze (1), smoke (1), chew (1), dine (1).
- **VN classes**: eat-39.1 (48), dine-39.5 (10), chew-39.2 (3).
- **Frames**: Transitive; intransitive (eat/drink/dine).
- **NOT**: Feeding (Feeding is other-directed nourishment provision).
- **Croft/Kalm consulted**: No.

### Intention (177 ex, 6+ verbs)
- **Realm**: Mental (Intention cluster — action-planning/seeking).
- **Event type**: Experiencer aims at, seeks, or pursues a goal cognitively (hope, look, pray, search, long, seek).
- **Subject role**: Intender/Seeker.
- **Verb senses**: hope (hope-v 1 — with future goal), look (look-v 1 — "look for" = search), pray (1), search (1), seek (1), long (long-v 1 — yearn-toward).
- **VN classes**: long-32.2 (72), peer-30.3 (20), hunt-35.1 (6).
- **Frames**: Prepositional ("look for", "search for"), infinitival ("hope to V").
- **NOT**: Desire (Desire has NO goal-seeking action; Intention is active pursuit). Not Perception_(exp._subj.) (Perception's `look` = direct gaze; Intention's `look` = look-for/search).
- **Croft/Kalm consulted**: Yes — `hope`/`look` span Intention and Desire/Perception; ON sense is the split.

### Joint_Statement (93 ex, 6 verbs)
- **Realm**: Social (Communication cluster — reciprocal).
- **Event type**: Two or more parties reciprocally communicate or reach alignment (agree, debate, cooperate, disagree, confer, chitchat).
- **Subject role**: Co-participants.
- **Verb senses**: agree (1 — consent; 3 — concur), cooperate (1), disagree (1), confer (2), debate, chitchat.
- **VN classes**: correspond-36.1 (69), chit_chat-37.6 (1).
- **Frames**: Plural subject / conjoined `X and Y V`; `V with X`; intransitive ("They agreed").
- **NOT**: Statement (Statement is unilateral; JS is bilateral/plural-subject). Not Collective (Collective is entering a group; JS is reaching consensus). Not Reciprocal (Reciprocal is any symmetric action; JS is specifically communicative).
- **Croft/Kalm consulted**: No.

### Learning (60 ex, 4 verbs)
- **Realm**: Mental (Cognition cluster).
- **Event type**: Agent engages in study or acquisition of knowledge/skill (learn, read, study, memorize).
- **Subject role**: Learner.
- **Verb senses**: learn (1 — study; 2 — come-to-know), read (1), study (2 — investigate systematically), memorize (no sense given).
- **VN classes**: learn-14 (48).
- **Frames**: Transitive (study X, read X); `learn about/from` PP.
- **NOT**: Discovery (Discovery is the outcome of coming-to-know; Learning is the ongoing process). Note: `learn` ON sense 2 could belong to Discovery instead; Josh's examples here use sense 1 predominantly (study).
- **Croft/Kalm consulted**: Yes — `learn` split with Discovery; see Shared-Verb Boundaries.

### Limitation (100 ex, 6+ verbs)
- **Realm**: Social (Control cluster — scope restriction).
- **Event type**: Agent or factor restricts the extent, quantity, or permissibility of something (limit, restrict, restrain, block, hinder, curb).
- **Subject role**: Limiter (agent or inanimate restriction).
- **Verb senses**: restrict (1), restrain (restrain-v 2 — hold back), block (block-v 2 — prevent, block-v 1 — obstruct), hinder (1), curb (1).
- **VN classes**: limit-76 (31), forbid-67 (22), NP (17).
- **Frames**: Transitive + theme; "restrict X to Y" PP.
- **NOT**: Concealment (Concealment blocks perception; Limitation blocks action/quantity). Not Enforcement (Enforcement maintains rules; Limitation sets boundaries). Not Protection (no harm-avoidance).
- **Croft/Kalm consulted**: No.

### Location (100 ex, 6+ verbs)
- **Realm**: Physical (Motion cluster — stative locative).
- **Event type**: Entity is located at, stays at, or emerges into a place (come, flow, stop, adjoin, emerge, stand).
- **Subject role**: Located-entity / Path-entity.
- **Verb senses**: come (2/5 — originate from, arrive at), flow (1), stop (stop-v 3 — rest at), emerge (emerge-v 2), stand (1/2/3 — be positioned), adjoin.
- **VN classes**: appear-48.1.1 (24), contiguous_location-47.8 (10), NM (7).
- **Frames**: Intransitive + locative PP.
- **NOT**: Motion (Motion is trajectory/displacement; Location is positional/existential-at-place). Not Existence (Existence is state of being, without a specified location).
- **Croft/Kalm consulted**: No.

### Manipulation (100 ex, 6+ verbs)
- **Realm**: Physical (Force cluster — instrumental).
- **Event type**: Agent uses or operates an instrument/tool/object (use, spin, exploit, carve, fold, operate).
- **Subject role**: User/Operator.
- **Verb senses**: use (1), spin (1/2/7 — turn, rotate), exploit (1 — use for advantage), carve (carve-v 1/3 — fashion by cutting), fold (1/3/4), operate (1/2).
- **VN classes**: use-105.1 (26), NM (12), NP (9).
- **Frames**: Transitive with instrument/theme.
- **NOT**: Contact (Contact is bounded impact; Manipulation is sustained use). Not Cause_Creation (Manipulation may use a tool, but no new entity produced). Not Induction (Induction manipulates agents; Manipulation manipulates objects — shared verb, different target).
- **Croft/Kalm consulted**: Yes — `manipulate` at object vs. person boundary.

### Measurement (60 ex, 6 verbs)
- **Realm**: Mental (Evaluation cluster).
- **Event type**: Agent or object registers/reports a quantitative property (cost, measure, take, total, gauge, weigh).
- **Subject role**: Measured-entity (as subject of `cost/measure/weigh`) or Measurer.
- **Verb senses**: cost (1), measure (1 — quantify; 3 — be of size), take (3 — require time), total (1 — sum to), gauge (1).
- **VN classes**: cost-54.2 (26), register-54.1 (23), price-54.4 (5).
- **Frames**: Transitive; "X V Quantity" ("the book costs $10", "measures 12 feet").
- **NOT**: Counting (Counting enumerates discrete items; Measurement reports magnitude). Not Evaluation (no subjective judgment). Not Charge (Charge imposes cost; Measurement reports it).
- **Croft/Kalm consulted**: No.

### Membership (71 ex, 6 verbs)
- **Realm**: Social (Affiliation cluster).
- **Event type**: Agent is a member of, manages, or belongs to a group or institution (attend, manage, oversee, belong, govern).
- **Subject role**: Member or Supervisor.
- **Verb senses**: attend (1 — be present at / be a member of), manage (manage-v 2 — supervise), oversee (1), belong (belong-v 2 — be a part of), govern (1).
- **VN classes**: attend-107.4 (41), supervision-95.2.2 (30).
- **Frames**: Transitive (attend a school, oversee a team); `belong to` PP.
- **NOT**: Participation (Participation fills a role; Membership is categorical affiliation). Not Cause_Membership (causative counterpart). Not Possession (`belong` sense 2 here is "member of", not ownership).
- **Croft/Kalm consulted**: No.

### Motion (51 ex, 6 verbs)
- **Realm**: Physical (Motion cluster).
- **Event type**: Entity undergoes self-directed displacement (come, leave, travel, move, glide) or a theme follows a path (cut through).
- **Subject role**: Mover.
- **Verb senses**: come (1 — approach), leave (1 — depart), travel (1), move (1), glide (1). `cut` here = traverse cleanly.
- **VN classes**: escape-51.1 (25), run-51.3.2 (7), slide-11.2 (3).
- **Frames**: Intransitive + path PP.
- **NOT**: Vehicular_Motion (VM requires vehicle/mode). Not Location (Location is stative/positional; Motion is change-of-position). Not Pursuit (Pursuit is goal-directed motion).
- **Croft/Kalm consulted**: No.

### Participation (100 ex, 6+ verbs)
- **Realm**: Social (Affiliation cluster).
- **Event type**: Agent fills or enacts a role (serve, act, host, behave, love, appreciate).
- **Subject role**: Role-filler.
- **Verb senses**: serve (3 — do duty as), act (2 — behave as), host (1 — be host), behave (1), love/appreciate (peripheral — evaluative participation).
- **VN classes**: masquerade-29.6 (28), admire-31.2 (14), captain-29.8 (7).
- **Frames**: Intransitive "act as X"; prepositional ("serve on the board").
- **NOT**: Membership (M is categorical affiliation; Participation is role-enactment). Not Cause_Participation (causative counterpart). Not Collective (Collective is joining, not ongoing role).
- **Croft/Kalm consulted**: No.

### Payment (71 ex, 1 verb)
- **Realm**: Social (Possession cluster).
- **Event type**: Agent pays (money for goods, services, or obligations).
- **Subject role**: Payer.
- **Verb senses**: pay (1 — remit payment) — monoculture.
- **VN classes**: pay-68 (67).
- **Frames**: Ditransitive ("pay X $Y"), `pay for X`, passive ("it's paid for").
- **NOT**: Buying (Buying foregrounds goods; Payment foregrounds money transfer). Not Charge (Charge imposes the cost; Payment remits it).
- **Croft/Kalm consulted**: No.

### Perception_(exp._subj.) (71 ex, 6 verbs)
- **Realm**: Mental (Perception cluster — experiencer-subject).
- **Event type**: Experiencer perceives a stimulus (see, look, hear, notice, spot, detect).
- **Subject role**: Experiencer.
- **Verb senses**: see (1 — visual; 6 — understand), look (1 — direct gaze), hear (1/2), notice (1), spot (1), detect (1).
- **VN classes**: see-30.1 (39), peer-30.3 (13), sight-30.2 (4).
- **Frames**: Transitive ("saw the play"); `look at` PP.
- **NOT**: Perception_(stim._subj.) (linking-reversal). Not Intention (Intention's `look` = look-for/search; PES's `look` = direct gaze).
- **Croft/Kalm consulted**: Yes — `look` is 3-way ambiguous across Perception_(exp.), Perception_(stim.), Intention.

### Perception_(stim._subj.) (100 ex, 6+ verbs)
- **Realm**: Mental (Perception cluster — stimulus-subject).
- **Event type**: Stimulus appears/sounds/feels a certain way to an implicit experiencer (sound, look, feel, appear, seem, reek).
- **Subject role**: Stimulus.
- **Verb senses**: sound (sound-v 1 — "sounds like"), look (look-v 2 — "looks tired"), feel (feel-v 1 — tactile property: "the fabric feels soft"), appear (1), seem (1), reek (reek-v 1 — smells-like).
- **VN classes**: NM (28), marvel-31.3-3;see-30.1-1;stimulus_subject-30.4 (14), smell_emission-43.3 (4).
- **Frames**: Copular-like: `X V Adj/Clause` ("looks tired", "seems fine"). Not transitive with experiencer.
- **NOT**: Perception_(exp._subj.) (linking-reversal). Not Emission (reek-v 1 = smells-like property; Emission's reek-v 2 = emits smell).
- **Croft/Kalm consulted**: Yes — see `look`/`reek` shared-verb boundaries.

### Pick_Up_and_Drop_Off (100 ex, 6+ verbs)
- **Realm**: Physical (Motion cluster — endpoint/delivery).
- **Event type**: Agent moves a theme to a specified endpoint (drop, pick, raise, deliver, hoist, lift).
- **Subject role**: Agent.
- **Verb senses**: drop (1 — release/lower), pick (pick-v 7.1 — "pick up"), raise (2 — lift), deliver (deliver-v 1 — convey to recipient), hoist (hoist-v 2 — heave upward), lift (1).
- **VN classes**: put_direction-9.4 (31), NM (10), carry-11.4 (10).
- **Frames**: Transitive + direction/goal PP.
- **NOT**: Carrying (Carrying is trajectory-focused; POD is endpoint/delivery-focused). Not Cause_Incremental (POD is singular event, CInc is scalar filling/application).
- **Croft/Kalm consulted**: No.

### Possession (82 ex, 3 verbs)
- **Realm**: Social (Possession cluster — stative).
- **Event type**: Possessor owns/has a theme statively.
- **Subject role**: Possessor.
- **Verb senses**: own (1 — legal ownership), have (possession), belong (reverse linking: theme=subject).
- **VN classes**: own-100.1 (74).
- **Frames**: Transitive; `X belongs to Y`.
- **NOT**: Dynamic_Possession (DP is a change event; P is stative). Not Constrain (wearing ≠ owning). Not Capacity (capacity ≠ having).
- **Croft/Kalm consulted**: No.

### Protection (57 ex, 4 verbs)
- **Realm**: Social/Physical (Aggression cluster — defensive).
- **Event type**: Agent shields a target from harm (protect, defend, guard, safeguard).
- **Subject role**: Protector.
- **Verb senses**: protect (1), defend (2 — uphold/shield), guard (1), safeguard (1).
- **VN classes**: defend-72.3 (51).
- **Frames**: Transitive + `from` PP.
- **NOT**: Aggression (Aggression is the attack; Protection is the defense). Not Concealment (Concealment hides; Protection shields).
- **Croft/Kalm consulted**: No.

### Pursuit (100 ex, 6+ verbs)
- **Realm**: Physical (Motion cluster — goal-directed).
- **IN**: Physical co-motion with adversarial or pursuit relation (chase, follow, trail), OR directed search activity toward a target (search for, hunt for, investigate). The common thread is directed motion or effort toward a target that has not yet been reached.
- **Subject role**: Pursuer/Guide.
- **Verb senses**: chase (1), lead (5 — guide), steer (1), inspect (1), investigate (1), excavate (1).
- **VN classes**: accompany-51.7 (15), chase-51.6 (12), search-35.2 (10).
- **Frames**: Transitive.
- **OUT**: Motion (Motion is self-displacement; Pursuit is goal-directed toward a target). Not Intention (Intention is cognitive seeking; Pursuit is physical/investigative pursuit). Stative desire for unrealized goal without active seeking → Desire. Commitment to a future action without search → Intention. Care/maintenance without pursuit → NOT this Situation.
- **Croft/Kalm consulted**: No.

### Reciprocal (64 ex, 6 verbs)
- **Realm**: Social (Reciprocal cluster).
- **Event type**: Two or more parties engage symmetrically (meet, visit, fight, marry, compete, hug).
- **Subject role**: Co-participants.
- **Verb senses**: meet (1/2 — encounter / match-up), visit (1), fight (1), marry (1), compete (1), hug (1).
- **VN classes**: meet-36.3 (40), battle-36.4 (10), marry-36.2 (5).
- **Frames**: Intransitive plural/conjoined subject; "X Vs Y" with symmetric reading.
- **NOT**: Joint_Statement (JS is reciprocal speech; Reciprocal can be physical/social). Not Collective (Collective is joining a group; Reciprocal is mutual interaction).
- **Croft/Kalm consulted**: No.

### Replacement (100 ex, 6+ verbs)
- **Realm**: Social (Reciprocal cluster — substitution).
- **Event type**: One entity replaces/succeeds/exchanges/ousts another (replace, exchange, succeed, oust, substitute, switch).
- **Subject role**: Successor / Replacement-agent.
- **Verb senses**: replace (1), exchange (1/2), succeed (succeed-v 1/2 — follow in office / accomplish), oust (1/2), substitute (1 — act as replacement), switch (2).
- **VN classes**: substitute-13.6.2 (36), exchange-13.6-1 (15), NM (9).
- **Frames**: Transitive + `by/for` PP.
- **NOT**: Cause_Membership (CM is hire/fire; Replacement foregrounds the new-for-old substitution).
- **Croft/Kalm consulted**: No.

### Request (85 ex, 6+ verbs)
- **Realm**: Social (Communication cluster — directive).
- **Event type**: Agent requests/demands/commands an action from a target (ask, urge, order, demand, request, beg).
- **Subject role**: Requester/Commander.
- **Verb senses**: ask (2 — request action, NOT inquire), urge (1/2), order (1 — command), demand (1), request (1), beg (1).
- **VN classes**: urge-58.1 (43), order-58.3 (21), beg-58.2 (6).
- **Frames**: Ditransitive with infinitival ("asked him to V"), transitive ("demanded a refund").
- **NOT**: Communicate (Communicate's `ask` = inquire; Request's `ask` = demand action). Not Statement (Request is directive; Statement is assertive).
- **Croft/Kalm consulted**: Yes — `ask` sense 1 (inquire, Communicate) vs sense 2 (request action, Request).

### Response (64 ex, 6 verbs)
- **Realm**: Social (Communication cluster — reactive).
- **Event type**: Agent reacts to a prior act, statement, or threat (face, respond, answer, confront, shoot, react).
- **Subject role**: Responder.
- **Verb senses**: face (1 — confront a situation), respond (1), answer (1), confront (1/3), shoot (1 — peripheral), react (1).
- **VN classes**: confront-98 (43), respond-113 (6), reciprocate-112 (5).
- **Frames**: Transitive; `respond to` PP.
- **NOT**: Request (Request initiates; Response reacts). Not Joint_Statement (JS is symmetric; Response is directional-back).
- **Croft/Kalm consulted**: No.

### Selling (50 ex, 5 verbs)
- **Realm**: Social (Possession cluster).
- **Event type**: Seller transfers goods to a buyer in exchange for money.
- **Subject role**: Seller.
- **Verb senses**: sell (1/5), auction (1), peddle (1), retail (1/2), hawk.
- **VN classes**: give-13.1 (16), NP (20).
- **Frames**: Transitive with goods; metonymic goods-as-subject ("books sell well").
- **NOT**: Buying (opposite agent role). Not Transfer_of_Possession (no commerce frame). Not Future_Having (no prospective grant).
- **Croft/Kalm consulted**: No.

### Sending (69 ex, 6 verbs)
- **Realm**: Physical (Motion cluster — dispatch).
- **Event type**: Agent dispatches a theme to a destination without accompanying (send, transport, export, import, return, deliver).
- **Subject role**: Sender.
- **Verb senses**: send (1/3), transport (1), export (1), import (1), return (2 — send back), deliver (5 — convey).
- **VN classes**: send-11.1 (58).
- **Frames**: Ditransitive / `send X to Y`.
- **NOT**: Carrying (Carrying entails agent co-motion; Sending does not). Not Pick_Up_and_Drop_Off (POD is the delivery endpoint; Sending is the dispatch act).
- **Croft/Kalm consulted**: No.

### Statement (73 ex, 6 verbs)
- **Realm**: Social (Communication cluster — assertive).
- **Event type**: Agent asserts or reports a proposition (say, talk, comment, declare, claim, report).
- **Subject role**: Speaker.
- **Verb senses**: say (1), talk (1), comment (1), declare (1), claim (1), report (1).
- **VN classes**: say-37.7 (48), lecture-37.11 (7), talk-37.5 (4).
- **Frames**: Transitive with clausal complement; direct/indirect quotation.
- **NOT**: Communicate (Communicate is directed transfer with explicit recipient; Statement can be monologic). Not Joint_Statement (JS is reciprocal). Not Request (Request is directive).
- **Croft/Kalm consulted**: No.

### Throwing (100 ex, 6+ verbs)
- **Realm**: Physical (Motion cluster — propulsion).
- **Event type**: Agent propels a theme through the air via impulse (fire, throw, launch, kick, discard, hit).
- **Subject role**: Thrower/Propeller.
- **Verb senses**: fire (1 — propel projectile), throw (1), launch (1/2), kick (kick-v 6/9 — propel by foot), discard (1), hit (hit-v 1/2/3).
- **VN classes**: throw-17.1 (52).
- **Frames**: Transitive + direction/goal PP.
- **NOT**: Sending (Sending is typically non-projectile, goal-directed dispatch; Throwing is impulse-based propulsion). Not Contact (Contact is bounded touching; Throwing's contact is mediated by projectile).
- **Croft/Kalm consulted**: No.

### Transfer_of_Possession (34 ex, 6 verbs)
- **Realm**: Social (Possession cluster — coercive).
- **Event type**: Agent takes possession involuntarily or coercively from a source (steal, rob, extort, confiscate, ply, compensate).
- **Subject role**: Taker (or Compensator in the compensation sub-frame).
- **Verb senses**: steal (1), rob (2), extort (1), confiscate (1), ply (1), compensate (2 — pay back).
- **VN classes**: steal-10.5 (20), equip-13.4.2 (6), rob-10.6.4 (4).
- **Frames**: Transitive + `from` PP.
- **NOT**: Dynamic_Possession (DP is volitional non-commercial; ToP is coercive/illicit). Not Buying (no exchange transaction).
- **Croft/Kalm consulted**: No.

### Vehicular_Motion (74 ex, 6 verbs)
- **Realm**: Physical (Motion cluster — vehicle-mediated).
- **Event type**: Agent or vehicle traverses space using a vehicle (ferry, paddle, ride, sail, cruise, navigate).
- **Subject role**: Vehicle-operator or Vehicle itself.
- **Verb senses**: ferry (1), paddle (1), ride (1/3), sail (1), cruise (1/2), navigate (1).
- **VN classes**: drive-11.5 (26), nonvehicle-51.4.2 (26), vehicle-51.4.1 (15).
- **Frames**: Intransitive + path; transitive for `ferry/paddle X` (carry by vehicle).
- **NOT**: Motion (Motion is self-powered displacement; VM requires vehicle/mode). Not Carrying (Carrying foregrounds theme-transport; VM foregrounds vehicle-traversal).
- **Croft/Kalm consulted**: No.

---

## Shared-Verb Boundaries

Each entry below records a verb lemma appearing in ≥2 Situations with distinct senses or frames that separate them. Resolutions cite ON senses or VN classes where available. Pairs where examples do not cleanly resolve are flagged in the next section.

### `look`: Intention(22) vs. Perception_(exp._subj.)(11) vs. Perception_(stim._subj.)(15)
- **Intention**: `look for` / `look to V` → ON sense 1 ("I'm looking for the apprentice"). Seeking/searching.
- **Perception_(exp._subj.)**: `look at` → ON sense 1 ("Jay, look at that sign."). Directed gaze.
- **Perception_(stim._subj.)**: `look Adj` → ON sense 2 ("He looks tired."). Copular-stimulus.
- **Discriminating test**: Complement type — `for` PP vs. `at` PP vs. bare Adj/clause.
- **Cross-realm**: No (all Mental).
- **Croft/Kalm consulted**: Yes (Kalm 2022 disambiguates look-at vs. look-for).

### `cut`: Hurt(12) vs. Cause_Change_of_State(11) vs. Cause_Creation(8) vs. Motion(6) vs. Change_of_State(2) vs. Incremental(1)
- **Hurt**: "Tessa cut herself" — injury-focused, reflexive typical.
- **Cause_Change_of_State**: "Carol cut the bread" — portioning/severing, result state.
- **Cause_Creation**: "cut a record" — produce a new entity (figurative extension).
- **Motion**: "The boat cut through the water" — traverse cleanly.
- **Change_of_State**: uncaused "the cloth cut easily" (middle).
- **Discriminating test**: Argument structure + world knowledge of theme — body part/person → Hurt; consumable/object → CCoS; abstract/artifact → CCrx; path PP → Motion.
- **Cross-realm**: Yes (Physical→Social for metaphorical cuts).
- **Croft/Kalm consulted**: No (examples resolve).

### `learn`: Learning(25) vs. Discovery(24)
- **Learning**: ON sense 1 — study ("Rhoda learned from an old book"). Process-focused.
- **Discovery**: ON sense 2 — come-to-know ("we learned a lot tonight"). Outcome-focused.
- **Discriminating test**: ON sense annotation is decisive. Clausal complement ("learned that X") → Discovery; `learn from/about N` as extended study → Learning.
- **Cross-realm**: No (both Mental).
- **Croft/Kalm consulted**: Yes.

### `raise`: Pick_Up_and_Drop_Off(14) vs. Cause_Change_of_State(2) vs. Cause_and_Effect(2) vs. Cause_Incremental(1) vs. Existence(1) vs. Form(1)
- **Pick_Up_and_Drop_Off**: ON sense 2 — lift physically ("raised my head"). Physical elevation.
- **Cause_and_Effect**: ON sense 3 — bring up / cause ("raise it with the Russian government"). Abstract engendering.
- **Cause_Change_of_State**: raise temperature/quality (increase, scalar CoS).
- **Form/Existence**: "raise a family", "raise crops" — developmental.
- **Discriminating test**: Concrete physical theme + upward path → POD; abstract theme + "with/before X" → C&E; scalar → CCoS.
- **Cross-realm**: Yes.

### `order`: Buying(15) vs. Request(11) vs. Dynamic_Possession(3)
- **Buying**: ON sense 2 — place a commercial order ("ordered pizza"). Theme = goods.
- **Request**: ON sense 1 — command/demand ("judge ordered the plaintiff to return the money"). Theme = action.
- **Dynamic_Possession**: order in a possession-change sense (peripheral).
- **Discriminating test**: Theme type — concrete goods → Buying; infinitival/action → Request.
- **Cross-realm**: No (both Social).

### `hire`: Cause_Membership(23) vs. Dynamic_Possession(2) vs. Buying(1)
- **Cause_Membership**: "he's hired liberals" — bringing into organization.
- **Dynamic_Possession/Buying**: peripheral "hire a car" (rent). Commercial.
- **Discriminating test**: Theme animacy — person → CM; object/service → DP/Buying.

### `hope`: Desire(14) vs. Intention(69)
- **Desire**: ON sense 1 — want/wish ("I hope it's true"). Stative wish.
- **Intention**: ON sense 1 — aim at future ("I would hope so", "hoping to find direction"). Action-directed.
- **Discriminating test**: Complement — bare clause / that-clause → Desire; `hope to V` (infinitival) or goal-pursuit → Intention.
- **Croft/Kalm consulted**: Yes.

### `hoist`: Pick_Up_and_Drop_Off(13) vs. Carrying(6) vs. Cause_Incremental(1)
- **POD**: ON sense 2 — heave upward to endpoint.
- **Carrying**: ON sense 1 — carry upward (accompanying).
- **Discriminating test**: Endpoint-focus → POD; trajectory-focus → Carrying.

### `take`: Measurement(13) vs. Carrying(10) vs. Dynamic_Possession(3)
- **Measurement**: ON sense 3 — require ("it takes three months").
- **Carrying**: ON sense 4 — convey ("took the books to the library").
- **Dynamic_Possession**: take possession of ("take them").
- **Discriminating test**: Subject = measured-entity → Measurement; subject = agent + path → Carrying; subject = agent + theme → DP.

### `bake`: Cause_Change_of_State(4) vs. Cause_Creation(2) vs. Change_of_State(2)
- **CCoS**: "baked the potatoes" — transform existing food.
- **CCrx**: "bake a cake" — produce new entity.
- **CoS**: middle "the potatoes baked" — uncaused.
- **Discriminating test**: Theme existence pre-event (CCoS) vs. created (CCrx); voice (CoS).

### `burn`: Hurt(11) vs. Cause_Change_of_State(3) vs. Emission(2)
- **Hurt**: "burn yourself" — injury.
- **CCoS**: "burned down the building" — destruction.
- **Emission**: "the torch burned" — light emission.
- **Discriminating test**: Theme animacy → Hurt; destruction result → CCoS; intransitive + light → Emission.

### `leave`: Future_Having(6) vs. Motion(6) vs. Cause_Change_of_State(1)
- **Future_Having**: "left him the house in her will" — bequeath.
- **Motion**: "I left the room" — depart.
- **Discriminating test**: Theme + beneficiary (ditransitive) → FH; path/source → Motion.

### `kick`: Throwing(9) vs. Carrying(7) vs. Existence(3) vs. Incremental(2)
- **Throwing**: ON sense 6 — propel ("kicking your father in the pants"). Impulse.
- **Carrying**: ON sense 9 — carry by foot (peripheral).
- **Existence**: ON sense 1/5 — "kick around" = exist idly.
- **Discriminating test**: Goal/target → Throwing; path/carry → Carrying; idiomatic/locative → Existence.

### `put`: Cause_Incremental(9) vs. Cause_Membership(2) vs. Emotion_(stim. subj.)(1) vs. Ingestion(1)
- **Cause_Incremental**: "Put away your toys" — location into container.
- **Cause_Membership**: "put him on the committee" — place into role.
- **Discriminating test**: Theme = object → CInc; theme = person + role PP → CM.

### `form`, `develop`, `grow`, `shape`: Form vs. Cause_Creation vs. Change_of_State vs. Location
- **Form**: cultivation/assembly ("form a circle", "cultivate crops").
- **Cause_Creation**: when a discrete artifact results.
- **Change_of_State**: intransitive growth ("the company grew").
- **Location**: "the river forms the boundary" — positional.
- **Discriminating test**: Subject animacy/agency; theme concreteness; result-entity discreteness.

### `goad`: Aggression(6) vs. Induction(11)
- **Aggression**: "goad him" as hostile needling without behavior-change goal.
- **Induction**: "goad you into an argument" — behavior-change target (infinitival complement `into V-ing`).
- **Discriminating test**: Presence of purposive complement → Induction.
- **Croft/Kalm consulted**: No.

### `manipulate`: Induction(6) vs. Manipulation
- **Induction**: "manipulate the subconscious" — target = person/mind.
- **Manipulation**: would target object (though in this dataset Manipulation's top verb is `use`, and `manipulate` is not in Manipulation's top-6 — so the split is clean in data).
- **Discriminating test**: Target animacy.

### `meet`: Reciprocal(31)
- Singleton-owned lemma; no cross-situation ambiguity.

### `agree`: Joint_Statement(65)
- Singleton-owned lemma.

### `sell`: Selling(19)
- Singleton-owned lemma in the pos data.

### `pay`: Payment(71)
- Singleton-owned lemma.

### `reek`: Emission(5) vs. Perception_(stim._subj.)(15)
- **Emission**: reek-v 2 — "bodies reek" = emit smell.
- **Perception_(stim._subj.)**: reek-v 1 — "reeks of corruption" = smells-like (copular).
- **Discriminating test**: ON sense is decisive; syntactic frame (`V of X` copular → PSS; bare intransitive emitting → Emission).
- **Note**: Many real sentences leave the perceiver implicit ("This reeks of corruption"). When a perceiver is pragmatically inferable even if not syntactically expressed, and the verb takes a predicative complement or *of*-phrase describing a quality rather than a substance, treat as Perception_(stim._subj.). Reserve Emission for cases where the verb describes physical emanation of a substance/sound/light with no quality predication.

### `control`: Enforcement(53)
- Singleton-owned in Enforcement (though `control` appears once in Manipulation too; handled by frame).

### `wear`: Constrain(65)
- Singleton-owned lemma (no cross-Situation contamination).

### `pull`: Carrying(6) vs. Manipulation(3) vs. Dynamic_Possession(2) vs. Incremental(2)
- **Carrying**: "pull a cart" — conveyance.
- **Manipulation**: "pull a lever" — operate an instrument.
- **Dynamic_Possession**: idiom.
- **Discriminating test**: Theme = conveyed object with path → Carrying; theme = instrument → Manipulation.

### `collect`: Dynamic_Possession(5) vs. Incremental(2) vs. Change_of_State(1) vs. Pick_Up_and_Drop_Off(1)
- **Dynamic_Possession**: "collect evidence" — accumulate/receive.
- **Incremental**: distribution across ground.
- **Discriminating test**: Theme type and aspectual reading.

### `drive`: Pick_Up_and_Drop_Off(2) vs. Manipulation(1) vs. Throwing(1) vs. Vehicular_Motion(1)
- **POD**: "drive X to Y" (convey).
- **Vehicular_Motion**: "drive across town" (self-motion).
- **Manipulation**: "drive a nail" (instrument).
- **Throwing**: "drive a ball" (propel).
- **Discriminating test**: Theme/instrument — projectile vs. vehicle vs. nail.

### `beat`: Contact(4) vs. Aggression(3) vs. Existence(1)
- **Contact**: "beat the rug" — repeated strike (cleaning/contact).
- **Aggression**: "beat him" — assault.
- **Discriminating test**: Theme animacy → Aggression; object → Contact.

### `shoot`: Cause_Change_of_State(2) vs. Throwing(2) vs. Response(1)
- **CCoS**: "shot him dead" — destruction.
- **Throwing**: "shoot a ball" — propel.
- **Discriminating test**: Result state.

### `serve`: Participation(15)
- Singleton-owned.

### `break`: Cause_Change_of_State(2) vs. Location(2) vs. Change_of_State(1) vs. Hurt(1) vs. Incremental(1)
- **CCoS**: "broke the window" — destroy.
- **CoS**: "the window broke" — middle.
- **Discriminating test**: Voice/agency.

### `change`: Change_of_State(3) vs. Replacement
- **CoS**: "London weather changed to cloudy" — state property change.
- **Replacement**: would use `change X for Y` — not in Change_of_State's examples.
- **Discriminating test**: `change X to/for Y` alternation.

### `close` / `open`: Cause_Change_of_State vs. Change_of_State vs. Existence
- Middle/causative alternation.

### Pursuit vs. Motion
- **Why confusable**: Physical pursuit (chase, follow) is a motion event with agent-subject.
- **Discriminating test**: Is a second co-moving entity (quarry/target) evoked or entailed? Co-motion toward/after a target → Pursuit; autonomous motion along a path → Motion.
- **A example** (Pursuit): "The detective trailed the suspect through the alley."
- **B example** (Motion): "She walked through the alley."

### Pursuit vs. Desire
- **Why confusable**: Long-class verbs (long for, yearn for) use the same *for*-oblique frame as search verbs.
- **Discriminating test**: Is the subject actively directing effort toward the target (searching, investigating) → Pursuit; or is the subject in a stative mental state of wanting → Desire?
- **A example** (Pursuit): "Detectives hunted for the missing weapon."
- **B example** (Desire): "She longed for a quiet life."

### Limitation vs. Enforcement
- **Why confusable**: Both in Control cluster; both restrict what another entity can do.
- **Discriminating test**: Does the causer restrict the scope/extent of action without naming a specific prevented action → Limitation; or does the causer compel or prevent a specific action → Enforcement?
- **A example** (Limitation): "The regulation limits campaign donations to $2,000."
- **B example** (Enforcement): "The court forbade him from contacting the witness."

### Concealment vs. Incremental
- **Why confusable**: Both involve mereological theme-ground motion (figure moves to/from ground). Now in same cluster.
- **Discriminating test**: Is a perceiver evoked whose view is blocked? Perceiver-not-seeing as result → Concealment; no perceiver, just spatial accretion/removal → Incremental.
- **A example** (Concealment): "She hid the letter under the mattress."
- **B example** (Incremental): "She spread butter on the toast."

### Constrain vs. Capacity
- **Why confusable**: Both use *hold, contain*; both describe spatial co-location.
- **Discriminating test**: Is the subject an agent actively constraining a theme's motion (holding, grasping) → Constrain; or is the subject a container/structure whose inherent property is to accommodate contents → Capacity?
- **A example** (Constrain): "He held the dog by the collar."
- **B example** (Capacity): "The auditorium holds 500 people."

### Aggression vs. Induction
- **Why confusable**: *bully* appears in both; both involve volitional social force on a person.
- **Discriminating test**: Does the action aim to cause the victim to *do* something (bully into X, with infinitival/gerund complement) → Induction; or is the action hostile without requiring a subsequent action from the victim → Aggression?
- **A example** (Aggression): "The older kids bullied him every day."
- **B example** (Induction): "They bullied him into signing the confession."

---

## Flagged Ambiguities

These are pairs where the examples alone do not cleanly resolve which Situation owns a given sentence, AND consultation of Croft/Kalm did not fully disambiguate. I note the gap rather than forcing a resolution.

1. **`hope`: Desire(14) vs. Intention(69)** — Both Situations annotate `hope` at ON sense 1. The putative split (Desire = static wish; Intention = goal-directed hoping) is frame-based (complement type), but several existing rows in Intention lack an infinitival ("I would hope so /."), blurring the boundary. Action-item: Josh may want to re-audit `hope` rows between these two files.

2. **`learn` ON sense 1 "study"**: Currently split between Learning (25 rows, primarily sense 1) and Discovery (24 rows, primarily sense 2). Some Learning rows with minimal context ("learn-v 1") could belong to Discovery if the intended reading is come-to-know rather than study. Action-item: Re-check low-context `learn` examples.

3. **`goad`: Aggression(6) vs. Induction(11)** — Same ON sense 1 in both. Discriminating test is complement ("goad into V-ing" → Induction; bare "goad him" → Aggression), but several rows in each file are genuinely ambiguous.

4. **`agree` sense 3 (Joint_Statement)**: "They agreed to X" can be interpreted as `agree = consent` (one-way speech act → Statement) OR `agree = reach consensus` (reciprocal → Joint_Statement). The sense distinction (1 vs 3) is annotated but not always discriminating in minimal sentences.

5. **`cost` in Measurement vs. Charge** — `cost` appears in both. Measurement: "the book costs $10" (intrinsic value reporting). Charge: "it cost me a clay pot" (imposed sacrifice/debit). Frame is similar (X cost Y Z); the distinguishing feature is dative/beneficiary ("cost me"/"cost him") and the interpretation of Y as loss-event recipient vs. measured-entity. The line is subtle.

6. **`kick` in Existence** — Three rows ("kick around", idiomatic). Could be argued for Motion or just noise. The idiom is conventional-existential, so the classification is defensible but marginal.

7. **`lead` in Pursuit** — `lead the troops into battle` vs. Induction `lead X to V`. Discriminating test is physical vs. abstract target, mostly clean but borderline cases exist.

---

## Phase 0 Summary

```
Total Situations:         62
Total shared-verb pairs:  190 (unique lemmas shared across ≥2 Situations)
Resolved by examples:     ~160 (clear ON sense or frame split in pos data)
Resolved by Croft/Kalm:   ~7 (pairs consulted; see per-boundary notes above)
Unresolved (flagged):     7 (listed in Flagged Ambiguities)
```

STOP. Awaiting Josh's review of this scope map.
