# Content Generation Prompts for IT Course Materials

Use these prompts to generate MkDocs + Material for MkDocs course materials.

---

## MkDocs/Material Format Rules (APPLIES TO ALL FILES)

### MkDocs Basics
- Standard Markdown with Python-Markdown extensions
- Relative linking between pages: `[Text](../module/file.md)`
- Anchor links: `[Text](file.md#heading-becomes-anchor)`
- All code blocks MUST have language tags: ` ```bash `, ` ```yaml `, ` ```python `

### Material for MkDocs Features

**1. Admonitions (Callout Boxes)**

Syntax:
```markdown
!!! type "Optional Title"
    Content indented with 4 spaces
    More content here
```

Types: `info`, `warning`, `danger`, `tip`, `note`, `success`, `question`

**Usage by file type:**
- **README.md / index pages:** ✅ USE FREELY (emojis allowed in titles)
- **loeng.md:** ⚠️ MAX 2-3 per file (pedagogical emphasis only, NO emojis)
- **labor.md:** ⚠️ MAX 1-2 (critical warnings only, NO emojis)
- **kodutoo.md:** ⚠️ MAX 1-2 (submission requirements, NO emojis)
- **tunnikava.md:** ✅ USE for pedagogical notes (NO emojis)
- **lisapraktika.md:** ❌ NEVER USE

**2. Buttons (README/index only)**
```markdown
[Get Started →](module/loeng.md){ .md-button .md-button--primary }
```

**3. Front Matter (optional)**
```markdown
---
title: Custom Page Title
description: Page description for SEO
---
```

---

## Universal Content Rules (ALL FILES)

### FORBIDDEN EVERYWHERE:
- ❌ Emojis in body text, headings (except README admonitions)
- ❌ "Samm 1", "Osa 1" as headings
- ❌ Time markers in H1: "(3×45 min)", "~2h"
- ❌ Code blocks without language tags
- ❌ Childish language: "selgita vanaisale", "lambike"
- ❌ Excessive enthusiasm: "Wow!", "Amazing!", "Super!"
- ❌ Code dumps without explanation
- ❌ Using headings for every small thing (heading inflation)

### REQUIRED EVERYWHERE:
- ✅ Exactly ONE H1 per file
- ✅ Professional vocational school tone (adult learners)
- ✅ Explain WHY before showing HOW
- ✅ Code blocks with language tags
- ✅ Max 2-3 bold terms per section (first occurrence only)
- ✅ Paragraphs 3-5 sentences (flowing, connected prose)
- ✅ Real industry examples
- ✅ Complete, working, testable code examples

### Code Block Rules:

**ALWAYS explain code:**
```markdown
Before code: 1-3 sentences explaining what will happen and why

```bash
command here
```

After code (if needed): Expected output or validation step
```

**Example of GOOD code presentation:**
```markdown
Enne projekti käivitamist tuleb seadistada virtuaalne keskkond. See hoiab 
projekti sõltuvused eraldatuna teistest Python projektidest, vältides 
versioonikonflekte.

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

Kui virtuaalne keskkond on aktiveeritud, näed terminalis `(venv)` prefiksit.
```

**Example of BAD code presentation:**
```markdown
## Paigaldamine

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Järgmine Samm
```
❌ No explanation, no context, no validation

### Heading Hierarchy Rules:

**Use headings for structure, NOT formatting:**

✅ GOOD - headings for major sections:
```markdown
## 3. Serverite Seadistamine

Configure the web servers using Ansible playbooks...

**Probleem:** Connection timeout after 30 seconds.

**Lahendus:** Increase timeout in ansible.cfg:
```

❌ BAD - headings for every tiny thing:
```markdown
## 3. Serverite Seadistamine

### Probleem
Connection timeout after 30 seconds.

### Lahendus  
Increase timeout in ansible.cfg:
```

**Bold labels vs Headings:**
- **Bold labels:** Inline quick-reference (`**Probleem:**`, `**Lahendus:**`, `**Nõuded:**`)
- **Headings:** Major structural sections, table of contents entries

---

## Prompt 1: loeng.md (Lecture Notes)

```
Create lecture notes (loeng.md) for [TOPIC] following these requirements:

TARGET AUDIENCE: Adult vocational school students, professional tone, technical depth

STRUCTURE:
- Exactly ONE H1: "# [Topic Name]" (no time markers, no emojis)
- After H1: Metadata paragraph (NOT separate lines):
  **Eeldused:** prerequisite1, prerequisite2 • **Platvorm:** platform-agnostic or specific platform
- First section MUST be "## Õpiväljundid" with 5 concrete learning outcomes
- Use Bloom's taxonomy verbs: mõistab, selgitab, eristab, võrdleb, rakendab, analüüsib

CONTENT REQUIREMENTS:
1. **Platform-agnostic theory** - cover concepts applicable across tools
2. **Compare multiple implementations** when relevant (tables preferred)
3. **Build understanding progressively:**
   - WHY does this exist? (motivation, problem it solves)
   - WHAT is it? (concepts, terminology, theory)
   - HOW does it work? (principles, not step-by-step - save for labor.md)
4. **Textbook-style flowing prose:**
   - Connected paragraphs (3-5 sentences)
   - Natural transitions between ideas
   - Build complexity gradually
   - NOT bullet-point lists (except for specific items like tools, commands)
5. **Real industry context** - how professionals use this, common patterns

CONTENT FLOW:
```
## Õpiväljundid (learning outcomes)

## 1. Introduction / Context
   - Why this topic matters
   - Problem it solves
   - Where it fits in the bigger picture

## 2. Fundamental Concepts  
   - Core terminology (bold first use only)
   - Underlying principles
   - Mental models

## 3. How It Works
   - Mechanics and architecture
   - Key components
   - Interaction patterns

## 4-6. [Specific topic sections]
   - Progressive depth
   - Comparison tables
   - Examples with explanation

## 7. Best Practices
   - Industry standards
   - Common patterns
   - What to avoid (antipatterns)

## 8. Real-World Applications
   - Use cases
   - Integration scenarios
   - Production considerations
```

FORMAT RULES:
- **Admonitions:** MAX 2-3 per file for critical concepts only (NO emojis)
- **Headings:** Numbered main sections: "## 1. Section Name", "## 2. Section Name"
- **Subsections:** Use H3 sparingly: "### 1.1 Subsection" (only when really needed)
- **Code examples:** ALWAYS with language tags and explanation before/after
- **Bold:** Max 2-3 technical terms per section, first occurrence only
- **Tables:** For comparisons, tool features, decision matrices

PEDAGOGICAL APPROACH:
- Activate prior knowledge ("Meenutades eelmisest moodulist...")
- Explain WHY before WHAT before HOW
- Use analogies from known domains (carefully, not childish)
- Include "Miks on see oluline?" explanations
- Show both what works AND what doesn't (common mistakes)
- Connect theory to practice ("labor.md näitab kuidas...")

CODE EXAMPLES IN loeng.md:
- Show WHAT code does, not step-by-step tutorial
- Annotate important lines with comments
- Explain concepts illustrated by the code
- Keep examples short and focused (10-20 lines max)

VALIDATION SECTIONS:
- "Kuidas kontrollida?" - show verification commands
- "Mis võib valesti minna?" - common issues

LENGTH: 8,000-12,000 words covering complete theory

TOPIC DETAILS:
[Provide topic, target audience, prerequisites, key concepts to cover]
```

---

## Prompt 2: labor.md (Lab Exercises)

```
Create hands-on lab exercises (labor.md) for [TOPIC] following these requirements:

TARGET AUDIENCE: Students working through guided practice with teacher available

STRUCTURE:
- Exactly ONE H1: "# [Topic Name] Labor" (no time markers, no emojis)
- After H1: Metadata paragraph:
  **Eeldused:** prerequisites • **Platvorm:** specific platform/tool • **Kestus:** approximate time
- First section MUST be "## Õpiväljundid" with 5 skill-based outcomes
- Use action verbs: loob, seadistab, käivitab, debugib, rakendab, testimisab

CONTENT REQUIREMENTS:
1. **Focus on ONE platform/tool** (choose best for teaching, explain why)
2. **Scenario-based** - realistic context students understand
3. **Step-by-step with explanations:**
   - Explain what you're about to do (1-2 sentences)
   - Show the commands/code
   - Explain what happened and why (1-2 sentences)
   - Validation checkpoint
4. **Progressive complexity:** simple → intermediate → advanced
5. **Complete working examples** students can reproduce exactly

STRUCTURE TEMPLATE:
```
## Õpiväljundid

## 1. Eelduste Kontrollimine
   - Check installations
   - Verify prerequisites
   - Prepare environment

## 2. Projekti Seadistamine
   - Initial setup
   - Configuration
   - Validation

## 3-5. [Core Tasks - numbered sequentially]
Each task:
   - Scenario/context (why are we doing this?)
   - Implementation steps (with explanations)
   - Validation (how to verify it works)
   - Expected output

## 6. Testimine ja Kontrollimine
   - End-to-end testing
   - Verification checklist

## 7. Puhastamine (Cleanup)
   - How to clean up resources
   - Reset environment

## 8. Probleemide Lahendamine
   **Probleem:** Description of common issue
   
   **Lahendus:** How to fix it:
   
   ```bash
   fix command
   ```
   
   (Repeat for 3-5 common problems)

## Kontrollnimekiri
- [ ] Task 1 completed
- [ ] Task 2 verified
- [ ] All tests passing
- [ ] Documentation updated
```

FORMAT RULES:
- **Admonitions:** MAX 1-2 (critical warnings only, NO emojis)
- **Headings:** Sequential numbering: "## 1. Task Name", "## 2. Task Name"
- **Code blocks:** MUST have language tags, explanations before AND after
- **Validation:** After each major step, show how to verify success
- **Time estimates:** In natural language in paragraphs ("see võtab umbes 10-15 minutit")

WRITING STYLE:
```markdown
GOOD EXAMPLE:

## 3. Teenuse Käivitamine

Nüüd kui konfiguratsioon on valmis, käivitame teenuse ja kontrollime selle staatust.
Dockeris töötab iga konteiner isoleeritud keskkonnnas, mis tähendab, et me peame
avaldama portid host-süsteemile.

```bash
docker run -d -p 8080:80 --name my-app nginx:latest
```

Käsk käivitab Nginx konteineri taustal (`-d`), seob host pordi 8080 konteineri 
pordiga 80 (`-p 8080:80`) ja annab konteinerile nime `my-app`. Kontrolli kas 
konteiner töötab:

```bash
docker ps
```

Peaksid nägema oma konteineri `STATUS` veerus "Up X seconds". Kui näed "Exited",
vaata logisid käsuga `docker logs my-app`.
```

NOT this (BAD):

## Paigaldamine

```bash
docker run -d -p 8080:80 --name my-app nginx:latest
docker ps
```
```

TROUBLESHOOTING SECTION:
Use **bold labels**, NOT headings:

```markdown
## Probleemide Lahendamine

**Probleem:** Konteiner ei käivitu, viskab välja "port already in use" vea.

**Lahendus:** Mõni teine protsess kasutab juba porti 8080. Kontrolli:

```bash
sudo lsof -i :8080
```

Kas soovid kasutada teist porti või peatada konkureeriva protsessi.

**Probleem:** Ei saa konteineri sisse logida.

**Lahendus:** Kontrolli kas konteiner töötab:

```bash
docker ps -a  # Näitab ka seisatud konteinereid
```
```

VALIDATION CHECKPOINTS:
After each major section:
```markdown
**Kontrolli:** Run `command` and verify you see `expected output`.
```

LENGTH: 4,000-6,000 words, 6-8 major numbered tasks

TOPIC DETAILS:
[Provide topic, platform choice, learning progression, common errors to address]
```

---

## Prompt 3: kodutoo.md (Homework)

```
Create homework assignment (kodutoo.md) for [TOPIC] following these requirements:

TARGET AUDIENCE: Students applying knowledge independently, graded work

STRUCTURE:
- Exactly ONE H1: "# [Topic Name] Kodutöö: [Specific Task]"
- After H1: Brief description paragraph with natural time estimate
  "See kodutöö võtab umbes 2-3 tundi ja tuleb esitada [date]."
- Metadata paragraph:
  **Eeldused:** prerequisites • **Esitamine:** GitHub repo link • **Tähtaeg:** specific date

NO "## Õpiväljundid" section (this is graded work, not teaching material)

CONTENT REQUIREMENTS:
1. **Different scenario from labor.md** - same platform, different tech stack/use case
2. **Apply knowledge creatively** - not just repeat lab steps
3. **Include design component** - requires thinking (architecture, pipeline design, etc.)
4. **Clear deliverables** - what files to submit, what must work
5. **Realistic scope** - completable in stated time by average student

STRUCTURE TEMPLATE:
```
# [Topic] Kodutöö: [Specific Scenario]

Brief intro paragraph with time estimate and submission info.

**Eeldused:** • **Esitamine:** • **Tähtaeg:**

## 1. Ülesande Kirjeldus

Detailed scenario:
- What you're building
- Why it matters (business context)
- Success criteria

## 2. Arhitektuur ja Planeerimine

Before coding:
- Create ARCHITECTURE.md or PIPELINE.md
- Diagram your approach
- Explain technical decisions

## 3-5. [Implementation Sections]

Each section:
- What to build
- Requirements (use checklists)
- Hints (not full solutions)
- Validation criteria

## 6. Esitamine

**Nõutavad Failid:**
- [ ] `README.md` - project overview
- [ ] `ARCHITECTURE.md` - design decisions
- [ ] Working code files
- [ ] `REFLECTION.md` - answers to reflection questions

**Repositoorium:**
Structure should look like:
```
homework-[topic]/
├── README.md
├── ARCHITECTURE.md
├── [your files]
└── REFLECTION.md
```

Submit by pushing to GitHub and sharing repo link.

## 7. Refleksioon

Answer these in `REFLECTION.md` (2-3 sentences each):

1. **Raskused:** Mis oli kõige raskem ja kuidas lahendasid?
2. **Õppetund:** Milline kontseptsioon oli suurim "ahaa!" hetk?
3. **Rakendus:** Kuidas kasutaksid seda tulevikus reaalprojektis?
4. **Seletus:** Kuidas selgitaksid sõbrale, kes ei tea IT-st midagi, mis see tehnoloogia on?
5. **Huvi:** Mis oli kõige huvitavam osa selles ülesandes?

## 8. Hindamiskriteeriumid

| Kriteerium | Punktid | Kirjeldus |
|------------|---------|-----------|
| **Funktsonaalsus** | 40% | Töötab nõuete järgi |
| **Koodikvaliteet** | 25% | Clean, documented, best practices |
| **Arhitektuur** | 20% | Design decisions explained |
| **Refleksioon** | 15% | Thoughtful answers |
| **Boonus** | +10% | Extra features (valikuline) |

**Minimaalne läbimiseks:** 50%

## 9. Boonus (+10%)

Optional extra challenges (pick one):
- [Advanced feature]
- [Integration with another tool]
- [Performance optimization]

Document bonus work in README.md.
```

FORMAT RULES:
- **Admonitions:** MAX 1-2 (submission requirements, NO emojis)
- **NO "## Kodutöö" prefix** in H2 headings
- **Numbered sections:** "## 1.", "## 2.", "## 3."
- **Checklists:** Use for requirements and deliverables
- **Code:** Provide templates/starters, NOT full solutions
- **Grading rubric:** Table format, clear percentages

TONE:
- Clear expectations (students know exactly what's required)
- Encouraging but realistic about complexity
- Hints guide without giving answers
- Emphasize learning over just "getting it done"

LENGTH: 3,000-5,000 words

TOPIC DETAILS:
[Provide topic, different scenario from lab, deliverables, grading criteria]
```

---

## Prompt 4: lisapraktika.md (Advanced Practice)

```
Create advanced optional exercises (lisapraktika.md) for [TOPIC] following these requirements:

TARGET AUDIENCE: Students who finish early, want deeper knowledge, self-directed

STRUCTURE:
- Exactly ONE H1: "# [Topic Name] Lisapraktika"
- After H1: Brief paragraph with **Eeldused:** (labor.md completed)
- NO "## Õpiväljundid" section (optional material)
- EXACTLY 3 exercises (no more, no less)

CONTENT REQUIREMENTS:
1. **Advanced beyond labor.md** but achievable in 30-45 min each
2. **One focused technique per exercise** (not combined multi-concept)
3. **Production-ready skills** students use in real jobs
4. **Progressive difficulty:** Exercise 1 (intermediate) → 3 (advanced)
5. **Self-contained** - students work independently

NO ADMONITIONS (keep it clean, text-based)

STRUCTURE PER EXERCISE:
```
## 1. [Descriptive Technique Name]

Brief paragraph explaining what this technique is and why it matters in production.

**Probleem:** What problem does basic approach have?

**Lahendus:** Explain the advanced technique:

Working code example with explanation:

```language
# Code here with comments
```

How it works explanation (2-3 paragraphs).

**Harjutus: [Specific Task]**

**Nõuded:**
- [ ] Requirement 1
- [ ] Requirement 2  
- [ ] Requirement 3
- [ ] Requirement 4

**Näpunäiteid:**
- Hint 1 (guides thinking, doesn't give answer)
- Hint 2
- Hint 3

**Testimine:**

```bash
# Commands to verify it works
```

**Boonus:**
- Optional extra challenge
- Related advanced topic

---

[Repeat structure for Exercise 2 and 3]
```

FORMAT RULES:
- **NO admonitions** anywhere
- **NO emojis** anywhere
- **Numbered exercises:** "## 1. Name", "## 2. Name", "## 3. Name"
- **Bold labels:** `**Probleem:**`, `**Lahendus:**`, `**Harjutus:**`, `**Nõuded:**`
- **NOT headings:** Don't use "### 1.1 Probleem" - use inline bold labels
- **Checklists:** For requirements (compact, actionable)
- **All code:** Language tags, explanations before showing code

WRITING STYLE:
```markdown
GOOD EXAMPLE:

## 1. Multi-Stage Docker Builds

Tavaliselt loome ühe Dockerfile'i mis sisaldab kõiki build tools'e ja runtime dependencies'e,
aga see teeb image'i ülemäära suureks. Production keskkonnas tahame võimalikult väikeseid
image'e, mis käivituvad kiiresti ja sisaldavad vähem turvaohte.

**Probleem:** Lihtne Dockerfile sisaldab build tools'e ja development dependencies'e, 
mida production runtime'is pole vaja. See suurendab image'i suurust 3-5x.

**Lahendus:** Multi-stage build võimaldab eraldada build protsessi runtime'ist:

```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/server.js"]
```

Esimene stage (`builder`) compileerib koodi. Teine stage võtab ainult compiled output'i
ja runtime dependencies. Build tools jäävad esimesse stage'i ja ei jõua final image'i.

**Harjutus: Optimeeri Node.js Rakendus**

**Nõuded:**
- [ ] Loo multi-stage Dockerfile
- [ ] Build stage kasutab node:18
- [ ] Production stage kasutab node:18-alpine
- [ ] Final image on <150MB

**Näpunäiteid:**
- Kasuta `COPY --from=builder` ainult vajalike failide jaoks
- Alpine image on minimaalne, aga kontrolli kas kõik dependencies töötavad
- Kasuta `.dockerignore` faili ebavajalike failide välistamiseks

**Testimine:**

```bash
docker build -t my-app:optimized .
docker images my-app:optimized  # Check size
docker run -p 3000:3000 my-app:optimized  # Verify it works
```

**Boonus:**
- Lisa third stage security scanning'uks
- Kasuta distroless base image veelgi väiksema image'i saamiseks
```

END SECTION:
```
## Kasulikud Ressursid

**Dokumentatsioon:**
- [Relevant official doc 1](URL)
- [Relevant official doc 2](URL)

**Tööriistad:**
- **Tool Name** - what it does: `installation command`
- **Tool Name** - what it does: `usage command`

**Näited:**
- [Example project/repo if exists](URL)

Need harjutused on mõeldud süvendama teie [TOPIC] oskusi. Alustage esimesest 
ja liikuge järk-järgult keerulisemate poole.
```

EXERCISE TOPIC SELECTION:
Choose techniques that:
- ✅ Come up in real production work
- ✅ Aren't covered in labor.md
- ✅ Can be completed in 30-45 min
- ✅ Build on each other progressively
- ❌ Aren't toy examples or academic exercises

LENGTH: 1,500-2,500 words total (500-800 per exercise)

TOPIC DETAILS:
[Provide topic, 3 specific advanced techniques, production context, skill level]
```

---

## Prompt 5: tunnikava.md (Lesson Plan)

```
Create teacher lesson plan (tunnikava.md) for [TOPIC] following these requirements:

TARGET AUDIENCE: Teachers/instructors (NOT students)

STRUCTURE:
- Exactly ONE H1: "# Tunnikava: [Topic Name]"
- After H1: Metadata paragraph:
  **Kestus:** total time • **Tase:** level • **Eeldused:** prerequisites • **Materjalid:** files needed
- First section MUST be "## Õpiväljundid" (pedagogical goals)

CONTENT REQUIREMENTS:
1. **Pedagogical framework** - cite learning theory
2. **Minute-by-minute breakdown** for each lesson block
3. **Teaching methods** - active learning strategies
4. **Troubleshooting** - common classroom issues
5. **Adaptation strategies** - for fast/slow students
6. **Assessment guidance** - formative checks

STRUCTURE TEMPLATE:
```
## Õpiväljundid

5 learning outcomes students will achieve

## Pedagoogiline Raamistik

Explain teaching philosophy for this module:
- How students learn this best (active vs passive)
- Cognitive load considerations
- Prior knowledge activation
- Metacognition strategies

Reference: "How People Learn" (National Research Council, 2000) or similar

## Õpetamismeetodid

| Meetod | Kirjeldus | Kasutamine |
|--------|-----------|------------|
| Direct instruction | Teacher explains concept | Introducing new terminology |
| Guided practice | Students do, teacher supports | Lab exercises |
| Think-pair-share | Discuss with partner | Troubleshooting |
| Live coding | Teacher codes, students follow | Demonstrating workflow |

## Näpunäited Algajale Õpetajale

Key tips for teaching this topic:
- What students find confusing
- Effective analogies/metaphors
- Common misconceptions to address
- Pace suggestions

---

[LESSON BLOCKS - One per 45 min period]

## 1. [Lesson 1 Title] (45 min)

**Aeg:** 45 minutit  
**Eesmärk:** What students achieve in this lesson  
**Meetodid:** Teaching methods used  
**Materjalid:** Files/resources needed

### Minutiplaan

**0-5 min:** Activation
- Quick review of prerequisites
- Hook/motivation for today's topic
- Learning outcomes overview

**5-15 min:** Direct Instruction
- Explain core concept
- Show examples
- Check for understanding questions

**15-35 min:** Guided Practice
- Students open labor.md
- Work through tasks 1-3
- Teacher circulates, helps

**35-40 min:** Reflection
- Quick quiz or discussion question
- What did we learn?
- Preview next lesson

**40-45 min:** Wrap-up
- Assign homework
- Answer questions
- Remind of deadlines

### Kontrollnimekiri

Success criteria for this lesson:
- [ ] All students can explain [concept]
- [ ] Code example runs successfully
- [ ] Common error addressed
- [ ] Homework assigned

### Kontrollküsimused

Ask students:
1. Question testing understanding
2. Question probing deeper
3. Question connecting to prior knowledge

### Refleksioon

Quick 2-minute activity:
- "Kirjuta üles üks asi mida täna õppisid"
- Think-pair-share: what was confusing?

### Kohandus

**Kui kiired õpilased:**
- Point to lisapraktika.md
- Suggest helping classmates
- Challenge: extend the example

**Kui aeglased õpilased:**
- Break task into smaller steps
- Pair with stronger student
- Simplify first iteration, add complexity later
- Extra lab time if needed

---

[Repeat for each lesson block]

## Kodutöö

**Millal anda:** After lesson 2  
**Tähtaeg:** 1 week  
**Tugi:** Office hours, online forum

**Jälgimine:**
- Check GitHub commits mid-week
- Remind 2 days before deadline
- Address common issues in next class

## Viited ja Täiendav Lugemine

**Pedagoogika:**
- National Research Council. (2000). *How People Learn*
- [Other learning science refs]

**Tehniline:**
- Official documentation links
- Tutorial resources
- Video explanations

## Kokkuvõte

**Mida TEHA:**
- ✅ Activate prior knowledge
- ✅ Use live coding demonstrations
- ✅ Give time for guided practice
- ✅ Check understanding frequently
- ✅ Provide individualized support

**Mida MITTE TEHA:**
- ❌ Lecture for entire period
- ❌ Skip validation steps
- ❌ Assume everyone understands
- ❌ Move too fast through fundamentals
- ❌ Ignore struggling students
```

FORMAT RULES:
- **Admonitions:** ✅ USE for pedagogical notes (NO emojis)
- **Numbered lesson blocks:** "## 1. Lesson Title", "## 2. Lesson Title"
- **Inline metadata:** **Aeg:**, **Eesmärk:** (OK in tunnikava.md)
- **Tables:** For teaching methods, assessment rubrics
- **Checklists:** For success criteria

PEDAGOGICAL DEPTH:
- Cite learning science research
- Explain cognitive load management
- Address misconceptions explicitly
- Formative assessment strategies
- Differentiation techniques

LENGTH: 4,000-6,000 words

TOPIC DETAILS:
[Provide topic, lesson count, time per lesson, key pedagogical considerations]
```

---

## Quality Checklist (Use Before Finalizing)

Before submitting ANY generated content, verify:

### Structure ✓
- [ ] Exactly ONE H1 (no duplicates)
- [ ] NO emojis in body text/headings (except README admonitions)
- [ ] Proper H2 structure for file type (Õpiväljundid placement)
- [ ] Numbered sequential headings where specified
- [ ] Heading hierarchy makes sense (not excessive H3/H4)

### Format ✓
- [ ] All code blocks have language tags (```bash, ```yaml, etc.)
- [ ] Code explained BEFORE and AFTER showing it
- [ ] Bold used sparingly (2-3 terms per section max)
- [ ] No "Samm N" or "Osa N" headings
- [ ] Admonition usage appropriate for file type
- [ ] MkDocs relative links formatted correctly

### Content ✓
- [ ] Professional adult tone (no childish language)
- [ ] Technical accuracy verified
- [ ] Real industry examples included
- [ ] Explains WHY before HOW
- [ ] Paragraphs flow naturally (3-5 sentences)
- [ ] Complete working code examples

### Pedagogy ✓
- [ ] Builds on prior knowledge explicitly
- [ ] Progressive complexity (simple → advanced)
- [ ] Validation checkpoints included
- [ ] Common errors/troubleshooting addressed
- [ ] Realistic time estimates

### File-Specific ✓
- [ ] loeng.md: Theory-focused, multi-platform
- [ ] labor.md: Step-by-step, one platform, full explanations
- [ ] kodutoo.md: Different scenario, requires creativity
- [ ] lisapraktika.md: 3 exercises, production-ready techniques
- [ ] tunnikava.md: Teacher-focused, pedagogical framework

---

## Example Usage

### For loeng.md:

```
[Use Prompt 1]

TOPIC DETAILS:
Topic: Kubernetes Basics
Target: Adult vocational school students with Docker knowledge
Prerequisites: Docker fundamentals, Linux CLI, YAML basics
Key concepts: Pods, Deployments, Services, ConfigMaps, Namespaces
Platform coverage: Kubernetes (general), compare with Docker Swarm
Industry context: Microservices architecture, cloud-native apps
```

### For labor.md:

```
[Use Prompt 2]

TOPIC DETAILS:
Topic: Kubernetes Hands-on Practice
Platform: Minikube (easiest for learning)
Progression: Single pod → Deployment → Service → ConfigMap
Common errors: Port conflicts, resource limits, image pull errors
Scenario: Deploy a simple web app with database
```

### For kodutoo.md:

```
[Use Prompt 3]

TOPIC DETAILS:
Topic: Kubernetes Application Deployment
Scenario: Multi-tier voting app (different from lab's web app)
Deliverables: Working K8s manifests, architecture diagram, reflection
Grading: 40% functionality, 25% code quality, 20% architecture, 15% reflection
Different tech stack: Use different app stack than in lab
```

---

## Common Generation Mistakes to Avoid

### ❌ Heading Inflation
```markdown
## 3. Configuration

### Probleem
### Lahendus
### Testimine
```
Should be:
```markdown
## 3. Configuration

**Probleem:** ...
**Lahendus:** ...
**Testimine:** ...
```

### ❌ Code Without Explanation
```markdown
Setup the environment:

```bash
export VAR=value
source .env
npm install
```

Next step...
```
Should be:
```markdown
Before running the application, configure the environment variables. These tell
the app where to find the database and which port to use.

```bash
export DATABASE_URL="postgresql://localhost/mydb"
export PORT=3000
```

The app will read these on startup. Verify they're set correctly:

```bash
echo $DATABASE_URL  # Should show your connection string
```
```

### ❌ Missing Language Tags
```markdown
Run these commands:

```
git clone repo
cd repo
```
```
Should be:
```markdown
Clone the repository to your local machine:

```bash
git clone https://github.com/user/repo.git
cd repo
```
```

### ❌ Time Markers in H1
```markdown
# Docker Basics (3×45 min)
```
Should be:
```markdown
# Docker Basics

**Kestus:** 3 nädalat (3×45 min tunni) • **Eeldused:** Linux CLI basics
```

---

## Final Notes

**Remember:**
1. Students need to understand WHY, not just copy-paste
2. Code without explanation teaches nothing
3. Headings are for structure, not every paragraph
4. MkDocs features enhance content, don't distract
5. Professional tone = respecting students' intelligence

**Test your generated content:**
- Can a student follow it without teacher help? (labor.md, kodutoo.md)
- Does it explain concepts clearly? (loeng.md)
- Could a new teacher use this? (tunnikava.md)
- Do the advanced exercises teach real skills? (lisapraktika.md)