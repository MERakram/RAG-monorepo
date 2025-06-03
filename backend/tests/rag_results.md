# RAG Query Results

Generated on: 2025-05-14 11:54:30

## Query: Tu peux m'expliquer comme fonctionne la 61850 ? fais un maximum de schémas en ascii art

### Model: mistral-small:latest

**Response:**

IEC 61850 est une norme internationale qui définit la communication dans les systèmes d'automatisation des sous-stations électriques. Elle permet une interopérabilité entre différents équipements fournis par différents fabricants, ce qui simplifie l'intégration et la gestion des systèmes de contrôle et de protection.

### Fonctionnement de IEC 61850

IEC 61850 utilise plusieurs protocoles pour assurer la communication entre les appareils. Voici une explication détaillée avec des schémas en ASCII art :

#### 1. Architecture Générale
```
+---------------------------------------+
|         Application Layer             |
| +-----------------------------+      |
| |       MMS Protocol          |      |
| +----------^-----------------+      |
|              |                  |
|              v                  |
| +-----------------------------+      |
| |    GOOSE Messages           |      |
| +-----------------------------+      |
| |   Sampled Values            |      |
| +---------------------------------------+
```

#### 2. MMS Protocol (Manufacturing Message Specification)
Le protocole MMS est utilisé pour la communication entre les objets IEC 61850 et les opérations de service. Chaque objet IEC 61850 est mappé à un objet MMS, et chaque service IEC 61850 est mappé à une opération MMS.

```
+---------------------------------------------+
|         IEC 61850 Object                        |
| +---------------------------+                |
| |    GOOSE Messages        |                |
| +----------^----------------+                |
|              |                             |
|              v                             |
| +---------------------------+                |
| |    MMS Object             |                |
| +---------------------------+                |
```

#### 3. GOOSE Messages (Generic Object Oriented Substation Event)
Les messages GOOSE sont utilisés pour la transmission rapide d'événements critiques, comme les commandes de protection et de contrôle.

```
+------------------------------------+
|         IEC 61850 Object           |
| +-------------------------+       |
| |      GOOSE Messages     |       |
| +----------^---------------+       |
|              |                   |
|              v                   |
| +-------------------------------+|
| |    Real Communication        ||
| |         System               ||
| +-------------------------------+
```

#### 4. Sampled Values
Les valeurs échantillonnées sont utilisées pour la transmission de données mesurées en temps réel, comme les tensions et courants.

```
+------------------------------------+
|         IEC 61850 Object           |
| +-------------------------+       |
| |    Sampled Values       |       |
| +----------^---------------+       |
|              |                   |
|              v                   |
| +-------------------------------+|
| |    Real Communication        ||
| |         System               ||
| +-------------------------------+
```

#### 5. Logical Nodes
Les nœuds logiques représentent les fonctions spécifiques dans un appareil, comme la mesure de tension ou la protection contre les surcharges.

```
+--------------------------------------+
|      IEC 61850 Logical Node           |
| +-------------------------+          |
| |    MMXU (Tension)       |          |
| +----------^---------------+          |
|              |                        |
|              v                        |
| +------------------------------+     |
| |   Real Communication System  |     |
| +------------------------------+
```

#### 6. Physical Nodes
Les nœuds physiques représentent les appareils réels dans une sous-station, comme les disjoncteurs et les transformateurs.

```
+---------------------------------------+
|      IEC 61850 Physical Node         |
| +-------------------------+          |
| |    Disjoncteur X        |          |
| +----------^---------------+          |
|              |                        |
|              v                        |
| +------------------------------+     |
| |   Real Communication System  |     |
| +------------------------------+
```

### Conclusion
IEC 61850 est une norme complexe mais nécessaire pour l'automatisation des sous-stations. Elle utilise plusieurs protocoles, notamment MMS, GOOSE messages et valeurs échantillonnées, pour assurer une communication efficace entre les équipements. Les nœuds logiques et physiques jouent un rôle crucial dans la représentation des fonctions et des appareils réels.

Pour plus de détails sur l'implémentation et les outils disponibles, vous pouvez consulter des ressources comme [rapid61850](https://github.com/stevenblair/rapid61850) et [bit.ly/rapid61850](http://bit.ly/rapid61850).

**Sources:**
* **61850-1 Ed2 - TR_draft_V3.pdf**, page *12*
* **61850-6{ed1.0}en.pdf**, page *141*
* **AN61850.EN005-IEC-61850-interface-configuration-for-VAMP-products-and-WIMO.pdf**, page *7*
* **Blair%20-%20Using%20IEC%2061850%20-%20PES%20GM%202013.pdf**, pages *3, 12, 17*
* **EL0820IEC6185020for20switchgear20-20basic20knowledge20-20Presentationpdfx-signRYfJAcR6902x5TOdCXncY9yJodrMAvCbmLOn76f2Fay7szCsBXhQjnPCo2FZ5Jp1LE.pdf**, pages *8, 13*
* **Fast bus protection using iec 61850.pdf**, page *8*
* **IEC%2061850%20Overview-Ruggedcom.pdf**, page *14*
* **IEC%2061850%20Protocol%20API%20User%20Manual.pdf**, page *41*
* **IEC%2061850_Presentation.pdf**, pages *10, 11, 14*
* **IEC61850_Protocol_API_UserManual_v02.pdf**, page *41*
* **N0123_Notes_IEC61850.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.pdf**, page *3*
* **PPT_COPALP IEC61850.pdf**, pages *3, 7, 17*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331_14h30.doc**, page *0*
* **Questionnaire CEI 61850 - 00 (juin 2014) - Fr.docx**, page *6*
* **iec61850-1{ed2.0}b.pdf**, page *4*
* **iec61850-6{ed2.0}en.pdf**, page *193*
* **iec61850-intro.pdf**, page *41*
* **iec61850-intropdf.pdf**, page *41*

---

### Model: deepseek-r1:32b

**Response:**



IEC 61850 est une norme utilisée pour automatiser les postes de transformation électrique. Elle permet une communication standardisée entre les dispositifs, facilitant la gestion et le contrôle des installations électriques.

### Fonctionnement de IEC 61850 :
1. **Modèle d'Objets** : 
   - Structure hiérarchique d'objets logiques (Logical Devices, Logical Nodes) représentant les fonctionnalités du dispositif.
   
2. **Services et Opérations** :
   - Définit des services comme la gestion de données, l'exécution de commandes, etc., qui sont mappés sur le protocole MMS.

3. **Communication** :
   - Utilise MMS pour les échanges de données standardisés.
   - Emploie GOOSE (Generic Object Oriented Substation Event) et des valeurs échantillonnées pour les messages temps réel via UDP.

### Diagrammes ASCII :

#### 1. Architecture Générale
```
+-------------------+
|     Poste        |
|    électrique    |
+-------------------+
           |
           v
+-------------------------------+
|   IEC 61850 Communication      |
| +--------+  +-----------+     |
 | |Dispositifs|  |Merging Units| |
 | +--------+  +-----------+     |
           |             |
           v             v
+-------------------+  +------------+
|    Contrôle       |  |   GOOSE/SV|
| et supervision    |  +------------+
+-------------------+
```

#### 2. Mappage des Protocoles
```
IEC 61850 Layer
+----------------+
| Logical Device |
+----------------+
           |
           v
+----------------+
| Logical Node   |
+----------------+
           |
           v
+----------------+
| IEC Services    |
+----------------+
           |
           v
MMS Mapping
+----------------+
| MMS Objects     |
+----------------+
           |
           v
+----------------+  +------------+
| MMS Operations |  | GOOSE/UDP  |
+----------------+  +------------+
```

Ces schémas simplifiés illustrent la structure et le flux de communication dans un système IEC 61850, montrant comment les données circulent des dispositifs vers les systèmes de contrôle.

**Sources:**
* **61850-1 Ed2 - TR_draft_V3.pdf**, page *12*
* **61850-6{ed1.0}en.pdf**, page *141*
* **AN61850.EN005-IEC-61850-interface-configuration-for-VAMP-products-and-WIMO.pdf**, page *7*
* **Blair%20-%20Using%20IEC%2061850%20-%20PES%20GM%202013.pdf**, pages *3, 12, 17*
* **EL0820IEC6185020for20switchgear20-20basic20knowledge20-20Presentationpdfx-signRYfJAcR6902x5TOdCXncY9yJodrMAvCbmLOn76f2Fay7szCsBXhQjnPCo2FZ5Jp1LE.pdf**, pages *8, 13*
* **Fast bus protection using iec 61850.pdf**, page *8*
* **IEC%2061850%20Overview-Ruggedcom.pdf**, page *14*
* **IEC%2061850%20Protocol%20API%20User%20Manual.pdf**, page *41*
* **IEC%2061850_Presentation.pdf**, pages *10, 11, 14*
* **IEC61850_Protocol_API_UserManual_v02.pdf**, page *41*
* **N0123_Notes_IEC61850.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.pdf**, page *3*
* **PPT_COPALP IEC61850.pdf**, pages *3, 7, 17*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331_14h30.doc**, page *0*
* **Questionnaire CEI 61850 - 00 (juin 2014) - Fr.docx**, page *6*
* **iec61850-1{ed2.0}b.pdf**, page *4*
* **iec61850-6{ed2.0}en.pdf**, page *193*
* **iec61850-intro.pdf**, page *41*
* **iec61850-intropdf.pdf**, page *41*

---

## Query: Tu peux détailler les Logical Nodes et leur architecture dans la norme IEC 61850 en t'appuyant sur de l'ascii art pour les schémas?

### Model: mistral-small:latest

**Response:**

Les Logical Nodes (LNs) sont des éléments centraux dans la norme IEC 61850, qui est utilisée pour la communication dans les sous-stations électriques. Un Logical Node est un modèle abstrait d'un dispositif réel ou d'une fonction spécifique. Il inclut des données, des attributs de données et des comportements bien définis.

### Architecture des Logical Nodes

#### 1. Définition et Structure
Un Logical Node représente une fonction typique dans une sous-station, comme un disjoncteur (XCBR), un transformateur (YPTR) ou un relais de protection (RSYN). Chaque LN fournit une liste bien organisée d'informations, telles que la position d'un disjoncteur ("Pos") et son mode ("Mode").

#### 2. Relation avec les Dispositifs Logiques
Un dispositif logique (Logical Device) représente un ensemble typique de fonctions de sous-station. Chaque dispositif logique contient plusieurs Logical Nodes. Par exemple, un dispositif logique pour un disjoncteur peut inclure des LNs comme XCBR (circuit breaker), RSYN (protection related), etc.

#### 3. Communication entre Logical Nodes
La communication entre les LNs est standardisée et générique, permettant une interopérabilité maximale. Les services définis dans IEC 61850-7-2 permettent l'échange d'informations entre les LNs. Par exemple, le LN "XCBR5" représente un disjoncteur spécifique avec des données telles que la position et le mode.

### Schéma ASCII Art

Voici une représentation simplifiée de l'architecture des Logical Nodes dans un dispositif logique :

```
Logical Device
   |
   +-- Logical Node 1 (LN1)
   |     +-- Data Object 1
   |     +-- Data Object 2
   |     +-- ...
   |
   +-- Logical Node 2 (LN2)
   |     +-- Data Object 3
   |     +-- Data Object 4
   |     +-- ...
   |
   +-- Logical Node 3 (LN3)
         +-- Data Object 5
         +-- Data Object 6
         +-- ...
```

### Exemple de LNs et leurs Données

- **XCBR** : Circuit Breaker
  - Position ("Pos")
  - Mode ("Mode")

- **RSYN** : Protection Related
  - Status ("Sta")
  - Settings ("Set")

- **YPTR** : Transformer
  - Temperature ("Temp")
  - Voltage ("Volt")

### Fonctionnement et Interopérabilité

Les LNs sont définis de manière à être indépendants du matériel, ce qui permet une mise en œuvre future-proof. Chaque LN contient des données avec des attributs dédiés, ayant une structure et un sens bien définis dans le contexte des systèmes d'automatisation pour les services publics électriques.

### Conclusion

Les Logical Nodes dans la norme IEC 61850 sont essentiels pour la communication standardisée et l'interopérabilité entre différents dispositifs dans les sous-stations. Ils fournissent une structure claire et bien définie pour modéliser les fonctions de sous-station, permettant ainsi une communication efficace et fiable.

En résumé, les Logical Nodes sont des composants clés de la norme IEC 61850, offrant une modularité et une flexibilité qui permettent de répondre aux besoins actuels et futurs des systèmes d'automatisation des sous-stations.

**Sources:**
* **2015_Seyed_Reza20Firouzi_MSc20thesis20reportpdf.pdf**, page *30*
* **61850-1 Ed2 - TR_draft_V3.pdf**, page *24*
* **61850-5 Ed2 - CDV {en}.pdf**, pages *37, 38*
* **61850-5{ed1.0}en.pdf**, page *36*
* **61850-7-1 Ed2 - FDIS {en}.pdf**, page *56*
* **61850-7-1_R2-05_FDIS_To-IEC-CO_2002-11-04pdf.pdf**, page *57*
* **61850-7-420 - Ed1.pdf**, page *24*
* **Asset-Management-IEC61850_Overview_and_Application-Day-2pdf.pdf**, page *11*
* **DJC passerelle 61850.doc**, page *0*
* **Guide pour IEC 61850-7 (2004).pdf**, page *4*
* **IEC 61850-5 (2003) - Spécifications de communication pour modèles de fonctions et de dispositifs.pdf**, page *36*
* **IEC 61850-5.pdf**, page *36*
* **IEC 61850-7-2 (2003) - Structure de base pour sous-stations - ACSI.pdf**, page *40*
* **IEC%2061850-5.pdf**, page *36*
* **IEC_61850_7_1_Browsable_Models.pdf**, page *4*
* **PPT_COPALP IEC61850.pdf**, page *10*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331.doc**, page *0*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331_14h30.doc**, page *0*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331_16h53.doc**, page *0*
* **SA2007-000062_en_A_User_Friendly_Implementation_of_IEC_61850_in_a_New_Generation_of_Protection_and_Control_Devices.pdf**, page *2*
* **T0994_61850 Network Simulator.pdf**, page *2*
* **iec61850-1{ed2.0}b.pdf**, pages *4, 27*
* **iec61850-5{ed2.0}b.pdf**, page *61*
* **iec61850-7-1{ed2.0}b(1).pdf**, page *58*
* **iec61850-7-420{ed1.0}en(1).pdf**, page *24*

---

### Model: deepseek-r1:32b

**Response:**



### Définition des Logical Nodes (LN)

Les **Logical Nodes** (Nœuds Logiques) sont des modèles abstraits de dispositifs ou fonctions réels dans un système électrique. Chaque LN contient des données, des attributs de données et un comportement spécifique. Par exemple :
- `XCBR` : Circuit Breaker
- `RSYN` : Fonction de protection
- `YPTR` : Transformateur

### Architecture des Logical Nodes

Les Logical Nodes sont organisés au sein de **Logical Devices** (LD), qui représentent une fonction ou un dispositif spécifique dans une sous-station. Par exemple :
- Un LD peut être un contrôleur de circuit (Breaker Controller).
- Un LD peut être une fonction PMU (Système de Mesure de Puissance).

#### Structure hiérarchique

```
Physique Device
├── Logical Device (LD)
│   ├── Logical Node (LN) 1
│   │   ├── Data Object 1
│   │   │   └── Data Attribute 1
│   │   └── Data Object 2
│   │       └── Data Attribute 2
│   ├── Logical Node (LN) 2
│   │   ├── Data Object 3
│   │   │   └── Data Attribute 3
│   │   └── Data Object 4
│   │       └── Data Attribute 4
│   └── ...
└── ...
```

#### Composants d'un Logical Node

Un LN comprend :
- **Données (Data)** : Valeurs mesurées ou générées.
- **Ensembles de données (DataSet)** : Groupement logique de données.
- **Contrôle des rapports (BRCB, URCB)** : Gestion des rapports en temps réel.
- **Logiciels et services** : Fonctionnalités d'échange de données.

```
Logical Node (LN)
├── Data
│   ├── Pos (Position)
│   └── Mode (Mode opérationnel)
├── DataSet
│   ├── DS1
│   └── DS2
├── BRCB (Buffered Report Control Block)
├── URCB (Unbuffered Report Control Block)
└── Services
    ├── GetLogicalNodeDirectory
    └── GetAllDataValues
```

#### Communication entre Logical Nodes

Les LN communiquent via des protocoles comme **Goose** et **GSSE**, permettant l'échange de données entre clients/serveurs ou dispositifs de même hiérarchie.

```
Logical Node A (XCBR1)
├── Envoie des données
│   └── Goose
└── Reçoit des données
    └── GSSE

Logical Node B (MMXU2)
├── Envoie des données
│   └── Goose
└── Reçoit des données
    └── GSSE
```

### Exemple d'architecture dans une sous-station

Voici un exemple de configuration typique :

```
Physical Device 1 (Circuit Breaker)
├── Logical Device 1 (Breaker Controller)
│   ├── LN1 (XCBR1)
│   │   ├── Pos (Position)
│   │   └── Mode (Mode opérationnel)
│   └── LN2 (MMXU1)
│       ├── Ua (Courant A)
│       └── Ub (Courant B)
└── Logical Device 2 (Protection Function)
    ├── LN3 (PSCH1)
    │   ├── Trip (Commande de déclenchement)
    │   └── Reset (Commande de réinitialisation)
    └── LN4 (RREC1)
        ├── Reclose (Commande de reclosure)
        └── Lockout (Verrouillage)
```

### Résumé

- **Logical Node** : Unité fondamentale modélisant une fonction ou dispositif.
- **Logical Device** : Ensemble logique de LN pour une fonction spécifique.
- **Données et services** : Structure interne des LN pour l'échange d'informations.
- **Protocoles** : Goose et GSSE pour la communication.

Cette architecture permet une standardisation et une interoperabilité robustes dans les systèmes de sous-station.

**Sources:**
* **2015_Seyed_Reza20Firouzi_MSc20thesis20reportpdf.pdf**, page *30*
* **61850-1 Ed2 - TR_draft_V3.pdf**, page *24*
* **61850-5 Ed2 - CDV {en}.pdf**, pages *37, 38*
* **61850-5{ed1.0}en.pdf**, page *36*
* **61850-7-1 Ed2 - FDIS {en}.pdf**, page *56*
* **61850-7-1_R2-05_FDIS_To-IEC-CO_2002-11-04pdf.pdf**, page *57*
* **61850-7-420 - Ed1.pdf**, page *24*
* **Asset-Management-IEC61850_Overview_and_Application-Day-2pdf.pdf**, page *11*
* **DJC passerelle 61850.doc**, page *0*
* **Guide pour IEC 61850-7 (2004).pdf**, page *4*
* **IEC 61850-5 (2003) - Spécifications de communication pour modèles de fonctions et de dispositifs.pdf**, page *36*
* **IEC 61850-5.pdf**, page *36*
* **IEC 61850-7-2 (2003) - Structure de base pour sous-stations - ACSI.pdf**, page *40*
* **IEC%2061850-5.pdf**, page *36*
* **IEC_61850_7_1_Browsable_Models.pdf**, page *4*
* **PPT_COPALP IEC61850.pdf**, page *10*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331.doc**, page *0*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331_14h30.doc**, page *0*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331_16h53.doc**, page *0*
* **SA2007-000062_en_A_User_Friendly_Implementation_of_IEC_61850_in_a_New_Generation_of_Protection_and_Control_Devices.pdf**, page *2*
* **T0994_61850 Network Simulator.pdf**, page *2*
* **iec61850-1{ed2.0}b.pdf**, pages *4, 27*
* **iec61850-5{ed2.0}b.pdf**, page *61*
* **iec61850-7-1{ed2.0}b(1).pdf**, page *58*
* **iec61850-7-420{ed1.0}en(1).pdf**, page *24*

---

## Query: Tu peux me faire un exemple complet d'une application qui mesure les puissances dans un transformateur haute tension et qui utiliserait le 61850 ? ajoute des schémas en ascii et détaille bien chaque interface

### Model: mistral-small:latest

**Response:**

Pour illustrer un exemple complet d'une application qui mesure les puissances dans un transformateur haute tension utilisant le protocole IEC 61850, nous allons décrire une configuration typique avec les éléments nécessaires. Nous utiliserons des schémas en ASCII pour représenter les interfaces et les connections.

### Contexte de l'application

L'objectif est de mesurer les puissances (active, réactive, apparente) dans un transformateur haute tension (HTA-BT) et d'intégrer ces mesures dans un système de supervision utilisant le protocole IEC 61850. Nous utiliserons des convertisseurs de mesure compatibles IEC 61850 pour effectuer les conversions nécessaires.

### Composants principaux

1. **Transformateur HTA-BT**
2. **Convertisseur de mesure SEREM (compatible IEC 61850)**
3. **Passerelle IEC 61850**
4. **Système de supervision**

### Schéma en ASCII

```
+---------------------+
| Transformateur HTA-BT|
+---------+-----------+
          |
          v
+--------------------------+
| Convertisseur de mesure   |
| SEREM (IEC 61850)        |
+-------+-----------------+
       |
       v
+----------------------------+
| Passerelle IEC 61850       |
+----------+-----------------+
           |
           v
+----------------------------+
| Système de supervision      |
+----------------------------+
```

### Détails des interfaces

1. **Transformateur HTA-BT**
   - **Entrée**: Tension et courant haute tension.
   - **Sortie**: Signaux analogiques (tension, courant).

2. **Convertisseur de mesure SEREM (IEC 61850)**
   - **Fonction**: Convertit les signaux analogiques en données numériques au format IEC 61850.
   - **Entrée**: Signaux analogiques du transformateur HTA-BT.
   - **Sortie**: Données numériques IEC 61850 (sample value, GOOSE, report).
   - **Paramétrage**: Via fichier ICD et page Web server.

3. **Passerelle IEC 61850**
   - **Fonction**: Transmet les données IEC 61850 au système de supervision.
   - **Entrée**: Données numériques IEC 61850 du convertisseur SEREM.
   - **Sortie**: Données IEC 61850 vers le système de supervision.

4. **Système de supervision**
   - **Fonction**: Affiche, enregistre et analyse les données de puissance.
   - **Entrée**: Données IEC 61850 via la passerelle.
   - **Sortie**: Interface utilisateur pour les opérateurs (graphiques, alarmes, rapports).

### Fonctionnement détaillé

1. **Mesure des signaux analogiques**:
   - Le transformateur HTA-BT génère des tensions et courants haute tension qui sont convertis en signaux analogiques par des capteurs de courant et de tension.

2. **Conversion en données numériques IEC 61850**:
   - Les signaux analogiques sont envoyés au convertisseur de mesure SEREM, qui les convertit en données numériques au format IEC 61850.
   - Le convertisseur est paramétré comme serveur IEC 61850 et renvoie des valeurs sous forme de "sample value", "GOOSE" ou "report".

3. **Transmission des données**:
   - Les données numériques IEC 61850 sont transmises à la passerelle IEC 61850 via Ethernet.
   - La passerelle agit comme un intermédiaire, assurant la communication entre le convertisseur et le système de supervision.

4. **Supervision et analyse**:
   - Le système de supervision reçoit les données IEC 61850 et les affiche en temps réel sur une interface utilisateur.
   - Les opérateurs peuvent visualiser les puissances active, réactive et apparente, ainsi que d'autres paramètres pertinents.

### Exemple de configuration IEC 61850

- **Logical Node**: MMXU (Measurements for active and reactive power)
- **Data Attributes**:
  - ActivePower
  - ReactivePower
  - ApparentPower

### Schéma détaillé en ASCII

```
+---------------------+
| Transformateur HTA-BT|
+---------+-----------+
          |
          v
+--------------------------+      +----------------------+
| Convertisseur de mesure   | <--> | Passerelle IEC 61850 |
| SEREM (IEC 61850)        |      +----------------------+
+-------+-----------------+                ^
       |                          |
       v                          |
+--------------------------+              v
| Système de supervision    |            +-------------+
+--------------------------+            | Interface   |
                                          | utilisateur|
                                          +-------------+

```

### Conclusion

Cette configuration permet de mesurer et de superviser les puissances dans un transformateur haute tension en utilisant le protocole IEC 61850. Les convertisseurs de mesure SEREM, la passerelle IEC 61850 et le système de supervision travaillent ensemble pour fournir une solution complète et intégrée, facilitant ainsi la gestion et l'analyse des données de puissance en temps réel.

**Sources:**
* **61850-1 Ed2 - TR_draft_V3.pdf**, page *2*
* **Blair%20-%20Using%20IEC%2061850%20-%20PES%20GM%202013.pdf**, pages *3, 12*
* **Fast bus protection using iec 61850.pdf**, page *50*
* **IEC 61850 - T_COSTE - R&D EDF.pdf**, page *10*
* **IEC%2061850%20Overview-Ruggedcom.pdf**, page *39*
* **IEC%2061850-hands-on-training%20program_Stockholm%20November%202-5%202010_v5.pdf**, page *2*
* **IEC%2061850_Presentation.pdf**, pages *10, 11*
* **N0123_Notes_IEC61850.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.pdf**, pages *3, 17, 18*
* **Overview20of20IEC206235120standardspdf.pdf**, page *7*
* **PPT_COPALP IEC61850.pdf**, page *17*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331.doc**, page *0*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331.pdf**, page *5*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331_14h30.doc**, page *0*
* **Retour_d_experience_EDF_61850.pdf**, page *10*
* **SEREM - iec61850-fra.pdf**, page *1*
* **SINEAX CAM_IEC61850_FR.pdf**, page *8*
* **Siemens - CEI 61850 - Application_examples.pdf**, pages *28, 44*
* **iec61850-1{ed2.0}b.pdf**, page *15*
* **iec61850-fra.pdf**, page *1*

---

### Model: deepseek-r1:32b

**Response:**



### Exemple complet d'une application mesurant les puissances dans un transformateur haute tension avec IEC 61850

#### **Contexte**
Dans une station électrique, il est essentiel de surveiller et de mesurer les puissances dans les transformateurs haute tension pour garantir le fonctionnement optimal du réseau. L'utilisation du protocole IEC 61850 permet une communication standardisée entre les appareils, facilitant l'intégration et la supervision des données.

#### **Interfaces Physiques**
1. **Transducteur Numérique** (comme SEREM CPA3)
   - Convertit les signaux électriques en données numériques conformes à IEC 61850.
2. **Concentrateur IEC 61850** (comme remsdaq Callisto)
   - Rassemble et route les données des transducteurs vers le système de supervision.
3. **Routeur Ethernet/IP**
   - Connecte les appareils via un réseau local pour la transmission des données.
4. **Serveur Historisateur**
   - Stocke les données mesurées pour l'analyse future.
5. **Station de Supervision**
   - Interface utilisateur pour visualiser et contrôler les données en temps réel.

#### **Interfaces Logiques**
1. **Message GOOSE (Generic Object Oriented Substation Event)**
   - Utilisé pour la transmission d'événements critiques (comme des alarmes ou des triages).
2. **Message Sampled Value**
   - Transmet les valeurs de mesure en temps réel.
3. **Nœuds Logiques IEC 61850**
   - MMXU (Measurements) pour les puissances et les tensions.
   - CSWI (Control Switch) pour le contrôle des disjoncteurs.

#### **Schéma ASCII de l'Architecture**

```
+-------------------+       +-------------------+       +-------------------+
| Transducteur CPA3 |-------| Concentrateur      |-------| Routeur Ethernet  |
| (SEREM)           |       | remsdaq Callisto   |       |                   |
+-------------------+       +-------------------+       +-------------------+
          ||                         ||                         ||
          ||                         ||                         ||
          vv                         vv                         vv
+-------------------+       +-------------------+       +-------------------+
| Serveur Historisateur  |   | Station de        |   | Logiciel de        |
| (Stockage des données) |   | Supervision       |   | Configuration      |
+-------------------+       +-------------------+       +-------------------+
```

#### **Fonctionnement Étape par Étape**
1. **Capture des Données**
   - Le transducteur CPA3 mesure les puissances et les tensions dans le transformateur.
2. **Conversion en Format IEC 61850**
   - Les données sont converties en messages Sampled Value conformes à la norme.
3. **Transmission via Réseau**
   - Les concentrateurs remsdaq Callisto transmettent ces données via Ethernet.
4. **Traitement et Visualisation**
   - La station de supervision affiche les données en temps réel, permettant aux opérateurs de surveiller l'état du transformateur.
5. **Enregistrement Historique**
   - Les serveurs historisateurs stockent les données pour une analyse postérieure.

#### **Conclusion**
Cette architecture exemplaire montre comment IEC 61850 facilite la communication et la supervision dans une station électrique, permettant une meilleure gestion des transformateurs haute tension.

**Sources:**
* **61850-1 Ed2 - TR_draft_V3.pdf**, page *2*
* **Blair%20-%20Using%20IEC%2061850%20-%20PES%20GM%202013.pdf**, pages *3, 12*
* **Fast bus protection using iec 61850.pdf**, page *50*
* **IEC 61850 - T_COSTE - R&D EDF.pdf**, page *10*
* **IEC%2061850%20Overview-Ruggedcom.pdf**, page *39*
* **IEC%2061850-hands-on-training%20program_Stockholm%20November%202-5%202010_v5.pdf**, page *2*
* **IEC%2061850_Presentation.pdf**, pages *10, 11*
* **N0123_Notes_IEC61850.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.pdf**, pages *3, 17, 18*
* **Overview20of20IEC206235120standardspdf.pdf**, page *7*
* **PPT_COPALP IEC61850.pdf**, page *17*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331.doc**, page *0*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331.pdf**, page *5*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331_14h30.doc**, page *0*
* **Retour_d_experience_EDF_61850.pdf**, page *10*
* **SEREM - iec61850-fra.pdf**, page *1*
* **SINEAX CAM_IEC61850_FR.pdf**, page *8*
* **Siemens - CEI 61850 - Application_examples.pdf**, pages *28, 44*
* **iec61850-1{ed2.0}b.pdf**, page *15*
* **iec61850-fra.pdf**, page *1*

---

## Query: Tu peux me faire un exemple complet d'une application qui mesure les puissances dans un transformateur haute tension et qui utiliserait le 61850 ? ajoute des schémas en ascii et détaille bien chaque interface et utilise les mots clés de l'IEC 61850 pour chaque élément.

### Model: mistral-small:latest

**Response:**

Pour illustrer un exemple complet d'une application qui mesure les puissances dans un transformateur haute tension (HT) utilisant le protocole IEC 61850, nous allons détailler chaque élément et interface en utilisant les mots-clés et concepts de l'IEC 61850.

### Exemple d'Application : Mesure des Puissances dans un Transformateur HT

#### Contexte :
Un transformateur haute tension (HT) est utilisé pour transformer le voltage de la distribution électrique. Nous allons mesurer la puissance active, réactive et apparente à l'aide d'un convertisseur de mesure IEC 61850.

#### Schéma ASCII :

```
+-------------------+
| Transformateur HT |
+-----------+-------+
          |
          v
+---------------------+
| Convertisseur IEC   |
| 61850               |
+---------+----------+
         |
         v
+-----------------------------+
| Contrôleur de Substation    |
| (IED - Intelligent Electronic|
| Device)                     |
+-------+--------------------+
        |
        v
+--------------------------+
| Système de Supervision   |
| et de Contrôle           |
| (SCADA System)           |
+-----------------------------+
```

#### Détails des Interfaces et Éléments :

1. **Transformateur HT** :
   - **Fonction** : Transforme le voltage haute tension.
   - **Interfaces** : Connecté au convertisseur de mesure IEC 61850 via des capteurs de courant et de tension.

2. **Convertisseur de Mesure IEC 61850** :
   - **Fonction** : Convertit les signaux analogiques (tension, courant) en données numériques au format IEC 61850.
   - **Interfaces** :
     - **Entrée** : Signaux analogiques (tension et courant) du transformateur HT.
     - **Sortie** : Données numériques au format IEC 61850 (sample value, GOOSE, report).
     - **Paramétrage** : Via fichier ICD (Institution Configuration Description) et page Web server.

3. **Contrôleur de Substation (IED)** :
   - **Fonction** : Collecte les données des convertisseurs de mesure et effectue les opérations de protection, contrôle et automation.
   - **Interfaces** :
     - **Entrée** : Données numériques IEC 61850 du convertisseur de mesure.
     - **Sortie** : Commandes et alarmes vers le système SCADA.

4. **Système de Supervision et de Contrôle (SCADA System)** :
   - **Fonction** : Supervise et contrôle l'ensemble du réseau électrique, y compris les transformateurs HT.
   - **Interfaces** :
     - **Entrée** : Données de supervision et de contrôle des IEDs.
     - **Sortie** : Interface utilisateur pour les opérateurs, rapports et alarmes.

#### Exemple de Mapping Logical Interfaces to Physical Interfaces :

```plaintext
+-----------------------------+
|       Logical Nodes        |
+----------+-----------------+
          |
          v
+---------------------------+
|      Physical Devices     |
+--------+------------------+
         |
         v
+-----------------------+
|  IEC 61850 Interfaces |
+------+----------------+
```

#### Exemple de Mapping des Fonctions, Logical Nodes et Physical Nodes :

```plaintext
Fonction          | Logical Node    | Physical Device
----------------- | --------------- | ------------------
Mesure de Puissance| MMXU1           | Convertisseur IEC 61850
Protection        | PPRO            | IED
Contrôle          | CCTR            | IED
Automation        | AUTO            | SCADA System
```

#### Exemple de Data Modelling :

```plaintext
Data Object     | Data Attribute   | Value Format
----------------| -----------------| --------------
Sampled Values  | Magnitude         | Float
                | Phase Angle      | Degrees
GOOSE           | Status           | Boolean
Report          | Timestamp        | UTC Time
```

### Conclusion :
Cet exemple illustre comment le protocole IEC 61850 peut être utilisé pour mesurer les puissances dans un transformateur haute tension. Les différents composants (convertisseurs de mesure, IEDs, système SCADA) communiquent via des interfaces définies par la norme IEC 61850, permettant ainsi une interopérabilité et une intégration efficaces.

**Sources:**
* **61850-1 Ed2 - TR_draft_V3.pdf**, pages *2, 13*
* **ABB@IEC61850(b).pdf**, page *10*
* **Blair%20-%20Using%20IEC%2061850%20-%20PES%20GM%202013.pdf**, pages *3, 4, 12, 17*
* **IEC 61850 - T_COSTE - R&D EDF.pdf**, page *10*
* **IEC 61850 Fuzzer[1].pdf**, page *10*
* **IEC%2061850%20Overview-Ruggedcom.pdf**, page *39*
* **IEC%2061850_Presentation.pdf**, pages *10, 11*
* **Introduction-to-IEC-61850-Basics-R2_Chi-Carnegie.pdf**, page *3*
* **Introduction-to-IEC-61850-Basics-R2_Chi-Carnegiepdf.pdf**, page *3*
* **N0123_Notes_IEC61850.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.pdf**, page *3*
* **Overview20of20IEC206235120standardspdf.pdf**, page *7*
* **PPT_COPALP IEC61850.pdf**, page *17*
* **Retour_d_experience_EDF_61850.pdf**, page *10*
* **SEREM - iec61850-fra.pdf**, page *1*
* **Siemens - CEI 61850 - Application_examples.pdf**, pages *1, 28, 44*
* **abb_sr_iec_61850_72dpi.pdf**, page *11*
* **iec61850-1{ed2.0}b.pdf**, page *15*
* **iec61850-fra.pdf**, page *1*

---

### Model: deepseek-r1:32b

**Response:**



### Exemple d'application mesurant les puissances dans un transformateur haute tension en utilisant le protocole IEC 61850 :

#### 1. **Vue générale de l'architecture du système :**
- Le système comprend :
  - Un transformateur haute tension (THT).
  - Des capteurs (transducteurs) pour mesurer les courants et les tensions.
  - Des unités de concentration (Merging Units, MU) pour collecter et traiter les données.
  - Des dispositifs électroniques intelligents (IED, Intelligent Electronic Devices) pour le traitement des données.
  - Un système de communication basé sur IEC 61850.

#### 2. **Schéma ASCII de l'architecture :**

```
+-------------------+       +-------------------+       +-------------------+
| Transformateur   |       | Capteurs (CT, VT)  |       | Merging Units    |
| Haute Tension    | <-->  | (Courant et Tension)| <-->  | (MU)              |
+-------------------+       +-------------------+       +-------------------+
                                |                   |
                                | Données numériques|
                                v                   v
                  +-------------------+       +-------------------+
                  | IED de Protection |       | Système de Contrôle|
                  | et Mesure         | <-->  | Substation         |
                  +-------------------+       +-------------------+
```

#### 3. **Description détaillée des interfaces et des éléments :**

##### a) **Capteurs (Transducteurs) :**
- Les capteurs mesurent les grandeurs électriques (courant, tension).
- Modélisation IEC 61850 :
  - **Logical Node (LN)** : MMXU (Mesure de Quantité)
  - **Data Object (DO)** : mag.i (Magnitude du courant), mag.v (Magnitude de la tension).

##### b) **Unités de Concentration (Merging Units, MU) :**
- Les MU collectent les données des capteurs et les transforment en données numériques conformes à IEC 61850.
- Modélisation IEC 61850 :
  - **Logical Device (LD)** : MUGB
  - **Logical Node (LN)** : MMXU, MMTR (Mesure de puissance).
  - **Data Object (DO)** : p (Puissance active), q (Puissance réactive).

##### c) **Dispositifs Électroniques Intelligents (IED) :**
- Les IED traitent les données et effectuent des calculs (puissances, états du système).
- Modélisation IEC 61850 :
  - **Logical Device (LD)** : PROT, CTRL
  - **Logical Node (LN)** : GGIO (Générateur d'Événements), MMXU.
  - **Data Object (DO)** : stVal (Valeurs de状態).

##### d) **Système de Contrôle Substation :**
- Le système central collecte et affiche les données des IED via le protocole MMS.
- Modélisation IEC 61850 :
  - **Service** : MMS (Manufacturing Message Specification).
  - **Communication** : Client/Serveur.

#### 4. **Schéma ASCII des communications :**

```
+-------------------+       +-------------------+       +-------------------+
| Transformateur   | <-->  | Capteurs (CT, VT)  | <-->  | Merging Units    |
| Haute Tension    |       | (Courant et Tension)|       | (MU)              |
+-------------------+       +-------------------+       +-------------------+
                                |                   |
                                v Données numériquesv
                  +-------------------+       +-------------------+
                  | IED de Protection | <----> | Système de Contrôle|
                  | et Mesure         |       | Substation         |
                  +-------------------+       +-------------------+
```

#### 5. **Fonctionnalités et avantages :**
- **Interopérabilité** : Les dispositifs sont compatibles et communicants.
- **Simplicité de configuration** : Grâce à la modélisation standardisée IEC 61850.
- **Réduction des coûts** : Moins d'entretien et une meilleure durabilité.
- **Performance accrue** : Mesures précises et rapides.

#### 6. **Conclusion :**
Cet exemple montre comment IEC 61850 permet de créer un système de mesure et de contrôle cohérent et efficace, en intégrant des dispositifs variés pour une meilleure gestion du transformateur haute tension.

**Sources:**
* **61850-1 Ed2 - TR_draft_V3.pdf**, pages *2, 13*
* **ABB@IEC61850(b).pdf**, page *10*
* **Blair%20-%20Using%20IEC%2061850%20-%20PES%20GM%202013.pdf**, pages *3, 4, 12, 17*
* **IEC 61850 - T_COSTE - R&D EDF.pdf**, page *10*
* **IEC 61850 Fuzzer[1].pdf**, page *10*
* **IEC%2061850%20Overview-Ruggedcom.pdf**, page *39*
* **IEC%2061850_Presentation.pdf**, pages *10, 11*
* **Introduction-to-IEC-61850-Basics-R2_Chi-Carnegie.pdf**, page *3*
* **Introduction-to-IEC-61850-Basics-R2_Chi-Carnegiepdf.pdf**, page *3*
* **N0123_Notes_IEC61850.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.pdf**, page *3*
* **Overview20of20IEC206235120standardspdf.pdf**, page *7*
* **PPT_COPALP IEC61850.pdf**, page *17*
* **Retour_d_experience_EDF_61850.pdf**, page *10*
* **SEREM - iec61850-fra.pdf**, page *1*
* **Siemens - CEI 61850 - Application_examples.pdf**, pages *1, 28, 44*
* **abb_sr_iec_61850_72dpi.pdf**, page *11*
* **iec61850-1{ed2.0}b.pdf**, page *15*
* **iec61850-fra.pdf**, page *1*

---

## Query: Tu peux me faire un exemple complet d'une application qui mesure les puissances dans un transformateur haute tension et qui utiliserait le 61850 ? ajoute des schémas en ascii et détaille bien chaque interface et utilise les mots clés de l'IEC 61850 pour chaque élément. Fais apparaitre la les notions de logical nodes, logical device et IED

### Model: mistral-small:latest

**Response:**

Pour illustrer un exemple complet d'une application qui mesure les puissances dans un transformateur haute tension en utilisant le protocole IEC 61850, nous allons décrire une installation typique avec des schémas ASCII détaillés. Cette application inclura les notions de logical nodes, logical devices et IEDs (Intelligent Electronic Devices).

### Schéma Général

```
+-------------------+
|   Transformateur  |
|    Haute Tension  |
+---------+----------+
          |
          v
+---------------------+
|   Capteur de Courant|
+---------+-----------+
          |
          v
+-------------+--------------------+
|   IED (Relais)|      |   SCL File  |
|    Protection |---->| Configuration|
+-------------+--+    +-------------+

```

### Description des Composants

1. **Transformateur Haute Tension**:
   - Le transformateur est le dispositif principal qui transforme la tension électrique.

2. **Capteur de Courant (CT)**:
   - Les capteurs de courant mesurent les courants électriques dans les enroulements du transformateur.
   - Les données collectées par ces capteurs sont transmises à l'IED via des interfaces physiques.

3. **IED (Relais de Protection)**:
   - L'IED est un dispositif intelligent qui collecte, traite et transmet les données mesurées.
   - Il utilise le protocole IEC 61850 pour la communication.

4. **SCL File**:
   - Le fichier SCL (Substation Configuration Language) contient la configuration des objets logiques et des interfaces de l'IED.
   - Ce fichier est utilisé par l'IEC 61850 client application pour extraire les définitions d'objets du dispositif.

### Logical Nodes

Les logical nodes sont des entités fonctionnelles qui représentent des fonctions spécifiques dans le système. Pour cette application, nous avons les suivants:

- **MMXU (Analog Input Measurement Unit)**:
  - Ce logical node mesure les valeurs analogiques de courant et de tension.
  - Exemple: `MMXU1` pour la mesure du courant.

- **CILO (Control Logic)**:
  - Ce logical node gère la logique de contrôle basée sur les mesures reçues.
  - Exemple: `CILO1` pour la logique de protection contre les surcharges.

### Logical Device

Un logical device est une collection de logical nodes qui partagent des caractéristiques communes et fonctionnent ensemble. Par exemple:

- **LD0 (Protection Logic Device)**:
  - Contient les logical nodes `MMXU1` et `CILO1`.

### IED

L'IED est le dispositif physique qui intègre les logical devices. Dans notre cas, l'IED est le relai de protection.

### Interface entre les Composants

- **Interface Physique**:
  - Les capteurs de courant (CT) sont connectés à l'IED via des interfaces physiques (câbles).
  - Exemple: `MMXU1` reçoit les données de courant du CT via une interface physique.

- **Interface Logique**:
  - Les logical nodes communiquent entre eux via des interfaces logiques définies dans le SCL file.
  - Exemple: `MMXU1` envoie les données mesurées à `CILO1` pour traitement.

### Configuration et Communication

1. **Configuration avec SCL File**:
   - Le fichier SCL configure les objets logiques de l'IED.
   - Exemple:
     ```xml
     <IED name="ProtectionRelay">
       <AccessPoint>
         <Server>
           <LDevice inst="LD0" desc="Protection Logic Device">
             <LNode class="MMXU" inst="1" desc="Analog Input Measurement Unit"/>
             <LNode class="CILO" inst="1" desc="Control Logic"/>
           </LDevice>
         </Server>
       </AccessPoint>
     </IED>
     ```

2. **Communication avec IEC 61850**:
   - L'IEC 61850 client application extrait les définitions d'objets de l'IED via le réseau.
   - Exemple: `MMXU1` envoie des données de courant à l'application cliente qui peut être une HMI (Human Machine Interface) ou un système SCADA.

### Conclusion

Cet exemple montre comment une installation de mesure de puissance dans un transformateur haute tension peut utiliser le protocole IEC 61850 pour assurer une communication efficace et interopérable entre les différents composants. Les logical nodes, logical devices et IEDs jouent des rôles cruciaux dans cette configuration, permettant une intégration fluide et une gestion centralisée des données de mesure.

**Sources:**
* **3BUS095131_en_IEC61850_Overview_and_Benefits_Paper_Generalpdf.pdf**, page *2*
* **61850-1 Ed2 - TR_draft_V3.pdf**, pages *2, 20*
* **ABB@IEC61850(b).pdf**, page *10*
* **Asset-Management-IEC61850_Overview_and_Application-Day-2pdf.pdf**, page *31*
* **Blair%20-%20Using%20IEC%2061850%20-%20PES%20GM%202013.pdf**, pages *3, 4, 12*
* **IEC%2061850-hands-on-training%20program_Stockholm%20November%202-5%202010_v5.pdf**, page *2*
* **IEC%2061850_Presentation.pdf**, pages *10, 11*
* **IEC-61869-9-2016pdf.pdf**, page *9*
* **IEC61850_Overview_and_Benefits_Paper_General.pdf**, page *2*
* **N0123_Notes_IEC61850.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.pdf**, page *3*
* **Overview20of20IEC206235120standardspdf.pdf**, page *7*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331_14h30.doc**, page *0*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331_16h53.doc**, page *0*
* **Siemens - CEI 61850 - Application_examples.pdf**, pages *28, 44*
* **T0994_61850 Network Simulator.pdf**, page *1*
* **iec61850-1{ed2.0}b.pdf**, pages *4, 15*
* **iec61850.pdf**, page *2*

---

### Model: deepseek-r1:32b

**Response:**



### Exemple complet d'une application mesurant les puissances dans un transformateur haute tension selon IEC 61850

#### Contexte de l'application
Nous considérons un système de mesure de puissance dans un transformateur haute tension (THT) au sein d'une sous-station électrique. L'objectif est de mesurer les grandeurs électriques (tension, courant, puissance) et de transmettre ces données via le protocole IEC 61850 pour une surveillance en temps réel.

#### Architecture du système
Le système comprend :
1. Un transformateur haute tension (THT).
2. Des capteurs de tension (PT - Potential Transformer) et de courant (CT - Current Transformer).
3. Une unité de fusion (Merging Unit - MU) qui collecte les valeurs échantillonnées.
4. Un dispositif électronique intelligent (IED - Intelligent Electronic Device), tel qu'un relais de protection ou un système de surveillance.

#### Modélisation selon IEC 61850
##### 1. **Logical Devices (LD)**
- **LD_MU**: Logique device représentant la fonction de fusion dans l'unité de fusion.
- **LD_Relay**: Logique device代表保护继电器的功能。

##### 2. **Logical Nodes (LN)**
- **MMXU** (Measurement, Multi-phase): Utilisé pour mesurer les grandeurs électriques multicycliques (tension, courant, puissance).
- **PTRC** (Protection, Trip Control): Utilisé pour la protection et le contrôle des disjoncteurs.
- **GGIO** (Generic Input/Output): Utilisé pour les entrées/sorties génériques dans l'unité de fusion.

##### 3. **Interfaces et communications**
- **GOOSE (Generic Object Oriented Substation Event)**: Utilisé pour la transmission des données de protection en temps réel.
- **MMS (Manufacturing Messaging Specification)**: Utilisé pour la configuration et la supervision des dispositifs.

#### Schéma ASCII
```
+-------------------+       +-------------------+       +-------------------+
| Transformateur    |       | PT / CT           |       | Merging Unit      |
| Haute Tension (THT) |       | Capteurs          |       | (MU)              |
|                   |       |                   |       | - LD_MU           |
|                   |       |                   |       |   - MMXU_1        |
+-------------------+       +-------------------+       |   - GGIO_1        |
                              |                   |       +-------------------+
                              | Echantillonnage  |
                              v                   v
+-------------------+       +-------------------+       +-------------------+
| IED de Protection |       | Système de        |       | Logiciel de       |
| (Relais)          |       | Surveillance      |       | Supervision       |
| - LD_Relay        |       |                   |       |                   |
|   - MMXU_2        |       +-------------------+       +-------------------+
|   - PTRC_1        |
+-------------------+

Flux de données :
- PT/CT --> MU via échantillonnage
- MU --> IED via GOOSE
- IED --> Système de surveillance via MMS
```

#### Détails des interfaces
##### 1. **Interface entre les capteurs (PT/CT) et l'unité de fusion (MU)**
- Les capteurs PT et CT mesurent respectivement la tension et le courant du transformateur.
- Ces signaux sont envoyés à l'unité de fusion MU sous forme d'échantillons numériques (sampless values).
- L'unité de fusion regroupe ces échantillons pour former des grandeurs électriques cohérentes.

##### 2. **Interface GOOSE entre la MU et l'IED**
- La MU publie les données mesurées sous forme de messages GOOSE.
- Ces messages contiennent les valeurs des grandeurs électriques (tension, courant, puissance).
- L'IED (relais de protection) s'abonne à ces messages pour effectuer des calculs en temps réel.

##### 3. **Interface MMS entre l'IED et le système de surveillance**
- L'IED expose ses données via un serveur MMS.
- Le système de surveillance peut accéder aux informations via ce protocole.
- Les configurations et les paramètres sont également échangés via MMS.

#### Fichier SCL (System Configuration Language)
Le fichier SCL décrit la configuration du système. Voici un exemple simplifié :
```xml
<Substation>
  <VoltageLevel name="VL1">
    <Bay name="THT_Bay">
      <Equipment>
        <PT name="PT_THT" voltage="220kV"/>
        <CT name="CT_THT" current="600A"/>
      </Equipment>
      <MU name="MU_1">
        <LD name="LD_MU">
          <LN class="MMXU" instance="1"/>
          <LN class="GGIO" instance="1"/>
        </LD>
      </MU>
      <IED name="Relay_1">
        <LD name="LD_Relay">
          <LN class="MMXU" instance="2"/>
          <LN class="PTRC" instance="1"/>
        </LD>
      </IED>
    </Bay>
  </VoltageLevel>
</Substation>
```

#### Explications détaillées
- **Logical Devices (LD)**: Chaque IED contient un ou plusieurs LD. Par exemple, `LD_MU` dans l'unité de fusion et `LD_Relay` dans le relais.
- **Logical Nodes (LN)**: Les LN sont des modèles standardisés pour représenter des fonctions spécifiques. Par exemple, `MMXU_1` dans la MU mesure les grandeurs électriques, tandis que `PTRC_1` dans le relais gère la protection.
- **Interfaces**:
  - Les messages GOOSE sont utilisés pour la transmission en temps réel des données de mesure.
  - Le protocole MMS est utilisé pour la configuration et la supervision des dispositifs.

#### Conclusion
Ce exemple montre comment IEC 61850 permet une intégration cohérente et standardisée d'un système de mesure dans une sous-station électrique. Les concepts clés incluent les Logical Devices, Logical Nodes, et les interfaces GOOSE et MMS pour garantir l'interopérabilité entre les différents composants du système.

**Sources:**
* **3BUS095131_en_IEC61850_Overview_and_Benefits_Paper_Generalpdf.pdf**, page *2*
* **61850-1 Ed2 - TR_draft_V3.pdf**, pages *2, 20*
* **ABB@IEC61850(b).pdf**, page *10*
* **Asset-Management-IEC61850_Overview_and_Application-Day-2pdf.pdf**, page *31*
* **Blair%20-%20Using%20IEC%2061850%20-%20PES%20GM%202013.pdf**, pages *3, 4, 12*
* **IEC%2061850-hands-on-training%20program_Stockholm%20November%202-5%202010_v5.pdf**, page *2*
* **IEC%2061850_Presentation.pdf**, pages *10, 11*
* **IEC-61869-9-2016pdf.pdf**, page *9*
* **IEC61850_Overview_and_Benefits_Paper_General.pdf**, page *2*
* **N0123_Notes_IEC61850.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.doc**, page *0*
* **N0123_Notes_IEC61850_20131002.pdf**, page *3*
* **Overview20of20IEC206235120standardspdf.pdf**, page *7*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331_14h30.doc**, page *0*
* **Prj_N0144_Investigation_IEC61850_Av_01_20140331_16h53.doc**, page *0*
* **Siemens - CEI 61850 - Application_examples.pdf**, pages *28, 44*
* **T0994_61850 Network Simulator.pdf**, page *1*
* **iec61850-1{ed2.0}b.pdf**, pages *4, 15*
* **iec61850.pdf**, page *2*

---

