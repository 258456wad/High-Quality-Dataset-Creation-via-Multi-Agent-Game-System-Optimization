math_template = '''Create a math problem related to the following persona:

{persona}

Note:

1. The math problem should be challenging and involve advanced mathematical skills and knowledge. Only top talents can solve it correctly.
2. You should make full use of the persona description to create the math problem to ensure that the math problem is unique and specific to the persona.
3. Your response should always start with "Math problem:". Your response should not include a solution to the created math problem.
4. Your created math problem should include no more than 2 sub-problems.
'''

math_template_cn = '''根据以下人设，创建一个数学题：

{persona}

注意：

1. 该数学题需具备挑战性，涉及高级数学技能与知识，只有顶尖人才能正确解答。
2. 你应充分利用人设描述，使数学题独特且与该人设高度相关。
3. 你的回答应包含该数学题的解答。
4. 你创建的数学题不应包含超过 2 个子问题。
'''

finance_template = '''Create a finance problem related to the following persona:

{persona}

Note:

1. The finance problem should be challenging and involve advanced quantitative finance concepts (e.g., stochastic processes, risk measures, derivatives pricing, portfolio optimization).
2. Make full use of the persona description so the problem is unique and tailored to the persona's background.
3. Your response should always start with "Finance problem:". Your response should not include a solution.
4. Your finance problem should include no more than 2 sub-problems.
'''

finance_template_cn = '''根据以下人设，创建一个金融题：

{persona}

注意：

1. 该金融题需具备挑战性，涉及高级量化金融概念（例如随机过程、风险度量、衍生品定价、投资组合优化）。
2. 你应充分利用人设描述，使题目独特且与该人设高度相关。
3. 你的回答应包含解答。
4. 你创建的金融题不应包含超过 2 个子问题。
'''


instruction_template = '''Guess a prompt that the following persona may ask you to do:

{persona}

Note:

1. The prompt should be informative and specific.
2. Your output should start with "User prompt:"'''

instruction_template_cn = '''Guess a prompt that the following persona may ask you to do:

{persona}

Note:

1. The prompt should be informative and specific.
2. Your output should start with "User prompt:"'''

knowledge_template = '''{persona}

Assume you are the persona described above and you are writing a Quora article using your knowledge, skills, experience, or insights to help others learn and benefit from it.

Note:

1. The article should be specific, informative and knowledge-rich.
2. Your response should start with "Title:"'''

knowledge_template_cn = '''{persona}

Assume you are the persona described above and you are writing a Quora article using your knowledge, skills, experience, or insights to help others learn and benefit from it.

Note:

1. The article should be specific, informative and knowledge-rich.
2. Your response should start with "Title:"'''

npc_template = '''World of Warcraft (WoW) is a massively multiplayer online role-playing game (MMORPG) developed by Blizzard Entertainment. It is set in the high-fantasy world of Azeroth, a land filled with rich lore, diverse races, and epic conflicts. The game has evolved significantly since its release in 2004, with numerous expansions adding new continents, races, classes, and storylines. Below is a detailed overview of the game's worldview, story background, and some key characters and NPCs.

### Worldview and Story Background

**Azeroth** is a world steeped in ancient history, powerful magic, and epic conflicts. The planet is divided into several continents, each with its own unique environments, cultures, and histories. The main continents include:

- Eastern Kingdoms: Home to the human kingdoms, dwarves, gnomes, and the undead Forsaken.
- Kalimdor: Inhabited by orcs, night elves, tauren, trolls, and other races.
- Northrend: A frozen continent, home to the Lich King and the undead Scourge.
- Pandaria: A mystical land shrouded in mists, home to the Pandaren.
- Broken Isles: The remnants of the ancient Night Elf civilization and the site of the Tomb of Sargeras.
- Zandalar and Kul Tiras: Introduced in the Battle for Azeroth expansion, these are the homelands of the Zandalari trolls and the human kingdom of Kul Tiras, respectively.
- Shadowlands: The realm of the afterlife, introduced in the Shadowlands expansion.

The story of Azeroth is vast and complex, spanning millennia and involving numerous races, factions, and cosmic forces. Here are some key aspects of the world's background:

#### **The Titans and the Old Gods**

- **The Titans**: Azeroth was shaped by the Titans, colossal beings who are part of the Pantheon, a group of god-like entities dedicated to bringing order to the universe. The Titans discovered Azeroth and found it infested with chaotic entities known as the Old Gods. To combat this, they created the Titan-forged, including the Keepers, to help shape and protect the world.

- **The Old Gods**: These malevolent, ancient beings sought to corrupt Azeroth. The Titans imprisoned the Old Gods beneath the surface of the world, but their influence persisted, causing chaos and corruption throughout history. Notable Old Gods include C'Thun, Yogg-Saron, N'Zoth, and Y'Shaarj.

#### **The Sundering**

- **The Well of Eternity**: At the center of ancient Kalimdor was the Well of Eternity, a source of immense arcane power. The Highborne, a group of night elves led by Queen Azshara, recklessly tapped into its power, attracting the attention of the Burning Legion, a demonic army led by the dark titan Sargeras.

- **The War of the Ancients**: This conflict saw the night elves, dragons, and other races unite to repel the Burning Legion's invasion. The war culminated in the Sundering, a catastrophic event that shattered the supercontinent of Kalimdor into several smaller continents and created the Maelstrom, a massive, swirling vortex of energy.

#### **The Rise and Fall of Empires**

- **The Troll Empires**: Before the Sundering, the trolls established powerful empires, such as the Gurubashi and Amani. These empires declined over time but left a lasting impact on Azeroth's history.

- **The Night Elf Empire**: After the Sundering, the night elves established a new empire, centered around the World Tree, Nordrassil. They became the guardians of nature and the Emerald Dream, a parallel realm of primal life.

- **The Human Kingdoms**: Humans emerged as a dominant race in the Eastern Kingdoms, founding powerful kingdoms such as Stormwind, Lordaeron, and Dalaran. These kingdoms played crucial roles in the defense of Azeroth against various threats.

#### **The First and Second Wars**

- **The First War**: The orcs, originally from the world of Draenor, were corrupted by the Burning Legion and transported to Azeroth through the Dark Portal. They waged war against the human kingdom of Stormwind, ultimately destroying it.

- **The Second War**: The orcs, now united under the Horde, continued their conquest, clashing with the Alliance of Lordaeron, a coalition of human, dwarf, and high elf forces. The Alliance eventually triumphed, and the orcs were interned in camps.

#### **The Scourge and the Lich King**

- **The Lich King**: Created by the demon lord Kil'jaeden, the Lich King was originally the orc shaman Ner'zhul. He was transformed into a powerful undead entity and imprisoned in the Frozen Throne in Northrend. The Lich King created the Scourge, an army of undead, to pave the way for a new invasion by the Burning Legion.

- **The Third War**: The Scourge ravaged the human kingdoms, leading to the fall of Lordaeron and the rise of the undead Forsaken. The war culminated in the Battle of Mount Hyjal, where the combined forces of the night elves, Horde, and Alliance defeated the Burning Legion.

#### **The Burning Crusade and Beyond**

- **The Burning Crusade**: The first expansion of WoW saw players journey to Outland, the shattered remnants of Draenor, to combat the Burning Legion and its allies.

- **Wrath of the Lich King**: This expansion focused on the conflict with the Lich King in Northrend, culminating in his defeat at Icecrown Citadel.

- **Cataclysm**: The return of the corrupted Dragon Aspect Deathwing caused massive upheaval across Azeroth, reshaping the world and leading to new conflicts.

- **Mists of Pandaria**: This expansion introduced the mysterious continent of Pandaria and its inhabitants, the Pandaren, as well as new threats from the Sha and the mogu.

- **Warlords of Draenor**: Players traveled to an alternate-timeline Draenor to confront the Iron Horde, a new orcish threat.

- **Legion**: The Burning Legion launched a full-scale invasion of Azeroth, leading to epic battles and the eventual defeat of the dark titan Sargeras.

- **Battle for Azeroth**: This expansion reignited the conflict between the Alliance and Horde, with new zones, races, and storylines.

- **Shadowlands**: The latest expansion takes players to the realm of the afterlife, where they must confront new threats and uncover the mysteries of death.

### Overarching Themes

**1. Conflict and Unity**
- The world of Azeroth is defined by its conflicts, both internal and external. The ongoing struggle between the Alliance and Horde is a central theme, but there are also numerous other conflicts involving ancient evils, demonic invasions, and cosmic forces. Despite these conflicts, there are moments of unity where disparate factions come together to face common threats.

**2. Corruption and Redemption**
- Many of Azeroth's greatest heroes and villains have faced corruption, often by dark forces such as the Old Gods or the Burning Legion. Redemption is a recurring theme, with characters seeking to atone for their past actions and reclaim their honor.

**3. Legacy and Heritage**
- The history of Azeroth is rich with ancient civilizations, legendary heroes, and powerful artifacts. The legacy of these past events shapes the present, with characters and factions often drawing on their heritage to guide their actions.

**4. Magic and Technology**
- Azeroth is a world where magic and technology coexist. Arcane magic, divine power, and druidic nature magic are all integral to the world's functioning, while technological advancements by races like the gnomes and goblins add another layer of complexity.

**5. Exploration and Discovery**
- The world of Azeroth is vast and filled with hidden secrets, ancient ruins, and uncharted territories. Exploration and discovery are key aspects of the game's appeal, with players constantly uncovering new lore and adventures.

### Key Characters and NPCs

**1. Thrall (Go'el)**
- **Race**: Orc
- **Class**: Shaman
- **Background**: Thrall is one of the most iconic characters in WoW. He was the Warchief of the Horde and played a crucial role in uniting the orc clans and leading them to a new home in Kalimdor. Thrall is known for his wisdom, strength, and deep connection to the elements.

**2. Jaina Proudmoore**
- **Race**: Human
- **Class**: Mage
- **Background**: Jaina is the daughter of Admiral Daelin Proudmoore and one of the most powerful mages in Azeroth. She has been a key figure in many of the game's major events, including the founding of Theramore and the defense of Azeroth against various threats.

**3. Sylvanas Windrunner**
- **Race**: Undead (formerly High Elf)
- **Class**: Hunter
- **Background**: Sylvanas was the Ranger-General of Silvermoon before being turned into a banshee by Arthas Menethil. She later became the leader of the Forsaken and, for a time, the Warchief of the Horde. Her actions have often been controversial and have had significant impacts on the game's storyline.

**4. Anduin Wrynn**
- **Race**: Human
- **Class**: Priest
- **Background**: Anduin is the King of Stormwind and the son of the legendary King Varian Wrynn. Known for his compassion and desire for peace, Anduin has grown into a strong leader, guiding the Alliance through numerous conflicts.

**5. Arthas Menethil (The Lich King)**
- **Race**: Undead (formerly Human)
- **Class**: Death Knight
- **Background**: Arthas was the Crown Prince of Lordaeron who fell from grace and became the Lich King, one of the most feared beings in Azeroth. His story is central to the Wrath of the Lich King expansion.

**6. Illidan Stormrage**
- **Race**: Night Elf (Demon Hunter)
- **Class**: Demon Hunter
- **Background**: Illidan is a complex character who has walked the line between hero and villain. He was imprisoned for ten thousand years for his use of forbidden magic but later became a key figure in the fight against the Burning Legion.

**7. Bolvar Fordragon**
- **Race**: Human (later Undead)
- **Class**: Paladin (later Death Knight)
- **Background**: Bolvar was a noble paladin who sacrificed himself to become the new Lich King, containing the Scourge. His story takes a dramatic turn in the Shadowlands expansion.

**8. Tyrande Whisperwind**
- **Race**: Night Elf
- **Class**: Priestess of Elune
- **Background**: Tyrande is the High Priestess of Elune and the leader of the Night Elves. She is a fierce warrior and a devoted leader, often seen alongside her husband, Malfurion Stormrage.

**9. Malfurion Stormrage**
- **Race**: Night Elf
- **Class**: Druid
- **Background**: Malfurion is the first Night Elf druid and one of the most powerful druids in Azeroth. He has played a crucial role in many of the world's major events, including the War of the Ancients and the defense of Azeroth against numerous threats.

**10. Vol'jin**
- **Race**: Troll
- **Class**: Shadow Hunter
- **Background**: Vol'jin was the leader of the Darkspear Trolls and later became the Warchief of the Horde. He is known for his wisdom, bravery, and deep connection to the spirits.

### Notable NPCs

**1. Khadgar**
- **Race**: Human
- **Class**: Mage
- **Background**: Khadgar is one of the most powerful mages in Azeroth and a key figure in the fight against the Burning Legion. He played a significant role in the events of the Warlords of Draenor and Legion expansions.

**2. Varok Saurfang**
- **Race**: Orc
- **Class**: Warrior
- **Background**: Saurfang is a legendary orc warrior known for his honor and strength. He played a pivotal role in the events of the Battle for Azeroth expansion.

**3. Lor'themar Theron**
- **Race**: Blood Elf
- **Class**: Ranger
- **Background**: Lor'themar is the Regent Lord of Quel'Thalas and the leader of the Blood Elves. He has guided his people through many challenges, including their alliance with the Horde.

**4. Genn Greymane**
- **Race**: Worgen (formerly Human)
- **Class**: Warrior
- **Background**: Genn is the King of Gilneas and a fierce leader of the Worgen. He has a deep-seated hatred for Sylvanas Windrunner and has been a key figure in the Alliance's efforts against the Horde.

**5. Baine Bloodhoof**
- **Race**: Tauren
- **Class**: Warrior
- **Background**: Baine is the High Chieftain of the Tauren and the son of the legendary Cairne Bloodhoof. He is known for his wisdom, strength, and dedication to his people.

**6. Alexstrasza the Life-Binder**
- **Race**: Dragon (Red Dragonflight)
- **Class**: Aspect of Life
- **Background**: Alexstrasza is the Aspect of Life and the leader of the Red Dragonflight. She has played a crucial role in many of Azeroth's major events, including the fight against Deathwing and the Cataclysm.

**7. Magni Bronzebeard**
- **Race**: Dwarf
- **Class**: Warrior (later Speaker of Azeroth)
- **Background**: Magni is the former King of Ironforge who was transformed into a diamond form to become the Speaker of Azeroth, communicating with the world-soul of the planet.

**8. Turalyon**
- **Race**: Human
- **Class**: Paladin
- **Background**: Turalyon is a legendary paladin and one of the original Knights of the Silver Hand. He spent many years fighting the Burning Legion in the Twisting Nether and returned to Azeroth during the Legion expansion.

**9. Alleria Windrunner**
- **Race**: High Elf (later Void Elf)
- **Class**: Ranger
- **Background**: Alleria is the eldest of the Windrunner sisters and a skilled ranger. She embraced the powers of the Void and became a key figure in the fight against the Burning Legion.

**10. Nathanos Blightcaller**
- **Race**: Undead
- **Class**: Hunter
- **Background**: Nathanos is a loyal champion of Sylvanas Windrunner and one of the most skilled hunters in Azeroth. He played a significant role in the events of the Battle for Azeroth expansion.

---

Above is the introduction and backgroud story of the game "World of Warcraft (WoW)".

Your task is to consider what NPC the following persona will become after they come to the world of WoW:

{persona}

Note:

1. Your response should start with "Name:".
2. Your NPC description should be specific and consistent with the game.
3. You also need to specify how the NPC interacts with players in the game.
'''

npc_template_cn = '''World of Warcraft (WoW) is a massively multiplayer online role-playing game (MMORPG) developed by Blizzard Entertainment. It is set in the high-fantasy world of Azeroth, a land filled with rich lore, diverse races, and epic conflicts. The game has evolved significantly since its release in 2004, with numerous expansions adding new continents, races, classes, and storylines. Below is a detailed overview of the game's worldview, story background, and some key characters and NPCs.

### Worldview and Story Background

**Azeroth** is a world steeped in ancient history, powerful magic, and epic conflicts. The planet is divided into several continents, each with its own unique environments, cultures, and histories. The main continents include:

- Eastern Kingdoms: Home to the human kingdoms, dwarves, gnomes, and the undead Forsaken.
- Kalimdor: Inhabited by orcs, night elves, tauren, trolls, and other races.
- Northrend: A frozen continent, home to the Lich King and the undead Scourge.
- Pandaria: A mystical land shrouded in mists, home to the Pandaren.
- Broken Isles: The remnants of the ancient Night Elf civilization and the site of the Tomb of Sargeras.
- Zandalar and Kul Tiras: Introduced in the Battle for Azeroth expansion, these are the homelands of the Zandalari trolls and the human kingdom of Kul Tiras, respectively.
- Shadowlands: The realm of the afterlife, introduced in the Shadowlands expansion.

The story of Azeroth is vast and complex, spanning millennia and involving numerous races, factions, and cosmic forces. Here are some key aspects of the world's background:

#### **The Titans and the Old Gods**

- **The Titans**: Azeroth was shaped by the Titans, colossal beings who are part of the Pantheon, a group of god-like entities dedicated to bringing order to the universe. The Titans discovered Azeroth and found it infested with chaotic entities known as the Old Gods. To combat this, they created the Titan-forged, including the Keepers, to help shape and protect the world.

- **The Old Gods**: These malevolent, ancient beings sought to corrupt Azeroth. The Titans imprisoned the Old Gods beneath the surface of the world, but their influence persisted, causing chaos and corruption throughout history. Notable Old Gods include C'Thun, Yogg-Saron, N'Zoth, and Y'Shaarj.

#### **The Sundering**

- **The Well of Eternity**: At the center of ancient Kalimdor was the Well of Eternity, a source of immense arcane power. The Highborne, a group of night elves led by Queen Azshara, recklessly tapped into its power, attracting the attention of the Burning Legion, a demonic army led by the dark titan Sargeras.

- **The War of the Ancients**: This conflict saw the night elves, dragons, and other races unite to repel the Burning Legion's invasion. The war culminated in the Sundering, a catastrophic event that shattered the supercontinent of Kalimdor into several smaller continents and created the Maelstrom, a massive, swirling vortex of energy.

#### **The Rise and Fall of Empires**

- **The Troll Empires**: Before the Sundering, the trolls established powerful empires, such as the Gurubashi and Amani. These empires declined over time but left a lasting impact on Azeroth's history.

- **The Night Elf Empire**: After the Sundering, the night elves established a new empire, centered around the World Tree, Nordrassil. They became the guardians of nature and the Emerald Dream, a parallel realm of primal life.

- **The Human Kingdoms**: Humans emerged as a dominant race in the Eastern Kingdoms, founding powerful kingdoms such as Stormwind, Lordaeron, and Dalaran. These kingdoms played crucial roles in the defense of Azeroth against various threats.

#### **The First and Second Wars**

- **The First War**: The orcs, originally from the world of Draenor, were corrupted by the Burning Legion and transported to Azeroth through the Dark Portal. They waged war against the human kingdom of Stormwind, ultimately destroying it.

- **The Second War**: The orcs, now united under the Horde, continued their conquest, clashing with the Alliance of Lordaeron, a coalition of human, dwarf, and high elf forces. The Alliance eventually triumphed, and the orcs were interned in camps.

#### **The Scourge and the Lich King**

- **The Lich King**: Created by the demon lord Kil'jaeden, the Lich King was originally the orc shaman Ner'zhul. He was transformed into a powerful undead entity and imprisoned in the Frozen Throne in Northrend. The Lich King created the Scourge, an army of undead, to pave the way for a new invasion by the Burning Legion.

- **The Third War**: The Scourge ravaged the human kingdoms, leading to the fall of Lordaeron and the rise of the undead Forsaken. The war culminated in the Battle of Mount Hyjal, where the combined forces of the night elves, Horde, and Alliance defeated the Burning Legion.

#### **The Burning Crusade and Beyond**

- **The Burning Crusade**: The first expansion of WoW saw players journey to Outland, the shattered remnants of Draenor, to combat the Burning Legion and its allies.

- **Wrath of the Lich King**: This expansion focused on the conflict with the Lich King in Northrend, culminating in his defeat at Icecrown Citadel.

- **Cataclysm**: The return of the corrupted Dragon Aspect Deathwing caused massive upheaval across Azeroth, reshaping the world and leading to new conflicts.

- **Mists of Pandaria**: This expansion introduced the mysterious continent of Pandaria and its inhabitants, the Pandaren, as well as new threats from the Sha and the mogu.

- **Warlords of Draenor**: Players traveled to an alternate-timeline Draenor to confront the Iron Horde, a new orcish threat.

- **Legion**: The Burning Legion launched a full-scale invasion of Azeroth, leading to epic battles and the eventual defeat of the dark titan Sargeras.

- **Battle for Azeroth**: This expansion reignited the conflict between the Alliance and Horde, with new zones, races, and storylines.

- **Shadowlands**: The latest expansion takes players to the realm of the afterlife, where they must confront new threats and uncover the mysteries of death.

### Overarching Themes

**1. Conflict and Unity**
- The world of Azeroth is defined by its conflicts, both internal and external. The ongoing struggle between the Alliance and Horde is a central theme, but there are also numerous other conflicts involving ancient evils, demonic invasions, and cosmic forces. Despite these conflicts, there are moments of unity where disparate factions come together to face common threats.

**2. Corruption and Redemption**
- Many of Azeroth's greatest heroes and villains have faced corruption, often by dark forces such as the Old Gods or the Burning Legion. Redemption is a recurring theme, with characters seeking to atone for their past actions and reclaim their honor.

**3. Legacy and Heritage**
- The history of Azeroth is rich with ancient civilizations, legendary heroes, and powerful artifacts. The legacy of these past events shapes the present, with characters and factions often drawing on their heritage to guide their actions.

**4. Magic and Technology**
- Azeroth is a world where magic and technology coexist. Arcane magic, divine power, and druidic nature magic are all integral to the world's functioning, while technological advancements by races like the gnomes and goblins add another layer of complexity.

**5. Exploration and Discovery**
- The world of Azeroth is vast and filled with hidden secrets, ancient ruins, and uncharted territories. Exploration and discovery are key aspects of the game's appeal, with players constantly uncovering new lore and adventures.

### Key Characters and NPCs

**1. Thrall (Go'el)**
- **Race**: Orc
- **Class**: Shaman
- **Background**: Thrall is one of the most iconic characters in WoW. He was the Warchief of the Horde and played a crucial role in uniting the orc clans and leading them to a new home in Kalimdor. Thrall is known for his wisdom, strength, and deep connection to the elements.

**2. Jaina Proudmoore**
- **Race**: Human
- **Class**: Mage
- **Background**: Jaina is the daughter of Admiral Daelin Proudmoore and one of the most powerful mages in Azeroth. She has been a key figure in many of the game's major events, including the founding of Theramore and the defense of Azeroth against various threats.

**3. Sylvanas Windrunner**
- **Race**: Undead (formerly High Elf)
- **Class**: Hunter
- **Background**: Sylvanas was the Ranger-General of Silvermoon before being turned into a banshee by Arthas Menethil. She later became the leader of the Forsaken and, for a time, the Warchief of the Horde. Her actions have often been controversial and have had significant impacts on the game's storyline.

**4. Anduin Wrynn**
- **Race**: Human
- **Class**: Priest
- **Background**: Anduin is the King of Stormwind and the son of the legendary King Varian Wrynn. Known for his compassion and desire for peace, Anduin has grown into a strong leader, guiding the Alliance through numerous conflicts.

**5. Arthas Menethil (The Lich King)**
- **Race**: Undead (formerly Human)
- **Class**: Death Knight
- **Background**: Arthas was the Crown Prince of Lordaeron who fell from grace and became the Lich King, one of the most feared beings in Azeroth. His story is central to the Wrath of the Lich King expansion.

**6. Illidan Stormrage**
- **Race**: Night Elf (Demon Hunter)
- **Class**: Demon Hunter
- **Background**: Illidan is a complex character who has walked the line between hero and villain. He was imprisoned for ten thousand years for his use of forbidden magic but later became a key figure in the fight against the Burning Legion.

**7. Bolvar Fordragon**
- **Race**: Human (later Undead)
- **Class**: Paladin (later Death Knight)
- **Background**: Bolvar was a noble paladin who sacrificed himself to become the new Lich King, containing the Scourge. His story takes a dramatic turn in the Shadowlands expansion.

**8. Tyrande Whisperwind**
- **Race**: Night Elf
- **Class**: Priestess of Elune
- **Background**: Tyrande is the High Priestess of Elune and the leader of the Night Elves. She is a fierce warrior and a devoted leader, often seen alongside her husband, Malfurion Stormrage.

**9. Malfurion Stormrage**
- **Race**: Night Elf
- **Class**: Druid
- **Background**: Malfurion is the first Night Elf druid and one of the most powerful druids in Azeroth. He has played a crucial role in many of the world's major events, including the War of the Ancients and the defense of Azeroth against numerous threats.

**10. Vol'jin**
- **Race**: Troll
- **Class**: Shadow Hunter
- **Background**: Vol'jin was the leader of the Darkspear Trolls and later became the Warchief of the Horde. He is known for his wisdom, bravery, and deep connection to the spirits.

### Notable NPCs

**1. Khadgar**
- **Race**: Human
- **Class**: Mage
- **Background**: Khadgar is one of the most powerful mages in Azeroth and a key figure in the fight against the Burning Legion. He played a significant role in the events of the Warlords of Draenor and Legion expansions.

**2. Varok Saurfang**
- **Race**: Orc
- **Class**: Warrior
- **Background**: Saurfang is a legendary orc warrior known for his honor and strength. He played a pivotal role in the events of the Battle for Azeroth expansion.

**3. Lor'themar Theron**
- **Race**: Blood Elf
- **Class**: Ranger
- **Background**: Lor'themar is the Regent Lord of Quel'Thalas and the leader of the Blood Elves. He has guided his people through many challenges, including their alliance with the Horde.

**4. Genn Greymane**
- **Race**: Worgen (formerly Human)
- **Class**: Warrior
- **Background**: Genn is the King of Gilneas and a fierce leader of the Worgen. He has a deep-seated hatred for Sylvanas Windrunner and has been a key figure in the Alliance's efforts against the Horde.

**5. Baine Bloodhoof**
- **Race**: Tauren
- **Class**: Warrior
- **Background**: Baine is the High Chieftain of the Tauren and the son of the legendary Cairne Bloodhoof. He is known for his wisdom, strength, and dedication to his people.

**6. Alexstrasza the Life-Binder**
- **Race**: Dragon (Red Dragonflight)
- **Class**: Aspect of Life
- **Background**: Alexstrasza is the Aspect of Life and the leader of the Red Dragonflight. She has played a crucial role in many of Azeroth's major events, including the fight against Deathwing and the Cataclysm.

**7. Magni Bronzebeard**
- **Race**: Dwarf
- **Class**: Warrior (later Speaker of Azeroth)
- **Background**: Magni is the former King of Ironforge who was transformed into a diamond form to become the Speaker of Azeroth, communicating with the world-soul of the planet.

**8. Turalyon**
- **Race**: Human
- **Class**: Paladin
- **Background**: Turalyon is a legendary paladin and one of the original Knights of the Silver Hand. He spent many years fighting the Burning Legion in the Twisting Nether and returned to Azeroth during the Legion expansion.

**9. Alleria Windrunner**
- **Race**: High Elf (later Void Elf)
- **Class**: Ranger
- **Background**: Alleria is the eldest of the Windrunner sisters and a skilled ranger. She embraced the powers of the Void and became a key figure in the fight against the Burning Legion.

**10. Nathanos Blightcaller**
- **Race**: Undead
- **Class**: Hunter
- **Background**: Nathanos is a loyal champion of Sylvanas Windrunner and one of the most skilled hunters in Azeroth. He played a significant role in the events of the Battle for Azeroth expansion.

---

Above is the introduction and backgroud story of the game "World of Warcraft (WoW)".

Your task is to consider what NPC the following persona will become after they come to the world of WoW:

{persona}

Note:

1. Your response should start with "Name:".
2. Your NPC description should be specific and consistent with the game.
3. You also need to specify how the NPC interacts with players in the game.
'''

# Stock and Securities Templates
stock_analysis_cn = '''根据以下人设，创建一个关于股票分析的问题或任务：

{persona}

注意：

1. 该问题需具备专业性和挑战性，涉及股票技术分析、基本面分析、估值方法等高级财务知识。
2. 问题应该结合该人设的背景和专业经验，使其独特且与该人设高度相关。
3. 你的回答应包含具体的股票分析方法、数据引用或投资建议。
4. 你创建的问题应包含不超过3个分析维度（如技术面、基本面、市场面等）。
'''

stock_knowledge_cn = '''{persona}

假设你是上述人设描述的专业人士，你正在撰写一篇关于证券投资的深度文章，利用你的知识、经验和见解来帮助他人学习和获益。

注意：

1. 文章应具有专业性、信息量丰富，涵盖股票市场、证券知识或投资策略的深度内容。
2. 你的回答应包含文章标题。
3. 文章应包含具体的数据、案例研究或理论分析。
'''

trading_strategy_cn = '''根据以下人设，创建一个关于交易策略的问题或方案：

{persona}

注意：

1. 该策略需具备可操作性和专业性，涉及风险管理、头寸管理、市场时机等因素。
2. 你应充分利用人设描述，使策略独特且与该人设的投资风格高度相关。
3. 你的回答应包含具体的交易规则、入场条件、止损点和利润目标。
4. 策略应考虑不同的市场条件（牛市、熊市、震荡市场）。
'''

risk_assessment_cn = '''根据以下人设和投资背景，创建一个关于风险评估的问题或分析：

{persona}

注意：

1. 风险评估需具备深度和专业性，涉及信用风险、市场风险、流动性风险、系统性风险等。
2. 你应充分利用人设描述来分析特定投资或投资组合的风险。
3. 你的回答应包含具体的风险指标（如VaR、夏普比率、Beta系数）和风险缓解措施。
4. 分析应包含不超过3个主要风险因素。
'''

market_insight_cn = '''{persona}

假设你是上述人设描述的投资专家或市场分析师，你正在撰写一份关于当前市场形势的深度分析报告，利用你的专业知识和市场敏感性来提供独特的市场洞察。

注意：

1. 分析应具有时效性和前瞻性，涵盖行业动态、宏观经济影响或市场机会。
2. 你的回答应包含报告标题和核心观点。
3. 报告应包含具体的数据支持、趋势判断和投资建议。
'''

# 建议在 prompt_templates.py 中添加
universal_gen_v2_cn = '''
### 角色背景
{persona}

### 任务指令
你现在是一名顶尖的内容生成专家。请结合上述人设的专业知识、思维方式和语言习惯，创作一个高质量的挑战性任务。

### 创作要求
1. 任务类型：可以是复杂的逻辑推理、专业领域深度分析、或是跨学科的综合问题。
2. 难度等级：必须是该领域专家级别才能处理的问题。
3. 语言：必须使用中文。

### 输出格式（必须严格遵守以下 JSON 结构）
{{
  "thought": "（第一步：分析该角色的核心能力和特有的思维盲点）",
  "instruction": "（第二步：基于背景，给出一个具体的、具有挑战性的指令或问题）",
  "expected_logic": "（第三步：拆解该问题的解题关键路径和所需的知识点）",
  "solution": "（第四步：给出该问题的标准答案或深度参考分析）"
}}
'''