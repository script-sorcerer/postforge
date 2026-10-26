# Postforge

Postforge is a content and marketing Office. Its agents find post ideas in a Project's work, put them to the owner for review, and turn the approved ones into ready-to-publish Posts. The owner can also bring a Topic of their own.

## Language

### Office and roles

**Office**:
The set of agent Roles plus the shared memory they work from. The owner directs it and approves its output.
_Avoid_: pipeline, agency, bot

**Role**:
One agent job in the Office with a fixed responsibility, for example Scout, Writer or Editor.
_Avoid_: agent (when the job is meant), worker

**Scout**:
The Role that reads a Project's Source material and proposes Topics.
_Avoid_: researcher, ideator

**Writer**:
The Role that turns an approved Topic into Drafts.
_Avoid_: copywriter, author

**Editor**:
The Role that scores a Draft against a fixed checklist built on the Voice guide and the Channel rules, and writes specific remarks; the Writer revises from them.
_Avoid_: reviewer, critic

**Packager**:
The Role that assembles a Publish package and checks its Attachments against the Channel rules.
_Avoid_: publisher, formatter

**Producer**:
The Role that builds a Composition from a ready Video script and the Owner's Attachments and renders the video (ADR 0002).
_Avoid_: video editor, renderer, animator

**Owner**:
The human who approves Topics, edits Drafts and publishes Posts.
_Avoid_: user, reviewer

### Inputs

**Project**:
A product the Office markets, described by its repository, its pitch and its audience. traffic_jam is the first Project.
_Avoid_: client, product

**Source material**:
The evidence the Scout reads, local and remote: git history, issues with their discussion, design docs, ADRs, other files in the Project's folder, and the Owner notes. The Office only reads it, never changes it.
_Avoid_: input, context, raw data

**Trend scan**:
The Scout's dated note on what is current outside the Project: hot discussions, meme formats, news and calendar hooks. It goes stale after two weeks.
_Avoid_: trend report, research

**Owner notes**:
Free-form observations from the Owner that exist nowhere in the Project's code or docs.
_Avoid_: memo, journal

**Voice guide**:
The written rules for tone, wording and what must never be published.
_Avoid_: brand book, style sheet

**Fact sheet**:
The Office's record of what a Project is, who it is for and what has already been shown publicly.
_Avoid_: project brief, profile

**Vault**:
The Office's shared memory: the notes that Roles and the Owner both read and write.
_Avoid_: knowledge base, database, memory bank

### Content

**Topic**:
One proposed story for a post, with its angle, audience and target Channels. The Owner approves, rejects or parks it.
_Avoid_: idea, pitch, suggestion

**Owner Topic**:
A Topic the Owner writes by hand and approves at once, outside any Digest. Every Role after the Scout treats it like a Scout Topic.
_Avoid_: manual topic, custom idea

**Parked Topic**:
A Topic the Owner set aside for later, neither approved nor rejected.
_Avoid_: backlog item, deferred

**Rubric**:
A recurring kind of story that Topics belong to, for example Devlog or Design decision. Rubrics keep a feed varied.
_Avoid_: category, pillar, series

**Digest**:
A batch of Topics the Scout delivers for the Owner to review in one sitting.
_Avoid_: summary, report, inbox

**Draft**:
A version of a post for one Channel that the Owner has not yet marked ready. One approved Topic yields one Draft per Channel.
_Avoid_: version, candidate

**Pass**:
One focused step of the Writer's work on a Draft: Angle, Hooks, Draft, Voice, Humanize or Channel fit.
_Avoid_: iteration, stage, round

**Owner edit**:
A change the Owner makes to a Draft, by hand or by prompt. Owner edits always win over the Editor's.
_Avoid_: correction, feedback

**Video script**:
A Draft for the Shorts Channel: the caption, the title and a beat table of timed footage, on-screen text and narration. The Writer writes it; the Producer renders it.
_Avoid_: storyboard, video post

**Composition**:
The HyperFrames source the Producer builds from a Video script: an HTML project under `Attachments/video/` that renders to the Post's video. Committed; its render is not.
_Avoid_: project file, timeline, scene file

**Adaptation**:
A Draft in a second language, rewritten for that language's readers rather than translated word for word.
_Avoid_: translation, localization

**Post**:
The final, ready-to-publish content for one Channel, with its Attachments.
_Avoid_: publication, entry

**Publish package**:
A Post with everything the Owner needs to publish it by hand: final text, checked Attachments in order, and alt text.
_Avoid_: bundle, export

**Channel**:
One place a Post goes out: X, Reddit, LinkedIn, Shorts (one 9:16 video for YouTube Shorts and TikTok) or Article (long-form: dev.to for English, Habr for Russian Adaptations).
_Avoid_: platform, network

**Shot list**:
The Office's description of the footage a Topic needs, for the Owner to capture. A Video script's beats name these files.
_Avoid_: storyboard, media request

**Attachment**:
An image or video file that the Owner supplies and a Post carries.
_Avoid_: media, asset, file
