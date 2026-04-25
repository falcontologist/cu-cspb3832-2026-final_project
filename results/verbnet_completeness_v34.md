# VerbNet Completeness Audit

Workbook: `Situation Shapes Workbook - VN Verb Mappings.csv`  
Reference: local VerbNet at `/Users/joshfalconer/Documents/Linguistic data/verbnet/verbnet3.4`.

NFKC normalization folded 299 workbook class IDs that contained Unicode ligatures (`ﬁ`, `ﬀ`, `ﬂ`) into their canonical forms. Examples: `suﬀocate-40.7`→`suffocate-40.7`, `suﬀocate-40.7`→`suffocate-40.7`, `suﬀocate-40.7`→`suffocate-40.7`.

## Summary

### Class-level coverage

- NLTK VerbNet top-level classes: **329**
- Workbook VN classes: **248**
- Classes covered in both: **248** (75.4% of NLTK)
- Classes in NLTK but missing from workbook: **81**
- Classes in workbook but not in NLTK: **0**

### Verb-level coverage

- NLTK VerbNet verbs (across all classes): **4,580**
- Workbook verbs: **4,189**
- VerbNet verbs covered: **4,189** (91.5% of VerbNet)
- VerbNet verbs missing from workbook: **391**
- Workbook verbs not in any NLTK VerbNet class: **0** (possibly added from other sources, paraphrases, or typos)

## Classes in NLTK VerbNet but missing from the workbook

- **abide_by-93.2** (7 verbs): abide_by, adhere_to, follow, heed, keep_to, obey, observe
- **accept-77.1** (4 verbs): accept, buy, encourage, understand
- **acquiesce-95.1** (12 verbs): accede, acquiesce, bow, capitulate, consent, defer, fall, give_in, give_way, submit ... (12 total)
- **act-114** (13 verbs): act, action, carry_out, carry_through, cause, conduct, do, engage_in, execute, fulfill ... (13 total)
- **addict-96** (6 verbs): addict, bias, dispose, incline, predispose, slant
- **adjust-26.9** (9 verbs): accommodate, adapt, adjust, assimilate, conform, fit, gear, readapt, readjust
- **admit-64.3** (8 verbs): admit, allow, hail, include, let, permit, receive, welcome
- **adopt-93.1** (4 verbs): adopt, assume, take, take_on
- **allow-64.1** (8 verbs): allow, approve, authorize, endorse, okay, permit, sanction, tolerate
- **amalgamate-22.2** (51 verbs): affiliate, alternate, amalgamate, associate, coalesce, coincide, compare, confederate, conflate, confuse ... (51 total)
- **avoid-52** (11 verbs): avoid, boycott, circumvent, dodge, duck, elude, eschew, evade, forgo, shun ... (11 total)
- **become-109.1** (11 verbs): become, come, come_out, end_up, fall, get, go, grow, leave, turn ... (11 total)
- **begin-55.1** (12 verbs): begin, commence, go_on, proceed, recommence, repeat, resume, set_about, set_out, start ... (12 total)
- **benefit-72.2** (2 verbs): benefit, profit
- **berry-13.7** (30 verbs): antique, berry, birdnest, blackberry, clam, crab, fish, fowl, grouse, hawk ... (30 total)
- **body_motion-49.2** (4 verbs): extend, hold, reach, stretch
- **calibratable_cos-45.6.1** (37 verbs): appreciate, build, climb, decline, depreciate, die, dip, dive, drop, dwindle ... (37 total)
- **care-88.1** (4 verbs): care, mind, wonder, worry
- **caring-75.2** (9 verbs): attend, babysit, care, look_after, look_out, manage, mind, tend, wait_on
- **caused_calibratable_cos-45.6.2** (14 verbs): advance, balloon, build-up, commute, cut, decrease, diminish, increase, lower, move ... (14 total)
- **complete-55.2** (5 verbs): accomplish, achieve, bring-off, complete, pull-off
- **comprise-107.2** (9 verbs): compose, comprise, consist_of, constitute, contain, encompass, form, make, make_up
- **conduct-111.1** (8 verbs): conduct, give, head, hold, host, run, spearhead, throw
- **conspire-71** (8 verbs): ally, collaborate, collude, conspire, machinate, partner, scheme, team_up
- **continue-55.3** (1 verbs): continue
- **convert-26.6.2** (19 verbs): advert, change_over, come_around, convert, fall, get, get_around, get_down, go_back, move_over ... (19 total)
- **cope-83** (6 verbs): cope, deal, get_by, get_through, grapple, manage
- **dedicate-79** (3 verbs): commit, dedicate, devote
- **delay-53.3** (5 verbs): defer, delay, postpone, procrastinate, stall
- **discourage-64.5** (9 verbs): deter, discourage, dissuade, hamper, hinder, impede, inhibit, obstruct, restrain
- **disfunction-105.2.2** (5 verbs): die, go_down, go_off, go_out, poop_out
- **empathize-88.2** (4 verbs): commiserate, empathize, identify, sympathize
- **enforce-63** (3 verbs): control, enforce, impose
- **establish-55.5** (32 verbs): arrange, bring, bring_about, constitute, constitutionalize, devise, establish, fake, feign, format ... (32 total)
- **exchange-13.6.1** (5 verbs): barter, change, exchange, swap, trade
- **exclude-107.3** (3 verbs): exclude, omit, preclude
- **exhale-40.1.3** (9 verbs): defecate, exhale, expectorate, hemorrhage, inhale, perspire, regurgitate, urinate, whiff
- **flinch-40.5** (8 verbs): balk, cower, cringe, flinch, quail, recoil, shrink, wince
- **focus-87.1** (17 verbs): brood, center, concentrate, contemplate, converge, deliberate, dwell, fixate, focalize, focus ... (17 total)
- **forbid-64.4** (10 verbs): ban, bar, block, exclude, forbid, keep, preclude, prevent, prohibit, stop
- **free-10.6.3** (21 verbs): absolve, acquit, alleviate, break, cleanse, clear, cure, discharge, disencumber, ease ... (21 total)
- **function-105.2.1** (7 verbs): function, go, go_on, operate, perform, run, work
- **help-72.1** (8 verbs): abet, aid, assist, go, help, pull, succor, support
- **hold-15.1** (8 verbs): clasp, clutch, grab, grasp, grip, handle, hold, wield
- **involve-107.1** (5 verbs): engage, enroll, include, involve, relate
- **keep-15.2** (7 verbs): hoard, hold, keep, leave, stock, stockpile, store
- **let-64.2** (1 verbs): let
- **limit-76** (6 verbs): confine, constrain, limit, reduce, restrain, restrict
- **linger-53.1** (12 verbs): dally, dawdle, dither, equivocate, hesitate, linger, loaf, loiter, pause, potter ... (12 total)
- **matter-91** (2 verbs): count, matter
- **neglect-75.1** (10 verbs): disregard, fail, forego, forgo, ignore, leave_out, neglect, omit, overleap, overlook
- **orbit-51.9.2** (4 verbs): orbit, revolve, rotate, twirl
- **pain-40.8.1** (7 verbs): ail, bother, burn, hurt, itch, kill, pain
- **patent-101** (12 verbs): accredit, certify, copyright, credential, evidence, imitate, impersonate, license, patent, register ... (12 total)
- **play-114.2** (3 verbs): frolic, play, recreate
- **promote-102** (8 verbs): advance, boost, emphasize, encourage, further, invite, promote, underscore
- **prosecute-33.2** (15 verbs): arrest, book, bust, charge, collar, impeach, indict, nab, penalize, persecute ... (15 total)
- **rebel-71.2** (6 verbs): discriminate, legislate, protest, rebel, retaliate, sin
- **refrain-69** (4 verbs): abstain, desist, forbear, refrain
- **rely-70** (11 verbs): bank, bargain, bet, count, depend, figure, gamble, reckon, rely, take_a_chance ... (11 total)
- **resign-10.11** (16 verbs): abdicate, depart, give_up, leave, leave_office, quit, renounce, resign, retire, step_down ... (16 total)
- **risk-94** (8 verbs): bet, chance, gamble, hazard, punt, risk, venture, wager
- **rotate-51.9.1** (10 verbs): coil, curl, hook, rotate, spin, swing, turn, twirl, twist, wind
- **rush-53.2** (3 verbs): hasten, hurry, rush
- **seem-109** (12 verbs): act, appear, be, feel, keep, look, remain, seem, smell, sound ... (12 total)
- **shake-22.3** (43 verbs): affix, agglutinate, attach, band, baste, beat, bind, bond, bundle, cluster ... (43 total)
- **spend_time-104** (8 verbs): kill, lead, misspend, pass, serve, spend, use, waste
- **stop-55.4** (16 verbs): cease, close, conclude, cut, cut_off, cut_out, deactivate, discontinue, end, finish ... (16 total)
- **subjugate-42.3** (37 verbs): calm_down, choke, conquer, crush, curb, dampen, disenfranchise, enslave, gag, hush ... (37 total)
- **subordinate-95.2.1** (2 verbs): answer, report
- **succeed-74** (10 verbs): excel, fail, fall, fall_by_the_wayside, fall_off, flub, lose, manage, succeed, win
- **suspect-81** (3 verbs): accuse, condemn, suspect
- **sustain-55.6** (10 verbs): carry_on, continue, hold, keep, keep_up, leave, maintain, prolong, protract, sustain
- **terminus-47.9** (6 verbs): begin, end, lead, start, stop, terminate
- **trifle-105.3** (6 verbs): dally, diddle, fiddle, play, toy, trifle
- **try-61.1** (2 verbs): attempt, try
- **void-106** (6 verbs): annul, avoid, invalidate, nullify, quash, void
- **volunteer-95.4** (6 verbs): enlist, hire_on, offer, sign_on, sign_up, volunteer
- **weekend-56** (10 verbs): december, holiday, honeymoon, junket, overnight, sojourn, summer, vacation, weekend, winter
- **withdraw-82** (13 verbs): back_down, back_off, back_out, bow_out, chicken_out, get_away, get_out, pull_away, pull_out, retire ... (13 total)
- **work-73.2** (6 verbs): bang_away, labor, labour, plug_away, slog_away, work

## Per-class verb coverage (classes with missing verbs)

Sorted worst-covered first. Classes with all NLTK verbs already in the workbook are omitted.

| VN Class | NLTK verbs | Covered | Missing | Coverage |
|---|---:|---:|---:|---:|

(0 classes have at least one missing verb; 248 are fully covered.)

## Missing VerbNet verbs by class (full lists)

