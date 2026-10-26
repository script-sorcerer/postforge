---
kind: fact-sheet
status: proposed
project: "[[traffic_jam]]"
public_name: ""          # the game's public name; empty until the Owner announces one
shown_publicly: []       # one item per thing already shown in public: "<date> <channel>: <what>"
sources:                 # repository-relative paths you drew on
  - CONTEXT.md
  - AGENTS.md
  - Docs/CityGeneration.md
  - Docs/GameCamera.md
  - Docs/MobileHUD.md
  - Docs/DistrictVisuals.md
  - Docs/ScenarioDesign.md
  - Docs/adr/0010-intersection-modal-presentation.md
  - Docs/adr/0012-logical-flow-drives-traffic-presentation.md
  - Docs/adr/0015-procedural-city-generator.md
  - Docs/adr/0016-level-number-derives-the-generated-level.md
  - Docs/adr/0017-roads-are-a-subgraph-of-the-lattice.md
  - Docs/adr/0018-rounded-bends-in-the-road-renderer.md
phases:                  # the campaign in order; starts is an ISO date, or empty until the Owner sets it
  - name: Pre-reveal
    starts: 2026-10-27
    makes_public: "The core loop and devlog of 'my traffic puzzle game', without its name, store page or dates"
  - name: Reveal
    starts:
    makes_public: "The public name, the store page and the pre-registration link"
  - name: Launch
    starts:
    makes_public: "Release date, price, platforms, game modes beyond the Day level, the daily challenge, the campaign's scale"
---

# traffic_jam: Fact sheet

## What it is
A mobile traffic puzzle game for landscape phones and tablets on iOS and Android (Docs/MobileHUD.md; Mac and the Unreal Editor are development hosts only). It is built in Unreal Engine with C++.

Core loop: a city of roads and districts fills with traffic between districts over one in-game day. The player does not draw roads or set traffic lights. They station a traffic officer at an intersection and choose the officer's pose, which decides which movements may go. If traffic waits too long, the city's dissatisfaction rises; at 100 the level fails. Better flow lets it recover.

What makes it different: control by officer poses instead of traffic lights, and cities built by a generator from the level number, so every player who opens level N meets the same city and the same traffic.

## Who it is for
- Mobile puzzle players.
- Indie and solo game developers (the Project note's second audience).
- People curious about building games with AI agents (the Project note's third audience).

## Key facts
- **Level scenario**: one playable day from 04:00 until 02:00 the next day over seven minutes of active play (CONTEXT.md).
- **District**: a place with a kind and a footprint of cells. An ordinary (Day) level has at least two Residential, one Commercial, one Park and one Entertainment district, with Industrial among the extra kinds (Docs/CityGeneration.md). PoliceStation and Hospital also exist as kinds.
- **Intersection**: where roads meet and a traffic officer can stand. Junctions are three-way or four-way. Players see them labelled "Junction N".
- **Officer pose**: Uncontrolled, StopAll, SideFlow or DirectTurn. A permitted movement with room ahead flows through without stopping; under Uncontrolled each driver hesitates briefly at the line (default 1.0 s); a forbidden movement holds (ADR 0012).
- **Pose panel**: a panel at the bottom of the screen; the city stays visible and play does not pause while it is open. Each pose shows a top-down pose diagram that turns with the camera. Pose badges above intersections show the current pose (ADR 0010).
- **Dissatisfaction**: the city's recoverable measure of traffic frustration, 0 to 100. Reaching 100 fails the level. The first two seconds of any stop cost nothing (waiting allowance).
- **Scheduled event**: an optional event announced at level start, such as a concert that brings extra traffic.
- **Incident / Accident**: a local disruption, resolved when police and an ambulance arrive in time and finish their service; otherwise it clears with a failure outcome.
- **Cars**: every car that takes space on the road is drawn. Cars alone show how full a road is; there are no tint strips or overlays (owner decision of 2026-10-16, CONTEXT.md).
- **Roads**: two-way or one-way, lanes under right-hand traffic, 90° bends drawn as rounded curves (ADR 0018). City exits sit at the edge of the city.
- **Generated level**: a level built at start from its level number alone, identical for every player and every retry (ADR 0016). A few numbered tutorial levels are baked from the same generator.
- **Camera**: an isometric perspective view; one finger pans, pinch zooms, twist rotates, a two-finger vertical drag tilts. No camera buttons (Docs/GameCamera.md).

## Where it stands
- In development since 2026-06-30; about 465 commits by one developer. About 150 commits carry a co-author line for an AI coding agent; the repository holds agent instructions (AGENTS.md).
- Works today in the Editor: Level01 (hand-made) with officers, poses, dissatisfaction and failure, the concert, accidents with police and ambulance, and continuous individual car traffic.
- An iPhone build and launch workflow exists; the mobile HUD was revised after testing on an iPhone in October 2026.
- The procedural city generator, the level-number progression and rounded bends were built on 2026-10-25 and 2026-10-26; their tickets are still open.
- Not built yet: event status text in the in-play HUD, rewards, final art.

## Not public yet
- [Reveal] The working name "traffic_jam" / "Traffic Jam". Until `public_name` is set, say "my traffic puzzle game".
- [Reveal] Store plans and the pre-registration.
- [Launch] Planned game modes beyond the ordinary Day level: Evacuation (residents leave within a time limit) and Official visit (an escort between an Airport and City Hall), and the Shelter, CityHall and Airport district kinds made for them.
- [Launch] The daily challenge (the same generated city for every player on a date).
- [Launch] Campaign scale and difficulty curve: the plan for 1,000 to 10,000 generated levels and its formula.
- [Launch] Release dates, prices, and whether Android ships at launch.
- [never] Internal tools: developer console commands, the Gameplay Debugger, the repository, its issues and pull requests.

## Open questions for the Owner
1. Which of the core loop may be shown before an announcement: officer poses, generated cities, dissatisfaction, the concert, accidents with police and ambulance?
2. Is there a public name, and has the working name ever been used in public?
3. What has already been posted, where and when (for `shown_publicly`)?
4. The generator, progression and rounded-bend work (2026-10-25 and 2026-10-26) sits on a branch, not on main, and its tickets are open. Is it accepted, or may it still change?
5. Is Android a launch platform, or iOS first? Has the game run on an Android device?
6. Docs/ScenarioDesign.md says rewards are deferred. Is there a star or score system to mention?
7. May the AI-agent workflow be named in posts, and which tools (the repository holds instructions for several)?
8. The game is landscape only. For Shorts (9:16), should footage be a crop of landscape captures, or a portrait capture window?
9. Are the Phases right (Pre-reveal from 2026-10-27, Reveal, Launch), and does each "Not public yet" item sit in the Phase that lifts it? Set Reveal's `starts` once the name and store page have a date.
