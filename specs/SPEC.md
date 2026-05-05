# Specification

Questo repository serve per gestire il mio curriculum vitae, sia dal punto di vista dei contenuti che delle varie rappresentazioni.

L'idea è di avere una unica single source of truth che rappresenta le informazioni ed il contenuto del cv. Come single source of truth penso ad un file `cv.yaml` con questo formato di esempio:

```yaml
personal:
  name: John Doe
  title: Software Engineer
  email: john.doe@example.com
  phone: +1 234 567 890
  linkedin: linkedin.com/in/johndoe
  github: github.com/johndoe
  website: www.johndoe.com
summary: >
  Experienced Software Engineer with a strong background in developing scalable web applications and working with cross-functional teams. Proficient in multiple programming languages and frameworks, with a passion for learning new technologies and improving
  software development processes.
experiences:
  - company: Company A
    role: Senior Software Engineer
    location: Siena, Italy
    start_date: 2020-01
    end_date: present
    responsibilities:
      - Lead the development of a high-traffic e-commerce platform, resulting in a 30% increase in sales.
      - Collaborate with product managers and designers to implement new features and improve user experience.
      - Mentor junior developers and conduct code reviews to maintain code quality.
  - company: Company B
    role: Software Engineer
    location: Siena, Italy
    start_date: 2017-01
    end_date: 2019-12
    responsibilities:
      - Something
      - Other things
education:
  - institution: University of Siena
    degree: Bachelor of Science in Computer Science
    date: 2012-09
  - institution: Google Cloud Certified
    degree: Associate Cloud Engineer
    date: 2020
skills:
  - topic: Programming Languages
    description: Python, JavaScript, Java
  - topic: Soft Skills
    description: Communication, Teamwork, Problem-solving
version: 1.2.3
```

Ad ora data la single source of truth vorrei avere a isposizione due possibili target di build:

1. formato pdf: attraverso LaTeX con il template Awesome-CV
2. formato web statico, mi piacerebbe con GitHub Pages.

siccome il repository è sotto github, vorrei utilizzare le actions di github per i due target di build.

Criteri di accettazione:

- il pdf deve stare massimo in due pagine
- il sito web deve essere responsive, riportare in calce la versione (major.minor.patch) gestita manualmente nello yaml e la data in formato YYYY-MM della build
- il sito web statico deve avere un link in calce con al pdf generato con latex, file `tommaso-cortonesi-cv.pdf` nella root
- anche il pdf generato deve avere la versione (major.minor.patch) gestita manualmente nello yaml e la data in formato YYYY-MM della build
- ad ora non esistono campi obbligatori
- le date devono avere il formato YYYY-MM, YYYY (nel caso non ci sia l'informazione del mese) oppure può essere la stringa "present"

Cosa non è in perimetro:

- gestiamo soltanto il profilo di software architect
- solo in inglese
- non si includono foto
- in caso di dubbi su decisioni da prendere devi porre a me la domanda
- non si valida per adesso lo yaml, se mancano info o campi la pipe si rompe

Il repository deve essere così strutturato:

```text
- spec # directory contenenti le spec
- cv-latex # folder contenente i componenti che servono alla generazione del cv in pdf con latex
- cv-web # folder contenente i componenti che servono alla generazione del cv in formato web
- CLAUDE.md # file per claude
- cv.yaml # single source of truth
- tommaso-cortonesi-cv.pdf # pdf generato con la pipe con latex
- README.md # readme che illustra il repo
```

Principi di ispirazione:

- Pragmatismo: YAGNI e KISS, costruiamo ciò che serve adesso senza over-engineering
- Evoluzione: disegnamo, progettiamo e pensiamo per evoluzione e cambiamento al fine di poterci adattare
