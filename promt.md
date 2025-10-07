# Content Generation Prompts for IT Course Materials

Use these prompts to generate course materials following the established format guide.

---

## Prompt 1: loeng.md (Lecture Notes)

```
Create lecture notes (loeng.md) for [TOPIC] following these requirements:

STRUCTURE:
- Exactly ONE H1: "# [Topic Name]"
- NO time markers, emojis, or difficulty markers in H1
- After H1: metadata block with **Eeldused:** and **Platvorm:**
- First H2 MUST be "## Õpiväljundid" with 5 concrete learning outcomes
- Use Bloom's taxonomy verbs: mõistab, selgitab, eristab, võrdleb

CONTENT REQUIREMENTS:
- Platform-agnostic theory (cover multiple tools/platforms when applicable)
- Start with WHY (motivation, problem this solves)
- Then WHAT (concepts, theory)
- Then HOW (implementation overview)
- Include comparison tables where relevant
- Professional tone for vocational school adults
- Technical depth without patronizing

FORMAT:
- NO emojis anywhere
- Numbered main sections: "## 1. Section Name"
- Max 2-3 bold terms per section (first occurrence only)
- All code blocks MUST have language tags
- Professional language (no "selgita vanaisale", no childish metaphors)
- Paragraphs max 4-5 sentences

PEDAGOGICAL ELEMENTS:
- Build on prior knowledge (reference what students already know)
- Focus on understanding over memorization
- Use real industry examples
- Include "Miks on see oluline?" explanations

LENGTH: 8,000-12,000 words covering complete theory

TOPIC DETAILS:
[Provide topic, target audience, prerequisites, key concepts to cover]
```

---

## Prompt 2: labor.md (Lab Exercises)

```
Create hands-on lab exercises (labor.md) for [TOPIC] following these requirements:

STRUCTURE:
- Exactly ONE H1: "# [Topic Name] Labor"
- After H1: metadata with **Eeldused:** and **Platvorm:**
- First H2 MUST be "## Õpiväljundid" with 5 skill-based outcomes
- Use action verbs: loob, seadistab, käivitab, debugib, rakendab

CONTENT REQUIREMENTS:
- Focus on ONE platform/tool (not multiple like loeng.md)
- Step-by-step instructions that students can follow
- Each major section is a numbered task: "## 1. Task Name"
- NOT "## Samm 1" or "## Osa 1"
- Include validation checkpoints after each task
- Troubleshooting sections for common problems

FORMAT:
- NO emojis anywhere
- Sequential numbering: "## 1.", "## 2.", "## 3."
- Detailed code examples with language tags
- Expected output shown after commands
- Checklists for validation: "- [ ] Item"
- Natural time references in paragraphs ("võtab umbes 30 min")

PEDAGOGICAL ELEMENTS:
- Guided practice (student does, teacher available)
- Clear success criteria for each step
- "Validation:" sections with test commands
- Progressive complexity (simple → advanced)
- Troubleshooting guide at end

STRUCTURE TEMPLATE:
1. Setup/installation check
2. Basic operations (3-4 tasks)
3. Intermediate concepts (2-3 tasks)
4. Cleanup section
5. Kontrollnimekiri (final checklist)

LENGTH: 4,000-6,000 words, 6-8 major tasks

TOPIC DETAILS:
[Provide topic, platform choice, learning progression, common errors to address]
```

---

## Prompt 3: kodutoo.md (Homework)

```
Create homework assignment (kodutoo.md) for [TOPIC] following these requirements:

STRUCTURE:
- Exactly ONE H1: "# [Topic Name] Kodutöö: [Specific Task]"
- After H1: brief description paragraph (no metadata about "Õpiväljundid")
- Time estimate in natural language in first paragraph
- Metadata: **Eeldused:**, **Esitamine:**, **Tähtaeg:**

CONTENT REQUIREMENTS:
- Same platform as labor.md BUT different tech stack/scenario
- Requires students to APPLY knowledge in new context
- Include design thinking element (e.g., PIPELINE.md, architecture doc)
- Clear deliverables and submission format
- Grading rubric as table

FORMAT:
- NO emojis anywhere
- NO "## Kodutöö" prefix in H2 headings
- Numbered sections for tasks: "## 1.", "## 2."
- Code templates provided (not full solutions)
- Checklists: "### Kontroll Enne Esitamist"

REQUIRED SECTIONS:
1. Ülesande Kirjeldus (what to build)
2. Implementation steps (3-5 main sections)
3. Esitamine (submission requirements with checklist)
4. Refleksioon (5 questions, 2-3 sentences each)
5. Hindamiskriteeriumid (grading rubric table)
6. Boonus (optional, +10%)

REFLEKSIOON KÜSIMUSED (mandatory):
- Mis oli kõige raskem ja kuidas lahendasid?
- Milline kontseptsioon oli suurim "ahaa!" hetk?
- Kuidas kasutaksid seda tulevikus?
- Kuidas selgitaksid sõbrale, mis see tehnoloogia on?
- Mis oli kõige huvitavam osa?

LENGTH: 3,000-5,000 words

TOPIC DETAILS:
[Provide topic, different scenario from lab, deliverables, grading criteria]
```

---

## Prompt 4: lisapraktika.md (Advanced Practice)

```
Create advanced optional exercises (lisapraktika.md) for [TOPIC] following these requirements:

STRUCTURE:
- Exactly ONE H1: "# [Topic Name] Lisapraktika"
- After H1: brief description with **Eeldused:**
- NO "## Õpiväljundid" section (this is optional material)
- MAXIMUM 3 exercises total

CONTENT REQUIREMENTS:
- Advanced topics beyond lab scope but buildable in 30-45 min each
- Each exercise teaches ONE focused advanced concept
- Production-ready techniques students will use in real jobs
- Progressive difficulty: Exercise 1 (intermediate) → Exercise 3 (advanced)
- Written FOR STUDENTS (no pedagogical theory or teacher notes)

FORMAT:
- NO emojis anywhere
- NO "## Lisapraktika" prefix in H2+ headings
- Numbered main exercises: "## 1. Topic Name", "## 2. Topic Name", "## 3. Topic Name"
- Each exercise has subsections: "### 1.1 Probleem", "### 1.2 Lahendus", "### 1.3 Harjutus"
- Code examples with explanations BEFORE showing code
- All code blocks MUST have language tags

EXERCISE STRUCTURE (repeat 3 times):

### X.1 Probleem
- Explain what problem this solves
- Why the basic approach from lab isn't enough
- Real-world scenario where this matters

### X.2 Lahendus
- Show the advanced technique/solution
- Complete working code example
- Explain how it works

### X.3 Harjutus: [Descriptive Title]

**Nõuded:**
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3
- [ ] Requirement 4

**Näpunäiteid:**
- Helpful hint 1
- Helpful hint 2
- Helpful hint 3

**Testimine:** (optional)
```bash
# Commands to verify it works
```

**Boonus:**
- Optional extra challenge
- Related advanced topic
- Production consideration

END SECTION:
## Kasulikud Ressursid

**Dokumentatsioon:**
- [Relevant Doc 1](URL)
- [Relevant Doc 2](URL)

**Tööriistad:**
- **Tool Name** - description: installation/usage command

**Näited:**
- Link to examples repo

Final sentence: "Need harjutused on mõeldud süvendama teie [TOPIC] oskusi. Alustage esimesest ja liikuge järk-järgult keerulisemate poole."

PEDAGOGICAL APPROACH (don't write this in output, just follow it):
- Each exercise follows Problem → Solution → Practice pattern
- Students learn by comparing "before/after" code
- Focus on WHY technique matters, not just HOW
- Exercises build independent problem-solving skills
- NO teacher notes or pedagogical framework in student-facing content

LENGTH: 1,500-2,500 words total (500-800 words per exercise)

TOPIC DETAILS:
[Provide topic, 3 specific advanced techniques to cover, production scenarios, target skill level]
```

---

## Prompt 5: tunnikava.md (Lesson Plan)

```
Create teacher lesson plan (tunnikava.md) for [TOPIC] following these requirements:

STRUCTURE:
- Exactly ONE H1: "# Tunnikava: [Topic Name]"
- After H1: metadata with **Kestus:**, **Tase:**, **Eeldused:**, **Materjalid:**
- First H2 MUST be "## Õpiväljundid"

CONTENT REQUIREMENTS:
- Designed FOR TEACHERS (not students)
- Include pedagogical framework explanation
- Reference teaching methods and cognitive science
- Minute-by-minute breakdown of each lesson block
- Troubleshooting for common classroom issues
- Adaptation strategies (if students fast/slow)

FORMAT:
- NO emojis anywhere
- Each lesson block: "## 1. Lesson Title"
- Include: **Aeg:**, **Eesmärk:**, **Meetodid:** for each block
- Minutiplaan (0-5 min, 5-15 min, etc.)
- Kontrollnimekiri for each block
- Refleksioon prompts
- Kohandus (adaptation) notes

REQUIRED SECTIONS:
1. Õpiväljundid
2. Pedagoogiline Raamistik (cite "How People Learn" NRC 2000)
3. Õpetamismeetodid (table of methods)
4. Näpunäited Algajale Õpetajale
5. Individual lesson blocks (one per 45 min)
6. Kodutöö section
7. Viited ja Täiendav Lugemine
8. Kokkuvõte (what to do / what NOT to do)

PEDAGOGICAL PRINCIPLES:
- Prior knowledge activation
- Understanding over memorization  
- Metacognition (reflection)
- Formative assessment
- Active learning over passive lecture

EACH LESSON BLOCK INCLUDES:
- Time allocation and goals
- Minutiplaan (minute-by-minute)
- Kontrollnimekiri (success criteria)
- Kontrollküsimused (assessment questions)
- Refleksioon (1-2 min activity)
- Kohandus (adaptation strategies)

LENGTH: 4,000-6,000 words

TOPIC DETAILS:
[Provide topic, lesson count, time per lesson, key pedagogical considerations]
```

---

## Universal Rules (All Files)

**FORBIDDEN:**
- Emojis in headings, paragraphs, code, tables (ANYWHERE)
- "Samm N" or "Osa N" as headings
- Time markers in H1: "(3×45 min)", "~2h"
- Inline metadata: **Aeg:**, **Õpetajale:** (except tunnikava.md)
- Code blocks without language tags
- Childish language: "selgita vanaisale", "lambike"
- Excessive enthusiasm: "Wow!", "Amazing!"

**REQUIRED:**
- Exactly ONE H1 per file
- Professional vocational school tone
- Code blocks with language tags: ```bash, ```yaml, etc.
- Max 2-3 bold terms per section
- Specific version numbers where applicable
- Real industry examples
- Technical depth respecting student intelligence

**FILE-SPECIFIC H2 RULES:**
- loeng.md: "## Õpiväljundid" first
- labor.md: "## Õpiväljundid" first  
- kodutoo.md: NO "## Õpiväljundid"
- lisapraktika.md: NO "## Õpiväljundid"
- tunnikava.md: "## Õpiväljundid" first

---

## Example Usage

```
[Use Prompt 1 above]

TOPIC DETAILS:
Topic: Kubernetes Basics
Target: Adult vocational school students with Docker knowledge
Prerequisites: Docker fundamentals, Linux CLI, YAML basics
Key concepts: Pods, Deployments, Services, ConfigMaps, Namespaces
Platform coverage: Kubernetes (general), compare with Docker Swarm
Industry context: Microservices architecture, cloud-native apps
```

---

## Quality Checklist

Before finalizing ANY generated content:

**Structure:**
- [ ] Exactly ONE H1
- [ ] NO emojis present
- [ ] Proper H2 structure for file type
- [ ] Numbered sequential headings where needed

**Content:**
- [ ] Professional adult tone
- [ ] Technical accuracy
- [ ] Real industry examples
- [ ] All code blocks have language tags

**Pedagogy:**
- [ ] Builds on prior knowledge
- [ ] Explains WHY before HOW
- [ ] Includes validation/checkpoints
- [ ] Appropriate complexity progression