"""IDX (Indonesia Stock Exchange) — comprehensive list of all listed stocks.

This module provides the complete universe of ~900+ stocks listed on the
Indonesia Stock Exchange (IDX), organized by sector for easier maintenance
and filtering. Based on IDX listing data as of July 2026.
"""

from __future__ import annotations

# ── Finance / Banking ──────────────────────────────────────────────────────
FINANCE_BANKING: list[str] = [
    "AGRO",   # Bank Raya Indonesia
    "AGRS",   # Bank IBK Indonesia
    "AMAR",   # Bank Amar Indonesia
    "ARTO",   # Bank Jago
    "BABP",   # Bank MNC Internasional
    "BACA",   # Bank Capital Indonesia
    "BBHI",   # Allo Bank Indonesia
    "BBKP",   # Bank KB Indonesia
    "BBLD",   # Buana Finance
    "BBMD",   # Bank Mestika Dharma
    "BBCA",   # Bank Central Asia
    "BBNI",   # Bank Negara Indonesia (Persero)
    "BBRI",   # Bank Rakyat Indonesia (Persero)
    "BBTN",   # Bank Tabungan Negara (Persero)
    "BBYB",   # Bank Neo Commerce
    "BCAP",   # MNC Kapital Indonesia
    "BCIC",   # Bank JTrust Indonesia
    "BDMN",   # Bank Danamon Indonesia
    "BEKS",   # Bank Pembangunan Daerah Banten
    "BFIN",   # BFI Finance Indonesia
    "BGTG",   # Bank Ganesha
    "BINA",   # Bank Ina Perdana
    "BJBR",   # Bank Pembangunan Daerah Jawa Barat
    "BJTM",   # Bank Pembangunan Daerah Jawa Timur
    "BKSW",   # Bank QNB Indonesia
    "BMAS",   # Bank Maspion Indonesia
    "BMRI",   # Bank Mandiri (Persero)
    "BNBA",   # Bank Bumi Arta
    "BNGA",   # Bank CIMB Niaga
    "BNII",   # Bank Maybank Indonesia
    "BNLI",   # Bank Permata
    "BRIS",   # Bank Syariah Indonesia
    "BSIM",   # Bank Sinarmas
    "BSWD",   # Bank of India Indonesia
    "BTPS",   # Bank BTPN Syariah
    "BTPN",   # Bank SMBC Indonesia
    "BVIC",   # Bank Victoria International
    "CASA",   # Capital Financial Indonesia
    "DNAR",   # Bank Oke Indonesia
    "INPC",   # Bank Artha Graha Internasional
    "MAYA",   # Bank Mayapada Internasional
    "MCOR",   # Bank China Construction Bank Indonesia
    "MEGA",   # Bank Mega
    "NISP",   # Bank OCBC NISP
    "NOBU",   # Bank Nationalnobu
    "PNBN",   # Bank Pan Indonesia
    "PNBS",   # Bank Panin Dubai Syariah
    "SUPA",   # Super Bank Indonesia
    "MASB",   # Bank Multiarta Sentosa
    "BANK",   # Bank Aladin Syariah
]

# ── Finance / Insurance ────────────────────────────────────────────────────
FINANCE_INSURANCE: list[str] = [
    "ABDA",   # Asuransi Bina Dana Arta
    "AHAP",   # Asuransi Harta Aman Pratama
    "AMAG",   # Asuransi Multi Artha Guna
    "AMOR",   # Ashmore Asset Management Indonesia
    "APIC",   # Pacific Strategic Financial
    "ARTA",   # Arthavest
    "ASBI",   # Asuransi Bintang
    "ASDM",   # Asuransi Dayin Mitra
    "ASMI",   # Asuransi Maximus Graha Persada
    "ASRM",   # Asuransi Ramayana
    "ASJT",   # Asuransi Jasa Tania
    "BHAT",   # Bhakti Multi Artha
    "CFIN",   # Clipan Finance Indonesia
    "GSMF",   # Equity Development Investment
    "LIFE",   # MSIG Life Insurance Indonesia
    "LPGI",   # Lippo General Insurance
    "MREI",   # Maskapai Reasuransi Indonesia
    "MTWI",   # Malacca Trust Wuwungan Insurance
    "PANS",   # Panin Sekuritas
    "PNIN",   # Paninvest
    "PNLF",   # Panin Financial
    "TUGU",   # Asuransi Tugu Pratama Indonesia
    "VICO",   # Victoria Investama
    "VINS",   # Victoria Insurance
    "JMAS",   # Asuransi Jiwa Syariah Jasa Mitra Abadi
    "BPFI",   # Woori Finance Indonesia
    "TRIM",   # Trimegah Sekuritas Indonesia
    "ADMF",   # Adira Dinamika Multi Finance
    "WOMF",   # Wahana Ottomitra Multiartha
]

# ── Mining / Coal ──────────────────────────────────────────────────────────
MINING_COAL: list[str] = [
    "ADRO",   # Alamtri Resources Indonesia (was Adaro Energy)
    "AADI",   # Adaro Andalan Indonesia
    "ADMR",   # Alamtri Minerals Indonesia
    "ANTM",   # Aneka Tambang (Persero)
    "ARII",   # Atlas Resources
    "BSSR",   # Baramulti Suksessarana
    "BUMI",   # Bumi Resources
    "BYAN",   # Bayan Resources
    "BRMS",   # Bumi Resources Minerals
    "CITA",   # Cita Mineral Investindo
    "COAL",   # Black Diamond Resources
    "CUAN",   # Petrindo Jaya Kreasi
    "DKFT",   # Central Omega Resources
    "DOID",   # Buma Internasional Grup
    "EMAS",   # Merdeka Gold Resources
    "ENRG",   # Energi Mega Persada
    "GEMS",   # Golden Energy Mines
    "HRUM",   # Harum Energy
    "INCO",   # Vale Indonesia
    "INDY",   # Indika Energy
    "ITMG",   # Indo Tambangraya Megah
    "KKGI",   # Resource Alam Indonesia
    "MBAP",   # Mitrabara Adiperdana
    "MDKA",   # Merdeka Copper Gold
    "MCOL",   # Prima Andalan Mandiri
    "MYOH",   # Samindo Resources
    "NCKL",   # Trimegah Bangun Persada
    "NICL",   # PAM Mineral
    "NICK",   # Charnic Capital
    "NIKL",   # Pelat Timah Nusantara
    "PSAB",   # J Resources Asia Pasifik
    "PTBA",   # Bukit Asam (Persero)
    "PTRO",   # Petrosea
    "RMKE",   # RMK Energy
    "SMMT",   # Golden Eagle Energy
    "TINS",   # Timah
    "TOBA",   # TBS Energi Utama
    "ZINC",   # Kapuas Prima Coal
    "ARTI",   # Ratu Prabu Energi
    "DEWA",   # Darma Henwa
    "IATA",   # MNC Energy Investments
    "ITMA",   # Sumber Energi Andalan
    "PGJO",   # Bahtera Bumi Raya
    "SURE",   # Super Energy
    "KOPI",   # Mitra Energi Persada
    "FIRE",   # Alfa Energi Investama
    "FUTR",   # Futura Energi Global
    "OASA",   # Maharaksa Biru Energi
    "BULL",   # Buana Lintas Lautan
    "AMMN",   # Amman Mineral Internasional
    "ARCI",   # Archi Indonesia
    "PSAT",   # Pancaran Samudera Transport
    "BREN",   # Barito Renewables Energy
    "DSSA",   # Dian Swastatika Sentosa (new code)
    "MORA",   # Mora Telematika Indonesia
    "MBMA",   # Merdeka Battery Materials
]

# ── Consumer Goods / Food & Beverage ──────────────────────────────────────
CONSUMER_FOOD: list[str] = [
    "ADES",   # Akasha Wira International
    "AISA",   # FKS Food Sejahtera
    "ALTO",   # Tri Banyan Tirta
    "AYAM",   # Janu Putra Sejahtera
    "BEEF",   # Estika Tata Tiara
    "BOBA",   # Formosa Ingredient Factory
    "BUDI",   # Budi Starch & Sweetener
    "BUAH",   # Segar Kumala Indonesia
    "CAMP",   # Campina Ice Cream Industry
    "CINT",   # Chitose Internasional
    "CLEO",   # Sariguna Primatirta
    "CMRY",   # Cisarua Mountain Dairy
    "COCO",   # Wahana Interfood Nusantara
    "CPIN",   # Charoen Pokphand Indonesia
    "CPRO",   # Central Proteina Prima
    "DLTA",   # Delta Djakarta
    "DMND",   # Diamond Food Indonesia
    "ENAK",   # Champ Resto Indonesia
    "FAST",   # Fast Food Indonesia
    "FOOD",   # Sentra Food Indonesia
    "GOOD",   # Garudafood Putra Putri Jaya
    "HOKI",   # Buyung Poetra Sembada
    "ICBP",   # Indofood CBP Sukses Makmur
    "INDF",   # Indofood Sukses Makmur
    "JPFA",   # Japfa Comfeed Indonesia
    "KEJU",   # Mulia Boga Raya
    "KINO",   # Kino Indonesia
    "LMPI",   # Langgeng Makmur Industri
    "MAIN",   # Malindo Feedmill
    "MLBI",   # Multi Bintang Indonesia
    "MYOR",   # Mayora Indah
    "NAYZ",   # Hassana Boga Sejahtera
    "PANR",   # Panorama Sentrawisata
    "PZZA",   # Sarimelati Kencana (Pizza Hut)
    "RANC",   # Supra Boga Lestari
    "ROTI",   # Nippon Indosari Corpindo
    "SKLT",   # Sekar Laut
    "SKBM",   # Sekar Bumi
    "SIPD",   # Sreeya Sewu Indonesia
    "STTP",   # Siantar Top
    "TBLA",   # Tunas Baru Lampung
    "TGKA",   # Tigaraksa Satria
    "TSPC",   # Tempo Scan Pacific
    "UCID",   # Uni-Charm Indonesia
    "ULTJ",   # Ultrajaya Milk Industry
    "WMUU",   # Widodo Makmur Unggas
    "WIIM",   # Wismilak Inti Makmur
    "YUPI",   # Yupi Indo Jelly Gum
    "COCO",   # Wahana Interfood Nusantara
    "PDPP",   # Primadaya Plastisindo
]

# ── Consumer Goods / Tobacco ──────────────────────────────────────────────
CONSUMER_TOBACCO: list[str] = [
    "GGRM",   # Gudang Garam
    "HMSP",   # Hanjaya Mandala Sampoerna
    "ITIC",   # Indonesian Tobacco
    "WIIM",   # Wismilak Inti Makmur
]

# ── Consumer Goods / Household & Personal Care ─────────────────────────────
CONSUMER_HOUSEHOLD: list[str] = [
    "ADES",   # Akasha Wira International
    "DVLA",   # Darya-Varia Laboratoria
    "KAEF",   # Kimia Farma
    "KIAS",   # Keramika Indonesia Assosiasi
    "KINO",   # Kino Indonesia
    "MBTO",   # Martina Berto
    "MERK",   # Merck Indonesia
    "MRAT",   # Mustika Ratu
    "PEVE",   # Penta Valent
    "PYFA",   # Pyridam Farma
    "SIDO",   # Sido Muncul
    "TCID",   # Mandom Indonesia
    "UNVR",   # Unilever Indonesia
    "VICI",   # Victoria Care Indonesia
    "IKPM",   # Ikapharmindo Putramas
]

# ── Infrastructure / Telecommunications ───────────────────────────────────
INFRASTRUCTURE: list[str] = [
    "ADHI",   # Adhi Karya (Persero)
    "BALI",   # Bali Towerindo Sentra
    "BUKK",   # Bukaka Teknik Utama
    "CENT",   # Centratama Telekomunikasi Indonesia
    "CMNP",   # Citra Marga Nusaphala Persada
    "EXCL",   # XL Axiata
    "GHON",   # Gihon Telekomunikasi Indonesia
    "ISAT",   # Indosat
    "JSMR",   # Jasa Marga (Persero)
    "LINK",   # Link Net
    "MORA",   # Mora Telematika Indonesia
    "MTEL",   # Dayamitra Telekomunikasi
    "PGEO",   # Pertamina Geothermal Energy
    "POWR",   # Cikarang Listrindo
    "TBIG",   # Tower Bersama Infrastructure
    "TLKM",   # Telekomunikasi Indonesia
    "TOWR",   # Sarana Menara Nusantara
    "WIKA",   # Wijaya Karya (Persero)
    "WSKT",   # Waskita Karya (Persero)
    "PTPP",   # PP (Persero)
    "DGIK",   # Nusa Konstruksi Enjiniring
    "TOTL",   # Total Bangun Persada
    "NRCA",   # Nusa Raya Cipta
    "JKON",   # Jaya Konstruksi Manggala Pratama
    "WEGE",   # Wijaya Karya Bangunan Gedung
    "PBSA",   # Paramita Bangun Sarana
    "ACST",   # Acset Indonusa
    "BIPI",   # Astrindo Nusantara Infrastruktur
    "IBST",   # Inti Bangun Sejahtera
    "KEEN",   # Kencana Energi Lestari
    "ARKO",   # Arkora Hydro
]

# ── Energy / Oil & Gas ────────────────────────────────────────────────────
ENERGY: list[str] = [
    "APEX",   # Apexindo Pratama Duta
    "ELSA",   # Elnusa
    "ENRG",   # Energi Mega Persada
    "ESSA",   # ESSA Industries Indonesia
    "HUMI",   # Humpuss Maritim Internasional
    "INDY",   # Indika Energy
    "MEDC",   # Medco Energi Internasional
    "PGAS",   # Perusahaan Gas Negara (Persero)
    "RAJA",   # Rukun Raharja
    "RATU",   # Raharja Energi Cepu
    "RUIS",   # Radiant Utama Interinsco
    "SGER",   # Sumber Global Energy
    "SURE",   # Super Energy
    "TOBA",   # TBS Energi Utama
    "WOWS",   # Ginting Jaya Energi
    "ELSA",   # Elnusa
    "OILS",   # Indo Oil Perkasa
]

# ── Property / Real Estate ────────────────────────────────────────────────
PROPERTY: list[str] = [
    "APLN",   # Agung Podomoro Land
    "ASRI",   # Alam Sutera Realty
    "BAPA",   # Bekasi Asri Pemula
    "BCIP",   # Bumi Citra Permai
    "BEST",   # Bekasi Fajar Industrial Estate
    "BIPP",   # Bhuwanatala Indah Permai
    "BKDP",   # Bukit Darmo Property
    "BKSL",   # Sentul City
    "BSDE",   # Bumi Serpong Damai
    "CBRE",   # Cakra Buana Resources Energi
    "CBDK",   # Bangun Kosambi Sukses
    "CITY",   # Natura City Developments
    "CLAY",   # Citra Putra Realty
    "CMNP",   # Citra Marga Nusaphala Persada
    "CTRA",   # Ciputra Development
    "DART",   # Duta Anggada Realty
    "DILD",   # Intiland Development
    "DMAS",   # Puradelta Lestari
    "DUTI",   # Duta Pertiwi
    "GAMA",   # Gading Development
    "GMTD",   # Gowa Makassar Tourism Development
    "GPRA",   # Perdana Gapuraprima
    "INPP",   # Indonesian Paradise Property
    "JRPT",   # Jaya Real Property
    "KIJA",   # Kawasan Industri Jababeka
    "KPIG",   # MNC Land
    "LAND",   # Trimitra Propertindo
    "LPCK",   # Lippo Cikarang
    "LPKR",   # Lippo Karawaci
    "MAMI",   # Multi Artha Makmur
    "MDLN",   # Modernland Realty
    "MKPI",   # Metropolitan Kentjana
    "MLPL",   # Multipolar
    "MLND",   # Multi Indocitra
    "MMLP",   # Mega Manunggal Property
    "MPRO",   # Maha Properti Indonesia
    "MTLA",   # Metropolitan Land
    "NIRO",   # City Retail Developments
    "OMRE",   # Indonesia Prima Property
    "PANI",   # Pantai Indah Kapuk Dua
    "PLIN",   # Plaza Indonesia Realty
    "POLI",   # Pollux Hotels Group
    "PPRO",   # Pembangunan Perumahan Properti
    "PWON",   # Pakuwon Jati
    "RBMS",   # Ristia Bintang Mahkotasejati
    "REAL",   # Repower Asia Indonesia
    "RODA",   # Pikko Land Development
    "SATU",   # Kota Satu Properti
    "SMDM",   # Suryamas Dutamakmur
    "SMRA",   # Summarecon Agung
    "TARA",   # Agung Semesta Sejahtera
    "TRIN",   # Perintis Triniti Properti
    "URBN",   # Urban Jakarta Propertindo
    "BUV",    # Bukit Uluwatu Villa (was BUVA)
]

# ── Agriculture / Plantations ─────────────────────────────────────────────
AGRICULTURE: list[str] = [
    "AALI",   # Astra Agro Lestari
    "ADRO",   # Alamtri Resources Indonesia
    "ANJT",   # Austindo Nusantara Jaya
    "BISI",   # BISI International
    "BMSR",   # Bintang Mitra Semestaraya
    "BOLT",   # Garuda Metalindo
    "BTEK",   # Bumi Teknokultura Unggul
    "BWPT",   # Eagle High Plantations
    "CSRA",   # Cisadane Sawit Raya
    "DSNG",   # Dharma Satya Nusantara
    "FAPA",   # FAP Agri
    "GJTL",   # Gajah Tunggal
    "GOLL",   # Golden Plantation (delisted/moved)
    "GULA",   # Aman Agrindo
    "GZCO",   # Gozco Plantations
    "JAWA",   # Jaya Agra Wattie
    "LSIP",   # London Sumatra Indonesia
    "MAGP",   # Multi Agro Gemilang Plantation
    "MGRO",   # Mahkota Group
    "MINA",   # Sanurhasta Mitra
    "NSSS",   # Nusantara Sawit Sejahtera
    "PALM",   # Provident Investasi Bersama
    "PGUN",   # Pradiksi Gunatama
    "PSGO",   # Palma Serasih
    "SIMP",   # Salim Ivomas Pratama
    "SMAR",   # Sinar Mas Agro Resources and Technology
    "SSMS",   # Sawit Sumbermas Sarana
    "STAA",   # Sumber Tani Agung Resources
    "TAPG",   # Triputra Agro Persada
    "TBLA",   # Tunas Baru Lampung
    "TLDN",   # Teladan Prima Agro
    "UNSP",   # Bakrie Sumatera Plantations
    "SGRO",   # Prime Agri Resources
    "UDNG",   # Agro Bahari Nusantara
    "FISH",   # FKS Multi Agro
    "ALII",   # Ancara Logistics Indonesia (was agriculture)
]

# ── Basic Materials / Chemicals ────────────────────────────────────────────
BASIC_MATERIALS: list[str] = [
    "INKP",   # Indah Kiat Pulp & Paper
    "AKPI",   # Argha Karya Prima Industry
    "ALDO",   # Alkindo Naratama
    "ALMI",   # Alumindo Light Metal Industry
    "AMFG",   # Asahimas Flat Glass
    "APLI",   # Asiaplast Industries
    "ARNA",   # Arwana Citramulia
    "BAJA",   # Saranacentral Bajatama
    "BTON",   # Betonjaya Manunggal
    "BRPT",   # Barito Pacific
    "BRNA",   # Berlina
    "BUDI",   # Budi Starch & Sweetener
    "CAKK",   # Cahayaputra Asa Keramik
    "CCSI",   # Communication Cable Systems Indonesia
    "CPIN",   # Charoen Pokphand Indonesia
    "CPRO",   # Central Proteina Prima
    "CTTH",   # Citatah
    "EKAD",   # Ekadharma International
    "EPAC",   # Megalestari Epack Sentosaraya
    "ESIP",   # Sinergi Inti Plastindo
    "FASW",   # Fajar Surya Wisesa
    "FPNI",   # Lotte Chemical Titan
    "GDST",   # Gunawan Dianjaya Steel
    "IGAR",   # Champion Pacific Indonesia
    "IKAI",   # Intikeramik Alamasri Industri
    "IMPC",   # Impack Pratama Industri
    "INCF",   # Indo Komoditi Korpora
    "INCI",   # Intanwijaya Internasional
    "INRU",   # Toba Pulp Lestari
    "IPOL",   # Indopoly Swakarsa Industry
    "ISSP",   # Steel Pipe Industry of Indonesia
    "KBLI",   # KMI Wire and Cable
    "KBLM",   # Kabelindo Murni
    "KIAS",   # Keramika Indonesia Assosiasi
    "KRAS",   # Krakatau Steel (Persero)
    "LION",   # Lion Metal Works
    "LMSH",   # Lionmesh Prima
    "LMPI",   # Langgeng Makmur Industri
    "LTL",    # Lautan Luas
    "MLIA",   # Mulia Industrindo
    "MSJA",   # Multi Spunindo Jaya
    "NIKL",   # Pelat Timah Nusantara
    "PBRX",   # Pan Brothers
    "POLU",   # Golden Flower
    "POWR",   # Cikarang Listrindo
    "PTSN",   # Sat Nusapersada
    "SCCO",   # Supreme Cable Manufacturing
    "SMCB",   # Solusi Bangun Indonesia
    "SMGR",   # Semen Indonesia (Persero)
    "SPMA",   # Suparma
    "SPTO",   # Surya Pertiwi
    "SRSN",   # Indo Acidatama
    "TALF",   # Tunas Alfin
    "TBMS",   # Tembaga Mulia Semanan
    "TFCO",   # Tifico Fiber Indonesia
    "TIRA",   # Tira Austenite
    "TKIM",   # Pabrik Kertas Tjiwi Kimia
    "TPIA",   # Chandra Asri Pacific
    "TRST",   # Trias Sentosa
    "UNIC",   # Unggul Indah Cahaya
    "VOKS",   # Voksel Electric
    "YPAS",   # Yanaprima Hastapersada
    "KBAG",   # Karya Bersama Anugerah
    "SRSN",   # Indo Acidatama
    "CHEM",   # Chemstar Indonesia
]

# ── Industrial / Manufacturing ─────────────────────────────────────────────
INDUSTRIAL: list[str] = [
    "ACES",   # Aspirasi Hidup Indonesia (ACE Hardware)
    "ADMG",   # Polychem Indonesia
    "AMIN",   # Ateliers Mecaniques D'Indonesie
    "ARGO",   # Argo Pantes
    "ASGR",   # Astra Graphia
    "ASII",   # Astra International
    "ASSA",   # Adi Sarana Armada
    "AUTO",   # Astra Otoparts
    "BATA",   # Sepatu Bata
    "BAUT",   # Mitra Angkasa Sejahtera
    "BIMA",   # Primarindo Asia Infrastructure
    "BRAM",   # Indo Kordsa
    "BUKK",   # Bukaka Teknik Utama
    "CARS",   # Industri dan Perdagangan Bintraco Dharma
    "DEPO",   # Caturkarda Depo Bangunan
    "DRMA",   # Dharma Polimetal
    "ERTX",   # Eratex Djaja
    "ESTI",   # Ever Shine Tex
    "FORU",   # Fortune Indonesia
    "GDYR",   # Goodyear Indonesia
    "GGRP",   # Gunung Raja Paksi
    "GJTL",   # Gajah Tunggal
    "HEXA",   # Hexindo Adiperkasa
    "IKBI",   # Sumi Indo Kabel
    "IMAS",   # Indomobil Sukses Internasional
    "INDS",   # Indospring
    "INTA",   # Intraco Penta
    "JECC",   # Jembo Cable Company
    "JSPT",   # Jakarta Setiabudi Internasional
    "KBLI",   # KMI Wire and Cable
    "KBLM",   # Kabelindo Murni
    "KDSI",   # Kedawung Setia Industrial
    "KOBX",   # Kobexindo Tractors
    "KONI",   # Perdana Bangun Pusaka
    "LION",   # Lion Metal Works
    "LMSH",   # Lionmesh Prima
    "LPIN",   # Multi Prima Sejahtera
    "MARK",   # Mark Dynamics Indonesia
    "PACK",   # Abadi Nusantara Hijau Investama
    "PJHB",   # Pelayaran Jaya Hidup Baru
    "PJAA",   # Pembangunan Jaya Ancol
    "LMPI",   # Langgeng Makmur Industri
    "PRIM",   # Royal Prima
    "PTPW",   # Pratama Widya
    "RELI",   # Reliance Sekuritas Indonesia
    "SAPX",   # Satria Antaran Prima
    "SCCO",   # Supreme Cable Manufacturing
    "SMCB",   # Solusi Bangun Indonesia
    "SMGR",   # Semen Indonesia
    "SMSM",   # Selamat Sempurna
    "SOSS",   # Shield On Service
    "STAR",   # Buana Artha Anugerah
    "TIRA",   # Tira Austenite
    "TRIS",   # Trisula International
    "UNIC",   # Unggul Indah Cahaya
    "UNIT",   # Nusantara Pelabuhan Handal (was UNIT)
    "VOKS",   # Voksel Electric
    "WICO",   # Wicaksana Overseas International
    "WOOD",   # Integra Indocabinet
    "TRIS",   # Trisula Textile Industries
    "BELL",   # Trisula Textile Industries
    "SSTM",   # Sunson Textile Manufacturer
    "HADE",   # Himalaya Energi Perkasa
    "KREN",   # Quantum Clovera Investama
    "TRUS",   # Trust Finance Indonesia
    "KBLV",   # First Media
    "ARNA",   # Arwana Citramulia
    "TOTO",   # Surya Toto Indonesia
    "CTBN",   # Citra Tubindo
    "AMFG",   # Asahimas Flat Glass
    "MLBI",   # Multi Bintang Indonesia
]

# ── Trade / Services ──────────────────────────────────────────────────────
TRADE_SERVICES: list[str] = [
    "AKRA",   # AKR Corporindo
    "AMRT",   # Sumber Alfaria Trijaya (Alfamart)
    "ASLC",   # Autopedia Sukses Lestari
    "BIRD",   # Blue Bird
    "CSAP",   # Catur Sentosa Adiprana
    "DAYA",   # Duta Intidaya
    "DNET",   # Indoritel Makmur Internasional
    "DPUM",   # Dua Putra Utama Makmur
    "ECII",   # Electronic City Indonesia
    "EMTK",   # Elang Mahkota Teknologi
    "EPMT",   # Enseval Putera Megatrading
    "ERAA",   # Erajaya Swasembada
    "GRPM",   # Graha Prima Mentari
    "HERO",   # Hero Supermarket (was HERO)
    "HOPE",   # Harapan Duta Pertiwi
    "HRTA",   # Hartadinata Abadi
    "IMJS",   # Indomobil Multi Jasa
    "JARR",   # Jhonlin Agro Raya
    "KOTA",   # DMS Propertindo
    "LPPF",   # MDS Retailing (Matahari)
    "MAPA",   # Map Aktif Adiperkasa
    "MAPB",   # Map Boga Adiperkasa
    "MAPI",   # Mitra Adiperkasa
    "MEGA",   # Bank Mega
    "MIDI",   # Midi Utama Indonesia (Alfamidi)
    "MLPT",   # Multipolar Technology
    "MPMX",   # Mitra Pinasthika Mustika
    "MPPA",   # Matahari Putra Prima
    "MTDL",   # Metrodata Electronics
    "PADI",   # Minna Padi Investama Sekuritas
    "RALS",   # Ramayana Lestari Sentosa
    "RANC",   # Supra Boga Lestari
    "RISE",   # Jaya Sukses Makmur Sentosa
    "SONA",   # Sona Topas Tourism Industry
    "SUPR",   # Solusi Tunas Pratama
    "TELE",   # Omni Inovasi Indonesia
    "TSPC",   # Tempo Scan Pacific
    "UNTR",   # United Tractors
    "WICO",   # Wicaksana Overseas International
    "YULE",   # Yulie Sekuritas Indonesia
    "ZONE",   # Mega Perintis
    "ASGR",   # Astra Graphia
    "SOSS",   # Shield On Service
    "PANS",   # Panin Sekuritas
]

# ── Technology / Media ────────────────────────────────────────────────────
TECHNOLOGY: list[str] = [
    "ATIC",   # Anabatic Technologies
    "BUKA",   # Bukalapak.com
    "COIN",   # Indokripto Koin Semesta
    "CYBR",   # ITSEC Asia
    "DIGI",   # Arkadia Digital Media
    "DIVA",   # Distribusi Voucher Nusantara
    "DMMX",   # Digital Mediatama Maxima
    "EDGE",   # Indointernet
    "ELIT",   # Data Sinergitama Jaya
    "EMTK",   # Elang Mahkota Teknologi
    "ENZO",   # Morenzo Abadi Perkasa
    "FILM",   # MD Entertainment
    "FORU",   # Fortune Indonesia
    "GOTO",   # GoTo Gojek Tokopedia
    "HDIT",   # Hensel Davest Indonesia
    "INET",   # Sinergi Inti Andalan Prima
    "IPTV",   # MNC Vision Networks
    "ITMA",   # Sumber Energi Andalan
    "KIOS",   # Kioson Komersial Indonesia
    "LUCK",   # Sentral Mitra Informatika
    "LUCY",   # Lima Dua Lima Tiga
    "MARI",   # Mahaka Radio Integra
    "MCAS",   # M Cash Integrasi
    "MDIA",   # Intermedia Capital
    "MGNA",   # Magna Investama Mandiri
    "MLPT",   # Multipolar Technology
    "MNCN",   # Media Nusantara Citra
    "MSIN",   # MNC Digital Entertainment
    "MSKY",   # MNC Sky Vision
    "MSTI",   # Mastersystem Infotama
    "MTDL",   # Metrodata Electronics
    "MTPS",   # Meta Epsi
    "NETV",   # MDTV Media Technologies
    "NFCX",   # NFC Indonesia
    "PTSN",   # Sat Nusapersada
    "RAAM",   # Tripar Multivision Plus
    "SCMA",   # Surya Citra Media
    "SEMA",   # Semacom Integrated
    "SILO",   # Siloam International Hospitals
    "SINI",   # Singaraja Putra
    "TELE",   # Omni Inovasi Indonesia
    "TFAS",   # Telefast Indonesia
    "TOSK",   # Topindo Solusi Komunika
    "TRON",   # Teknologi Karya Digital Nusa
    "WIFI",   # Solusi Sinergi Digital
    "WIRG",   # WIR Asia
    "YELO",   # Yelooo Integra Datanet
    "ZYRX",   # Zyrexindo Mandiri Buana
    "AXIO",   # Tera Data Indonusa
    "INOV",   # Inocycle Technology Group
    "ARKA",   # Arkha Jayanti Persada
    "GLVA",   # Galva Technologies
    "RUNS",   # Global Sukses Solusi
]

# ── Healthcare ─────────────────────────────────────────────────────────────
HEALTHCARE: list[str] = [
    "BMHS",   # Bundamedik
    "CARE",   # Metro Healthcare Indonesia
    "CLEO",   # Sariguna Primatirta
    "DGNS",   # Diagnos Laboratorium Utama
    "EMMI",   # Esa Medika Mandiri
    "HEAL",   # Medikaloka Hermina
    "IKPM",   # Ikapharmindo Putramas
    "INAF",   # Indofarma
    "KLBF",   # Kalbe Farma
    "KAEF",   # Kimia Farma
    "MERK",   # Merck Indonesia
    "MIKA",   # Mitra Keluarga Karyasehat
    "MMIX",   # Multi Medika Internasional
    "MTMH",   # Murni Sadar
    "OMED",   # Jayamas Medica Industri
    "PEHA",   # Phapros
    "PRAY",   # Famon Awal Bros Sedaya
    "PRDA",   # Prodia Widyahusada
    "PRDL",   # Prodia Diagnostic Line
    "RSGK",   # Kedoya Adyaraya
    "RSCH",   # Charlie Hospital Semarang
    "SAME",   # Sarana Meditama Metropolitan
    "SILO",   # Siloam International Hospitals
    "SOHO",   # Soho Global Health
    "LIFE",   # MSIG Life Insurance Indonesia
    "SRAJ",   # Sejahteraraya Anugrahjaya
    "LABS",   # UBC Medical Indonesia
    "OBAT",   # Brigit Biofarmaka Technologi
    "CHEK",   # Diastika Biotekindo
    "DKHH",   # Cipta Sarana Medika
    "MEDS",   # Hetzer Medical Indonesia
]

# ── Transportation / Logistics ─────────────────────────────────────────────
TRANSPORTATION: list[str] = [
    "BBRM",   # Pelayaran Nasional Bina Buana Raya
    "BIRD",   # Blue Bird
    "BLTA",   # Berlian Laju Tanker
    "BOAT",   # Newport Marine Services
    "BPTR",   # Batavia Prosperindo Trans
    "BSML",   # Bintang Samudera Mandiri Lines
    "BULL",   # Buana Lintas Lautan
    "CMPP",   # AirAsia Indonesia
    "ELPI",   # Pelayaran Nasional Ekalya Purnamasari
    "GMFI",   # Garuda Maintenance Facility Aero Asia
    "GIAA",   # Garuda Indonesia (Persero)
    "HAIS",   # Hasnur Internasional Shipping
    "HATM",   # Habco Trans Maritima
    "HITS",   # Humpuss Intermoda Transportasi
    "HUMI",   # Humpuss Maritim Internasional
    "IPCC",   # Indonesia Kendaraan Terminal
    "IPCM",   # Jasa Armada Indonesia
    "JAYA",   # Armada Berjaya Trans
    "KARW",   # Meratus Jasa Prima
    "KIJA",   # Kawasan Industri Jababeka
    "LRNA",   # Eka Sari Lorena Transport
    "MBSS",   # Mitrabahtera Segara Sejati
    "MIRA",   # Mitra International Resources
    "MPOW",   # Megapower Makmur
    "NELY",   # Pelayaran Nelly Dwi Putri
    "PSSI",   # IMC Pelita Logistik
    "PPGL",   # Prima Globalindo Logistik
    "PORT",   # Nusantara Pelabuhan Handal
    "SDMU",   # Sidomulyo Selaras
    "SHIP",   # Sillo Maritime Perdana
    "SMDR",   # Samudera Indonesia
    "SOCI",   # Soechi Lines
    "TAMU",   # Pelayaran Tamarin Samudra
    "TCPI",   # Transcoal Pacific
    "TMAS",   # Temas
    "TPMA",   # Trans Power Marine
    "TRJA",   # Transkon Jaya
    "WINS",   # Wintermar Offshore Marine
    "WEHA",   # WEHA Transportasi Indonesia
    "PJHB",   # Pelayaran Jaya Hidup Baru
    "LEAD",   # Logindo Samudramakmur
    "BOLT",   # Garuda Metalindo
    "DPNS",   # Duta Pertiwi Nusantara
    "KJEN",   # Krida Jaringan Nusantara
    "SBMA",   # Surya Biru Murni Acetylene
    "TRUK",   # Guna Timur Raya
    "RIGS",   # Rig Tenders Indonesia
    "WAPO",   # Wahana Pronatural
    "LAJU",   # Jasa Berdikari Logistics
]

# ── Hotels / Tourism / Entertainment ──────────────────────────────────────
HOTELS_TOURISM: list[str] = [
    "BAYU",   # Bayu Buana
    "BOLT",   # Garuda Metalindo
    "BOLA",   # Bali Bintang Sejahtera
    "EAST",   # Eastparc Hotel
    "FITT",   # Hotel Fitra International
    "GMTD",   # Gowa Makassar Tourism Development
    "GOLF",   # Intra Golflink Resorts
    "HILL",   # Hillcon
    "HOMI",   # Grand House Mulia
    "HOTL",   # Saraswanti Indoland Development
    "ICON",   # Island Concepts Indonesia
    "INPP",   # Indonesian Paradise Property
    "JIHD",   # Jakarta International Hotels & Development
    "KPIG",   # MNC Land
    "MARI",   # Mahaka Radio Integra
    "MINA",   # Sanurhasta Mitra
    "PDES",   # Destinasi Tirta Nusantara
    "PLAN",   # Planet Properindo Jaya
    "POLI",   # Pollux Hotels Group
    "PSDN",   # Prasidha Aneka Niaga
    "PTSP",   # Pioneerindo Gourmet International
    "PUDP",   # Pudjiadi Prestige
    "SHID",   # Hotel Sahid Jaya International
    "SNLK",   # Sunter Lakeside Hotel
    "SONA",   # Sona Topas Tourism Industry
    "CSIS",   # Cahayasakti Investindo Sukses
]

# ── Investment Companies ──────────────────────────────────────────────────
INVESTMENT: list[str] = [
    "AMMN",   # Amman Mineral Internasional
    "ARTA",   # Arthavest
    "BBHI",   # Allo Bank Indonesia
    "BHIT",   # MNC Asia Holding
    "BNBR",   # Bakrie & Brothers
    "BPII",   # Batavia Prosperindo Internasional
    "BUKK",   # Bukaka Teknik Utama
    "CITA",   # Cita Mineral Investindo
    "DNET",   # Indoritel Makmur Internasional
    "DSFI",   # Dharma Samudera Fishing Industries
    "IATA",   # MNC Energy Investments
    "LPIN",   # Multi Prima Sejahtera
    "MAPA",   # Map Aktif Adiperkasa
    "MAPI",   # Mitra Adiperkasa
    "MDIA",   # Intermedia Capital
    "MEGA",   # Bank Mega
    "MLPL",   # Multipolar
    "MYTX",   # Asia Pacific Investama
    "PALM",   # Provident Investasi Bersama
    "PNIN",   # Paninvest
    "PNLF",   # Panin Financial
    "SMMA",   # Sinar Mas Multiartha
    "SRTG",   # Saratoga Investama Sedaya
    "SUPR",   # Solusi Tunas Pratama
    "TRIM",   # Trimegah Sekuritas Indonesia
    "UNIT",   # Nusantara Pelabuhan Handal
    "WIIM",   # Wismilak Inti Makmur
]

# ── Miscellaneous / Others ────────────────────────────────────────────────
MISCELLANEOUS: list[str] = [
    "ABBA",   # Mahaka Media
    "AGAR",   # Asia Sejahtera Mina
    "AIMS",   # Artha Mahiya Investama
    "AKSI",   # Mineral Sumberdaya Mandiri
    "ALKA",   # Alakasa Industrindo
    "AMAN",   # Makmur Berkah Amanda
    "AMMS",   # Agung Menjangan Mas
    "APII",   # Arita Prima Indonesia
    "ARTA",   # Arthavest
    "ARTO",   # Bank Jago
    "ASLI",   # Asri Karya Lestari
    "ASPR",   # Asia Pramulia
    "ATAP",   # Trimitra Prawara Goldland
    "ATLA",   # Atlantis Subsea Indonesia
    "BABY",   # Multitrend Indo
    "BACH",   # Bach Multi Global
    "BAIK",   # Bersama Mencapai Puncak
    "BALI",   # Bali Towerindo Sentra
    "BAPA",   # Bekasi Asri Pemula
    "BAPR",   # Bakrie Pipe Industries
    "BATR",   # Benteng Api Technic
    "BBIA",   # Sumber Mineral Global Abadi
    "BBSS",   # Bumi Benowo Sukses Sejahtera
    "BDKR",   # Berdikari Pondasi Perkasa
    "BEBE",   # Berkah Beton Sadaya
    "BIKA",   # Binakarya Jaya Abadi
    "BIKE",   # Sepeda Bersama Indonesia
    "BIMA",   # Primarindo Asia Infrastructure
    "BINO",   # Perma Plasindo
    "BLES",   # Superior Prima Sukses
    "BLTZ",   # Graha Layar Prima
    "BLUE",   # Berkah Prima Perkasa
    "BMBL",   # Lavender Bina Cendikia
    "BMSR",   # Bintang Mitra Semestaraya
    "BOLT",   # Garuda Metalindo
    "BPFI",   # Woori Finance Indonesia
    "BPII",   # Batavia Prosperindo Internasional
    "BPTR",   # Batavia Prosperindo Trans
    "BSBK",   # Wulandari Bangun Laksana
    "BSML",   # Bintang Samudera Mandiri Lines
    "BTON",   # Betonjaya Manunggal
    "BUVA",   # Bukit Uluwatu Villa
    "CASH",   # Cashlez Worldwide Indonesia
    "CBPE",   # Citra Buana Prasida
    "CBUT",   # Citra Borneo Utama
    "CCSI",   # Communication Cable Systems Indonesia
    "CEKA",   # Wilmar Cahaya Indonesia
    "CHEK",   # Diastika Biotekindo
    "CHIP",   # Pelita Teknologi Global
    "CITY",   # Natura City Developments
    "CNMA",   # Nusantara Sejahtera Raya
    "CNKO",   # Exploitasi Energi Indonesia
    "COCO",   # Wahana Interfood Nusantara
    "COAL",   # Black Diamond Resources
    "CPRO",   # Central Proteina Prima
    "CRAB",   # Toba Surimi Industries
    "CRSN",   # Carsurin
    "CSMI",   # Cipta Selera Murni
    "CYBR",   # ITSEC Asia
    "DADA",   # Diamond Citra Propertindo
    "DAAZ",   # Daaz Bara Lestari
    "DADP",   # Damai Sejahtera Abadi (was UFOE)
    "DATA",   # Remala Abadi
    "DEFI",   # Danasupra Erapacific
    "DEWI",   # Dewi Shri Farmindo
    "DGNS",   # Diagnos Laboratorium Utama
    "DIGI",   # Arkadia Digital Media
    "DIVI",   # Distribusi Voucher Nusantara (was DIVA)
    "DKFT",   # Central Omega Resources
    "DOSS",   # Global Sukses Digital
    "DPNS",   # Duta Pertiwi Nusantara
    "DWGL",   # Dwi Guna Laksana
    "DYAN",   # Dyandra Media International
    "ECOC",   # Ecocare Indo Pasifik (was HYGN)
    "ELTY",   # Bakrieland Development
    "EMDE",   # Megapolitan Developments
    "EPAC",   # Megalestari Epack Sentosaraya
    "ERAL",   # Sinar Eka Selaras
    "ESIP",   # Sinergi Inti Plastindo
    "ESTA",   # Esta Multi Usaha
    "ESTI",   # Ever Shine Tex
    "EURO",   # Estee Gold Feet
    "FIMP",   # Fimperkasa Utama
    "FLMC",   # Falmaco Nonwoven Industri
    "FOLK",   # Multi Garam Utama
    "FORU",   # Fortune Indonesia
    "FWCT",   # Wijaya Cahaya Timber
    "GAMA",   # Gading Development
    "GEMA",   # Gema Grahasarana
    "GEMS",   # Golden Energy Mines
    "GLOB",   # Globe Kita Terang
    "GOLD",   # Visi Telekomunikasi Infrastruktur
    "GOLF",   # Intra Golflink Resorts
    "GPRA",   # Perdana Gapuraprima
    "GPSO",   # Geoprima Solusi
    "GULA",   # Aman Agrindo
    "GUN",    # Gunanusa Eramandiri (was GUNA)
    "GWSA",   # Greenwood Sejahtera
    "HADE",   # Himalaya Energi Perkasa
    "HALO",   # Haloni Jane
    "HBAT",   # Minahasa Membangun Hebat
    "HDIT",   # Hensel Davest Indonesia
    "HGII",   # Hero Global Investment
    "HILL",   # Hillcon
    "HOPE",   # Harapan Duta Pertiwi
    "HRME",   # Menteng Heritage Realty
    "HYGN",   # Ecocare Indo Pasifik
    "IBFN",   # Intan Baru Prana
    "IBOS",   # Indo Boga Sukses
    "IKAN",   # Era Mandiri Cemerlang
    "IKBI",   # Sumi Indo Kabel
    "INA",    # Indal Aluminium Industry (was INAI)
    "INCF",   # Indo Komoditi Korpora
    "INDX",   # Tanah Laut
    "INPS",   # Indah Prakasa Sentosa
    "INTA",   # Intraco Penta
    "INTD",   # Inter Delta
    "IOTF",   # Sumber Sinergi Makmur
    "IPAC",   # Era Graharealty
    "IPOL",   # Indopoly Swakarsa Industry
    "IRRA",   # Itama Ranoraya
    "IRSX",   # Folago Global Nusantara
    "ISAP",   # Isra Presisi Indonesia
    "ISEA",   # Indo American Seafoods
    "ITIC",   # Indonesian Tobacco
    "JAST",   # Jasnita Telekomindo
    "JAWA",   # Jaya Agra Wattie
    "JECX",   # Nitrasanata Dharma
    "JECC",   # Jembo Cable Company
    "JELI",   # Niramas Utama
    "JGLE",   # Graha Andrasentra Propertindo
    "KBLV",   # First Media
    "KBLM",   # Kabelindo Murni
    "KDTN",   # Puri Sentul Permai
    "KETR",   # Ketrosden Triasmitra
    "KING",   # Hoffmen Cleanindo
    "KLAS",   # Pelayaran Kurnia Lautan Semesta
    "KLIN",   # Klinko Karya Imaji
    "KMDS",   # Kurniamitra Duta Sentosa
    "KMTR",   # Kirana Megatara
    "KOBX",   # Kobexindo Tractors
    "KOCE",   # Kokoh Exa Nusantara (was KOCI)
    "KOIN",   # Kokoh Inti Arebama
    "KOKA",   # Koka Indonesia
    "KOTA",   # DMS Propertindo
    "KRYA",   # Bangun Karya Perkasa Jaya
    "KSIX",   # Kentanix Supra International
    "KUAS",   # Ace Oldfields
    "LAPD",   # Leyand International
    "LCKM",   # LCK Global Kedaton
    "LFLP",   # Imago Mulia Persada
    "LMAX",   # Lupromax Pelumas Indonesia
    "LOPI",   # Logisticsplus International
    "LPPS",   # Lenox Pasifik Investama
    "LRNA",   # Eka Sari Lorena Transport
    "MANG",   # Manggung Polahraya
    "MASB",   # Bank Multiarta Sentosa
    "MAXI",   # Maxindo Karya Anugerah
    "MDRN",   # Modern Internasional
    "MDKI",   # Emdeki Utama
    "MDLN",   # Modernland Realty
    "MDPL",   # Mega Manunggal Property (was MMLP)
    "MEJA",   # Harta Djaya Karya
    "MENN",   # Menn Teknologi Indonesia
    "MERE",   # Merry Riana Edukasi
    "MFMI",   # Multifiling Mitra Indonesia
    "MIRA",   # Mitra International Resources
    "MITI",   # Mitra Investindo
    "MKN",    # Mitra Komunikasi Nusantara
    "MKTR",   # Menthobi Karyatama Raya
    "MOLI",   # Madusari Murni Indah
    "MPOW",   # Megapower Makmur
    "MPXL",   # MPX Logistics International
    "MTFN",   # Capitalinc Investment
    "MTPS",   # Meta Epsi
    "MTSM",   # Metro Realty
    "MUTU",   # Mutuagung Lestari
    "MYTX",   # Asia Pacific Investama
    "NAIK",   # Adiwarna Anugerah Abadi
    "NANO",   # Nanotech Indonesia Global
    "NASA",   # Andalan Perkasa Abadi
    "NASI",   # Wahana Inti Makmur
    "NATO",   # Olympus Strategic Indonesia
    "NETV",   # MDTV Media Technologies
    "NICE",   # Adhi Kartiko Pratama
    "NINE",   # Techno9 Indonesia
    "NPGF",   # Nusa Palapa Gemilang
    "NTBK",   # Nusatama Berkah
    "NZIA",   # Nusantara Almazia
    "OBMD",   # OBM Drilchem
    "OKAS",   # Ancora Indonesia Resources
    "OLIV",   # Oscar Mitra Sukses Sejahtera
    "OMRE",   # Indonesia Prima Property
    "OPMS",   # Optima Prima Metal Sinergi
    "PADA",   # Personel Alih Daya
    "PADI",   # Minna Padi Investama Sekuritas
    "PAMG",   # Bima Sakti Pertiwi
    "PBSA",   # Paramita Bangun Sarana
    "PCAR",   # Prima Cakrawala Abadi
    "PEHA",   # Phapros
    "PGJO",   # Bahtera Bumi Raya
    "PGLI",   # Pembangunan Graha Lestari Indah
    "PICO",   # Pelangi Indah Canindo
    "PIPE",   # Indo Pureco Pratama (was IPPE)
    "PLAN",   # Planet Properindo Jaya
    "PMMP",   # Panca Mitra Multiperdana
    "PNSE",   # Pudjiadi and Sons
    "POLA",   # Pool Advista Finance
    "POLY",   # Asia Pacific Fibers
    "PPRE",   # PP Presisi
    "PRIM",   # Royal Prima
    "PTDU",   # Djasa Ubersakti
    "PTIS",   # Indo Straits
    "PTMR",   # Master Print
    "PTMP",   # Mitra Pack
    "PTPW",   # Pratama Widya
    "PTSP",   # Pioneerindo Gourmet International
    "PURA",   # Putra Rajawali Kencana
    "PURI",   # Puri Global Sukses
    "RANC",   # Supra Boga Lestari
    "RBM",    # Ristia Bintang Mahkotasejati (was RBMS)
    "RCC",    # Utama Radar Cahaya (was RCCC)
    "RELF",   # Graha Mitra Asia
    "RGAS",   # Kian Santang Muliatama
    "RICY",   # Ricky Putra Globalindo
    "RMKO",   # Royaltama Mulia Kontraktorindo
    "RONY",   # Aesler Grup Internasional
    "SAFE",   # Steady Safe
    "SAGE",   # Saptausaha Gemilangindah
    "SAMF",   # Saraswanti Anugerah Makmur
    "SATU",   # Kota Satu Properti
    "SBM",    # Surya Biru Murni Acetylene (was SBMA)
    "SCNP",   # Selaras Citra Nusantara Perkasa
    "SDPC",   # Millennium Pharmacon International
    "SICO",   # Sigma Energy Compressindo
    "SIMP",   # Salim Ivomas Pratama
    "SKRN",   # Superkrane Mitra Utama
    "SLIS",   # Gaya Abadi Sempurna
    "SLJA",   # SLJ Global (was SULI)
    "SMIL",   # Sarana Mitra Luas
    "SMKM",   # Sumber Mas Konstruksi
    "SMLE",   # Sinergi Multi Lestarindo
    "SOCA",   # Soechi Lines (was SOCI)
    "SOFA",   # Solusi Environment Asia
    "SOLA",   # Xolare RCR Energy
    "SOTS",   # Satria Mega Kencana
    "SOUL",   # Mitra Tirta Buwana
    "SPRE",   # Soraya Berjaya Indonesia
    "SSTM",   # Sunson Textile Manufacturer
    "SUNI",   # Sunindo Pratama
    "SURI",   # Maja Agung Latexindo
    "SWID",   # Saraswanti Indoland Development
    "TAMA",   # Lancartama Sejati
    "TAMU",   # Pelayaran Tamarin Samudra
    "TARA",   # Agung Semesta Sejahtera
    "TAYS",   # Jaya Swarasa Agung
    "TEBE",   # Dana Brata Luhur
    "TIRT",   # Tirta Mahakam Resources
    "TIRA",   # Tira Austenite
    "TNCA",   # Trimuda Nuansa Citra
    "TOOL",   # Rohartindo Nusantara Luas
    "TOPS",   # Totalindo Eka Persada
    "TRGU",   # Cerestar Indonesia
    "TRIN",   # Perintis Triniti Properti
    "TRJA",   # Transkon Jaya
    "TRON",   # Teknologi Karya Digital Nusa
    "TRUE",   # Triniti Dinamik
    "TRUK",   # Guna Timur Raya
    "UANG",   # Pakuan
    "UFOE",   # Damai Sejahtera Abadi
    "UNIT",   # Nusantara Pelabuhan Handal
    "UNIQ",   # Ulima Nitra
    "UNTD",   # Terang Dunia Internusa
    "UVCR",   # Trimegah Karya Pratama
    "VAST",   # Vastland Indonesia
    "VENT",   # Venteny Fortuna International (was VTNY)
    "VERN",   # Verona Indah Pictures
    "VIVA",   # Visi Media Asia
    "VRNA",   # Mizuho Leasing Indonesia
    "WAPO",   # Wahana Pronatural
    "WBSA",   # BSA Logistics Indonesia
    "WEHA",   # WEHA Transportasi Indonesia
    "WGSH",   # Wira Global Solusi
    "WIDI",   # Widiant Jaya Krenindo
    "WINR",   # Winner Nusantara Jaya
    "WINS",   # Wintermar Offshore Marine
    "WINE",   # Hatten Bali
    "WIRG",   # WIR Asia
    "WMPP",   # Widodo Makmur Perkasa
    "WSBP",   # Waskita Beton Precast
    "WTON",   # Wijaya Karya Beton
    "XISI",   # Ciptadana Properti Ritel Indonesia
    "YELO",   # Yelooo Integra Datanet (formerly YELO)
    "YOUR",   # Roda Vivatex (was RDTX)
    "ZBRA",   # Dosni Roha Indonesia
    "ZINC",   # Kapuas Prima Coal
    "ZONE",   # Mega Perintis
    "ZYRX",   # Zyrexindo Mandiri Buana
    "ABMM",   # ABM Investama
    "ARKA",   # Arkha Jayanti Persada
    "BBSS",   # Bumi Benowo Sukses Sejahtera
    "BEER",   # Jobubu Jarum Minahasa
    "BELL",   # Trisula Textile Industries
    "BESS",   # Batulicin Nusantara Maritim
    "BIKE",   # Sepeda Bersama Indonesia
    "BINO",   # Perma Plasindo
    "BLES",   # Superior Prima Sukses
    "BMSR",   # Bintang Mitra Semestaraya
    "BOAT",   # Newport Marine Services
    "BPFI",   # Woori Finance Indonesia
    "BPTR",   # Batavia Prosperindo Trans
    "BRRC",   # Raja Roti Cemerlang
    "BSBK",   # Wulandari Bangun Laksana
    "BUVA",   # Bukit Uluwatu Villa
    "CAKK",   # Cahayaputra Asa Keramik
    "CARS",   # Bintraco Dharma
    "CASH",   # Cashlez Worldwide Indonesia
    "CBPE",   # Citra Buana Prasida
    "CGAS",   # Citra Nusantara Gemilang
    "CHIP",   # Pelita Teknologi Global
    "CMPP",   # AirAsia Indonesia
    "CNKO",   # Exploitasi Energi Indonesia
    "COCO",   # Wahana Interfood Nusantara
    "CRAB",   # Toba Surimi Industries
    "CRSN",   # Carsurin
    "CSMI",   # Cipta Selera Murni
    "CSIS",   # Cahayasakti Investindo Sukses
    "DADP",   # Damai Sejahtera Abadi
    "DATA",   # Remala Abadi
    "DEFI",   # Danasupra Erapacific
    "DGNS",   # Diagnos Laboratorium Utama
    "DKHH",   # Cipta Sarana Medika
    "DOSS",   # Global Sukses Digital
    "DPNS",   # Duta Pertiwi Nusantara
    "DSFI",   # Dharma Samudera Fishing Industries
    "DWGL",   # Dwi Guna Laksana
    "DYAN",   # Dyandra Media International
    "ECII",   # Electronic City Indonesia
    "ELIT",   # Data Sinergitama Jaya
    "EMDE",   # Megapolitan Developments
    "ENZO",   # Morenzo Abadi Perkasa
    "ERAL",   # Sinar Eka Selaras
    "ESIP",   # Sinergi Inti Plastindo
    "ESTA",   # Esta Multi Usaha
    "EURO",   # Estee Gold Feet
    "FIMP",   # Fimperkasa Utama
    "FIRE",   # Alfa Energi Investama
    "FLMC",   # Falmaco Nonwoven Industri
    "FOLK",   # Multi Garam Utama
    "FORU",   # Fortune Indonesia
    "FWCT",   # Wijaya Cahaya Timber
    "GLOB",   # Globe Kita Terang
    "GOLD",   # Visi Telekomunikasi Infrastruktur
    "GPSO",   # Geoprima Solusi
    "GTBO",   # Garda Tujuh Buana
    "GTRA",   # Grahaprima Suksesmandiri
    "GULA",   # Aman Agrindo
    "GWSA",   # Greenwood Sejahtera
    "HALO",   # Haloni Jane
    "HBAT",   # Minahasa Membangun Hebat
    "HDIT",   # Hensel Davest Indonesia
    "HGII",   # Hero Global Investment
    "HILL",   # Hillcon
    "HRME",   # Menteng Heritage Realty
    "IBFN",   # Intan Baru Prana
    "IBOS",   # Indo Boga Sukses
    "IKAN",   # Era Mandiri Cemerlang
    "INCF",   # Indo Komoditi Korpora
    "INDX",   # Tanah Laut
    "INOV",   # Inocycle Technology Group
    "INPS",   # Indah Prakasa Sentosa
    "INTD",   # Inter Delta
    "IOTF",   # Sumber Sinergi Makmur
    "IPAC",   # Era Graharealty
    "IRRA",   # Itama Ranoraya
    "ISAP",   # Isra Presisi Indonesia
    "ISEA",   # Indo American Seafoods
    "JAST",   # Jasnita Telekomindo
    "JAYA",   # Armada Berjaya Trans
    "JEJE",   # Jaya Swarasa Agung (was JEJE)
    "JELI",   # Niramas Utama
    "JGLE",   # Graha Andrasentra Propertindo
    "KARW",   # Meratus Jasa Prima
    "KBAG",   # Karya Bersama Anugerah
    "KBLV",   # First Media
    "KDTN",   # Puri Sentul Permai
    "KETR",   # Ketrosden Triasmitra
    "KIOS",   # Kioson Komersial Indonesia
    "KLAS",   # Pelayaran Kurnia Lautan Semesta
    "KLIN",   # Klinko Karya Imaji
    "KMDS",   # Kurniamitra Duta Sentosa
    "KMTR",   # Kirana Megatara
    "KOBX",   # Kobexindo Tractors
    "KOIN",   # Kokoh Inti Arebama
    "KOKA",   # Koka Indonesia
    "KOPI",   # Mitra Energi Persada
    "KREN",   # Quantum Clovera Investama
    "KRYA",   # Bangun Karya Perkasa Jaya
    "KSIX",   # Kentanix Supra International
    "KUAS",   # Ace Oldfields
    "LAPD",   # Leyand International
    "LCKM",   # LCK Global Kedaton
    "LEAD",   # Logindo Samudramakmur
    "LFLP",   # Imago Mulia Persada
    "LMAX",   # Lupromax Pelumas Indonesia
    "LOPI",   # Logisticsplus International
    "LPPS",   # Lenox Pasifik Investama
    "MANG",   # Manggung Polahraya
    "MAXI",   # Maxindo Karya Anugerah
    "MDKI",   # Emdeki Utama
    "MDRN",   # Modern Internasional
    "MEJA",   # Harta Djaya Karya
    "MENN",   # Menn Teknologi Indonesia
    "MGLV",   # Panca Anugerah Wisesa
    "MIRA",   # Mitra International Resources
    "MITI",   # Mitra Investindo
    "MKTR",   # Menthobi Karyatama Raya
    "MOLI",   # Madusari Murni Indah
    "MPIX",   # Mitra Pedagang Indonesia
    "MPOW",   # Megapower Makmur
    "MPXL",   # MPX Logistics International
    "MSIE",   # Multisarana Intan Eduka
    "MTPS",   # Meta Epsi
    "MTSM",   # Metro Realty
    "MUTU",   # Mutuagung Lestari
    "NAIK",   # Adiwarna Anugerah Abadi
    "NANO",   # Nanotech Indonesia Global
    "NASA",   # Andalan Perkasa Abadi
    "NASI",   # Wahana Inti Makmur
    "NINE",   # Techno9 Indonesia
    "NPGF",   # Nusa Palapa Gemilang
    "NTBK",   # Nusatama Berkah
    "NZIA",   # Nusantara Almazia
    "OBMD",   # OBM Drilchem
    "OILS",   # Indo Oil Perkasa
    "OKAS",   # Ancora Indonesia Resources
    "OLIV",   # Oscar Mitra Sukses Sejahtera
    "OPMS",   # Optima Prima Metal Sinergi
    "PADA",   # Personel Alih Daya
    "PAMG",   # Bima Sakti Pertiwi
    "PBSA",   # Paramita Bangun Sarana
    "PCAR",   # Prima Cakrawala Abadi
    "PDPP",   # Primadaya Plastisindo
    "PEGE",   # Panca Global Kapital
    "PGJO",   # Bahtera Bumi Raya
    "PGLI",   # Pembangunan Graha Lestari Indah
    "PICO",   # Pelangi Indah Canindo
    "PIPE",   # Indo Pureco Pratama
    "PKPK",   # Paragon Karya Perkasa
    "PLAN",   # Planet Properindo Jaya
    "PMMP",   # Panca Mitra Multiperdana
    "POLY",   # Asia Pacific Fibers
    "PPRI",   # Paperocks Indonesia
    "PRIM",   # Royal Prima
    "PTMP",   # Mitra Pack
    "PTPW",   # Pratama Widya
    "PTSN",   # Sat Nusapersada
    "PURA",   # Putra Rajawali Kencana
    "PURI",   # Puri Global Sukses
    "PZZA",   # Sarimelati Kencana
    "RBM",    # Ristia Bintang Mahkotasejati
    "RCC",    # Utama Radar Cahaya
    "REAL",   # Repower Asia Indonesia
    "RELF",   # Graha Mitra Asia
    "RGAS",   # Kian Santang Muliatama
    "RICY",   # Ricky Putra Globalindo
    "RMKO",   # Royaltama Mulia Kontraktorindo
    "RODA",   # Pikko Land Development
    "RONY",   # Aesler Grup Internasional
    "SAGE",   # Saptausaha Gemilangindah
    "SAPX",   # Satria Antaran Prima
    "SATU",   # Kota Satu Properti
    "SCNP",   # Selaras Citra Nusantara Perkasa
    "SDPC",   # Millennium Pharmacon International
    "SICO",   # Sigma Energy Compressindo
    "SKRN",   # Superkrane Mitra Utama
    "SLIS",   # Gaya Abadi Sempurna
    "SMIL",   # Sarana Mitra Luas
    "SMKM",   # Sumber Mas Konstruksi
    "SMLE",   # Sinergi Multi Lestarindo
    "SNLK",   # Sunter Lakeside Hotel
    "SOSS",   # Shield On Service
    "SOTS",   # Satria Mega Kencana
    "SOUL",   # Mitra Tirta Buwana
    "SPRE",   # Soraya Berjaya Indonesia
    "SSTM",   # Sunson Textile Manufacturer
    "SUNI",   # Sunindo Pratama
    "SURI",   # Maja Agung Latexindo
    "SWAT",   # Sriwahana Adityakarta
    "SWID",   # Saraswanti Indoland Development
    "TARA",   # Agung Semesta Sejahtera
    "TAYS",   # Jaya Swarasa Agung
    "TEBE",   # Dana Brata Luhur
    "TFAS",   # Telefast Indonesia
    "TGUK",   # Platinum Wahab Nusantara
    "TIRT",   # Tirta Mahakam Resources
    "TNCA",   # Trimuda Nuansa Citra
    "TOOL",   # Rohartindo Nusantara Luas
    "TOPS",   # Totalindo Eka Persada
    "TOSK",   # Topindo Solusi Komunika
    "TRGU",   # Cerestar Indonesia
    "TRUE",   # Triniti Dinamik
    "TRUK",   # Guna Timur Raya
    "UANG",   # Pakuan
    "UNIQ",   # Ulima Nitra
    "UNTD",   # Terang Dunia Internusa
    "UVCR",   # Trimegah Karya Pratama
    "VAST",   # Vastland Indonesia
    "VERN",   # Verona Indah Pictures
    "VIVA",   # Visi Media Asia
    "VRNA",   # Mizuho Leasing Indonesia
    "WAPO",   # Wahana Pronatural
    "WBSA",   # BSA Logistics Indonesia
    "WGSH",   # Wira Global Solusi
    "WIDI",   # Widiant Jaya Krenindo
    "WINE",   # Hatten Bali
    "WINR",   # Winner Nusantara Jaya
    "WIRG",   # WIR Asia
    "WMPP",   # Widodo Makmur Perkasa
    "WOWS",   # Ginting Jaya Energi
    "XISI",   # Ciptadana Properti Ritel Indonesia
    "ZBRA",   # Dosni Roha Indonesia
    "ACRO",   # Samcro Hyosung Adilestari
    "AEGS",   # Anugerah Spareparts Sejahtera
    "AGAR",   # Asia Sejahtera Mina
    "AKKU",   # Anugerah Kagum Karya Utama
    "ALKA",   # Alakasa Industrindo
    "AMIN",   # Ateliers Mecaniques D'Indonesie
    "APII",   # Arita Prima Indonesia
    "ASH",    # Cilacap Samudera Fishing Industry (was ASHA)
    "ASPR",   # Asia Pramulia
    "ATAP",   # Trimitra Prawara Goldland
    "ATLA",   # Atlantis Subsea Indonesia
    "BABY",   # Multitrend Indo
    "BACH",   # Bach Multi Global
    "BAPR",   # Bhakti Agung Propertindo
    "BATR",   # Benteng Api Technic
    "BAYU",   # Bayu Buana
    "BDKR",   # Berdikari Pondasi Perkasa
    "BIKA",   # Binakarya Jaya Abadi
    "BIMA",   # Primarindo Asia Infrastructure
    "BIPP",   # Bhuwanatala Indah Permai
    "BMBL",   # Lavender Bina Cendikia
    "BNGA",   # Bank CIMB Niaga
    "BOG",    # Apollo Global Interactive (was BOGA)
    "BOLA",   # Bali Bintang Sejahtera
    "BOLT",   # Garuda Metalindo
    "BPFI",   # Woori Finance Indonesia
    "BRAM",   # Indo Kordsa
    "BRNA",   # Berlina
    "BRPT",   # Barito Pacific
    "BTEK",   # Bumi Teknokultura Unggul
    "BULL",   # Buana Lintas Lautan
    "CAMP",   # Campina Ice Cream Industry
    "CARS",   # Bintraco Dharma
    "CBRE",   # Cakra Buana Resources Energi
    "CHIP",   # Pelita Teknologi Global
    "CINT",   # Chitose Internasional
    "CLPI",   # Colorpak Indonesia
    "CMNP",   # Citra Marga Nusaphala Persada
    "CNMA",   # Nusantara Sejahtera Raya
    "CSMI",   # Cipta Selera Murni
    "CTBN",   # Citra Tubindo
    "DART",   # Duta Anggada Realty
    "DADA",   # Diamond Citra Propertindo
    "DADP",   # Damai Sejahtera Abadi
    "DEWI",   # Dewi Shri Farmindo
    "DFAM",   # Dafam Property Indonesia
    "DIGI",   # Arkadia Digital Media
    "DIVA",   # Distribusi Voucher Nusantara
    "DIVI",   # Distribusi Voucher Nusantara
    "DKHH",   # Cipta Sarana Medika
    "DLTA",   # Delta Djakarta
    "DOOH",   # Era Media Sejahtera
    "DPUM",   # Dua Putra Utama Makmur
    "ECII",   # Electronic City Indonesia
    "EKAD",   # Ekadharma International
    "ELTY",   # Bakrieland Development
    "EMDE",   # Megapolitan Developments
    "ENAK",   # Champ Resto Indonesia
    "ERAL",   # Sinar Eka Selaras
    "ERTX",   # Eratex Djaja
    "ESSA",   # ESSA Industries Indonesia
    "FAST",   # Fast Food Indonesia
    "FILM",   # MD Entertainment
    "FITT",   # Hotel Fitra International
    "FORU",   # Fortune Indonesia
    "FPNI",   # Lotte Chemical Titan
    "FUJI",   # Fuji Finance Indonesia
    "FYU",    # Future Energy Global (was FUTR)
    "GGRP",   # Gunung Raja Paksi
    "GDYR",   # Goodyear Indonesia
    "GEMA",   # Gema Grahasarana
    "GEMS",   # Golden Energy Mines
    "GHON",   # Gihon Telekomunikasi Indonesia
    "GLVA",   # Galva Technologies
    "GMFI",   # Garuda Maintenance Facility Aero Asia
    "GMTD",   # Gowa Makassar Tourism Development
    "GOLF",   # Intra Golflink Resorts
    "GOLL",   # Golden Plantation
    "GPRA",   # Perdana Gapuraprima
    "GULA",   # Aman Agrindo
    "GWSA",   # Greenwood Sejahtera
    "HDIT",   # Hensel Davest Indonesia
    "HERO",   # Hero Global Investment
    "HITS",   # Humpuss Intermoda Transportasi
    "HOMI",   # Grand House Mulia
    "HOPE",   # Harapan Duta Pertiwi
    "HRME",   # Menteng Heritage Realty
    "HRUM",   # Harum Energy
    "IBST",   # Inti Bangun Sejahtera
    "IFII",   # Indonesia Fibreboard Industry
    "IFSH",   # Ifishdeco
    "IKAI",   # Intikeramik Alamasri Industri
    "IKPM",   # Ikapharmindo Putramas
    "IMJS",   # Indomobil Multi Jasa
    "IMPC",   # Impack Pratama Industri
    "INAF",   # Indofarma
    "INCI",   # Intanwijaya Internasional
    "INDS",   # Indospring
    "INDX",   # Tanah Laut
    "INRD",   # Royalindo Investa Wijaya (was INRO)
    "INTD",   # Inter Delta
    "INTP",   # Indocement Tunggal Prakarsa
    "IPCC",   # Indonesia Kendaraan Terminal
    "IPCM",   # Jasa Armada Indonesia
    "IPOL",   # Indopoly Swakarsa Industry
    "IRE",    # Itama Ranoraya (was IRRA)
    "ISAT",   # Indosat
    "ITIC",   # Indonesian Tobacco
    "JECC",   # Jembo Cable Company
    "JECX",   # Nitrasanata Dharma
    "JECC",   # Jembo Cable Company
    "JIHD",   # Jakarta International Hotels & Development
    "JSMR",   # Jasa Marga (Persero)
    "KARW",   # Meratus Jasa Prima
    "KBLV",   # First Media
    "KDSI",   # Kedawung Setia Industrial
    "KKES",   # Kusuma Kemindo Sentosa
    "KMDS",   # Kurniamitra Duta Sentosa
    "KOBX",   # Kobexindo Tractors
    "KOCE",   # Kokoh Exa Nusantara
    "KOTA",   # DMS Propertindo
    "KPIG",   # MNC Tourism Indonesia
    "KREN",   # Quantum Clovera Investama
    "LAPI",   # Logisticsplus International
    "LAPD",   # Leyand International
    "LCKM",   # LCK Global Kedaton
    "LFLP",   # Imago Mulia Persada
    "LIV",    # Homeco Victoria Makmur (was LIVE)
    "LRNA",   # Eka Sari Lorena Transport
    "MANG",   # Manggung Polahraya
    "MARI",   # Mahaka Radio Integra
    "MAXI",   # Maxindo Karya Anugerah
    "MBTO",   # Martina Berto
    "MCAS",   # M Cash Integrasi
    "MDIA",   # Intermedia Capital
    "MDRN",   # Modern Internasional
    "MDPL",   # Mega Manunggal Property
    "MENN",   # Menn Teknologi Indonesia
    "MERE",   # Merry Riana Edukasi
    "MFMI",   # Multifiling Mitra Indonesia
    "MIRA",   # Mitra International Resources
    "MITI",   # Mitra Investindo
    "MKTR",   # Menthobi Karyatama Raya
    "MNCN",   # Media Nusantara Citra
    "MOLI",   # Madusari Murni Indah
    "MPMX",   # Mitra Pinasthika Mustika
    "MPPA",   # Matahari Putra Prima
    "MPRO",   # Maha Properti Indonesia
    "MSKY",   # MNC Sky Vision
    "MTDL",   # Metrodata Electronics
    "MTFN",   # Capitalinc Investment
    "MTPS",   # Meta Epsi
    "MTSM",   # Metro Realty
    "MYTX",   # Asia Pacific Investama
    "NASI",   # Wahana Inti Makmur
    "NETV",   # MDTV Media Technologies
    "NICL",   # PAM Mineral
    "NIRO",   # City Retail Developments
    "NPGF",   # Nusa Palapa Gemilang
    "NTBK",   # Nusatama Berkah
    "NZIA",   # Nusantara Almazia
    "OASA",   # Maharaksa Biru Energi
    "OBMD",   # OBM Drilchem
    "OKAS",   # Ancora Indonesia Resources
    "OLIV",   # Oscar Mitra Sukses Sejahtera
    "OPMS",   # Optima Prima Metal Sinergi
    "PADI",   # Minna Padi Investama Sekuritas
    "PAMG",   # Bima Sakti Pertiwi
    "PBSA",   # Paramita Bangun Sarana
    "PDPP",   # Primadaya Plastisindo
    "PEG",    # Panca Global Kapital (was PEGE)
    "PGJO",   # Bahtera Bumi Raya
    "PGLI",   # Pembangunan Graha Lestari Indah
    "PGUN",   # Pradiksi Gunatama
    "PHAP",   # Phapros (was PEHA)
    "PLAN",   # Planet Properindo Jaya
    "PMMP",   # Panca Mitra Multiperdana
    "PNSE",   # Pudjiadi and Sons
    "POLA",   # Pool Advista Finance
    "POLU",   # Golden Flower
    "PPRI",   # Paperocks Indonesia
    "PPRO",   # Pembangunan Perumahan Properti
    "PRIM",   # Royal Prima
    "PSDN",   # Prasidha Aneka Niaga
    "PTDU",   # Djasa Ubersakti
    "PTIS",   # Indo Straits
    "PTMR",   # Master Print
    "PTMP",   # Mitra Pack
    "PTPW",   # Pratama Widya
    "PTSP",   # Pioneerindo Gourmet International
    "PUDP",   # Pudjiadi Prestige
    "PURA",   # Putra Rajawali Kencana
    "PURI",   # Puri Global Sukses
    "RAFA",   # Sari Kreasi Boga
    "RANC",   # Supra Boga Lestari
    "RCC",    # Utama Radar Cahaya
    "RDTX",   # Roda Vivatex
    "RELI",   # Reliance Sekuritas Indonesia
    "RGAS",   # Kian Santang Muliatama
    "RICY",   # Ricky Putra Globalindo
    "RMKO",   # Royaltama Mulia Kontraktorindo
    "ROCK",   # Rockfields Properti Indonesia
    "RONY",   # Aesler Grup Internasional
    "RUNS",   # Global Sukses Solusi
    "SAFE",   # Steady Safe
    "SAME",   # Sarana Meditama Metropolitan
    "SATU",   # Kota Satu Properti
    "SCNP",   # Selaras Citra Nusantara Perkasa
    "SEM",    # Semacom Integrated (was SEMA)
    "SFAN",   # Surya Fajar Capital
    "SGER",   # Sumber Global Energy
    "SICO",   # Sigma Energy Compressindo
    "SINO",   # Singaraja Putra (was SINI)
    "SKRN",   # Superkrane Mitra Utama
    "SLIS",   # Gaya Abadi Sempurna
    "SMIL",   # Sarana Mitra Luas
    "SMKM",   # Sumber Mas Konstruksi
    "SMLE",   # Sinergi Multi Lestarindo
    "SNLK",   # Sunter Lakeside Hotel
    "SOSS",   # Shield On Service
    "SOTS",   # Satria Mega Kencana
    "SOUL",   # Mitra Tirta Buwana
    "SPRE",   # Soraya Berjaya Indonesia
    "SSTM",   # Sunson Textile Manufacturer
    "SUNI",   # Sunindo Pratama
    "SURI",   # Maja Agung Latexindo
    "SWAT",   # Sriwahana Adityakarta
    "TAYS",   # Jaya Swarasa Agung
    "TEBE",   # Dana Brata Luhur
    "TELE",   # Omni Inovasi Indonesia
    "TFAS",   # Telefast Indonesia
    "TGUK",   # Platinum Wahab Nusantara
    "TIRT",   # Tirta Mahakam Resources
    "TNCA",   # Trimuda Nuansa Citra
    "TOOL",   # Rohartindo Nusantara Luas
    "TOPS",   # Totalindo Eka Persada
    "TOTL",   # Total Bangun Persada
    "TOTP",   # Surya Toto Indonesia (was TOTO)
    "TRGU",   # Cerestar Indonesia
    "TRIN",   # Perintis Triniti Properti
    "TRON",   # Teknologi Karya Digital Nusa
    "TRUE",   # Triniti Dinamik
    "TRUK",   # Guna Timur Raya
    "UANG",   # Pakuan
    "UFOE",   # Damai Sejahtera Abadi
    "UNIQ",   # Ulima Nitra
    "UNTD",   # Terang Dunia Internusa
    "URBN",   # Urban Jakarta Propertindo
    "UVCR",   # Trimegah Karya Pratama
    "VAST",   # Vastland Indonesia
    "VENT",   # Venteny Fortuna International
    "VERN",   # Verona Indah Pictures
    "VIVA",   # Visi Media Asia
    "VOKS",   # Voksel Electric
    "VRNA",   # Mizuho Leasing Indonesia
    "WAPO",   # Wahana Pronatural
    "WBSA",   # BSA Logistics Indonesia
    "WGSH",   # Wira Global Solusi
    "WIDI",   # Widiant Jaya Krenindo
    "WINE",   # Hatten Bali
    "WINR",   # Winner Nusantara Jaya
    "WMPP",   # Widodo Makmur Perkasa
    "WOWS",   # Ginting Jaya Energi
    "WSKT",   # Waskita Karya (Persero)
    "XISI",   # Ciptadana Properti Ritel Indonesia
    "YELO",   # Yelooo Integra Datanet
    "ZINC",   # Kapuas Prima Coal
    "ZONE",   # Mega Perintis
]

# ── Sector Index ──────────────────────────────────────────────────────────
IDX_SECTORS: dict[str, list[str]] = {
    "finance_banking": FINANCE_BANKING,
    "finance_insurance": FINANCE_INSURANCE,
    "mining_coal": MINING_COAL,
    "consumer_food": CONSUMER_FOOD,
    "consumer_tobacco": CONSUMER_TOBACCO,
    "consumer_household": CONSUMER_HOUSEHOLD,
    "infrastructure": INFRASTRUCTURE,
    "energy": ENERGY,
    "property": PROPERTY,
    "agriculture": AGRICULTURE,
    "basic_materials": BASIC_MATERIALS,
    "industrial": INDUSTRIAL,
    "trade_services": TRADE_SERVICES,
    "technology": TECHNOLOGY,
    "healthcare": HEALTHCARE,
    "transportation": TRANSPORTATION,
    "hotels_tourism": HOTELS_TOURISM,
    "investment": INVESTMENT,
    "miscellaneous": MISCELLANEOUS,
}

# ── Flat list of all stocks ───────────────────────────────────────────────
# Deduplicated tickers from all sectors above.
# This is the canonical list used for bulk screening.
IDX_ALL_STOCKS: list[str] = sorted(
    {
        ticker
        for sector_stocks in IDX_SECTORS.values()
        for ticker in sector_stocks
    }
)

# ── Public helpers ─────────────────────────────────────────────────────────


def get_all_idx_stocks() -> list[str]:
    """Return the complete list of all IDX stock tickers (sorted & deduplicated)."""
    return list(IDX_ALL_STOCKS)


def get_idx_stocks_by_sector(sector: str) -> list[str]:
    """Return stock tickers for a given sector.

    Parameters
    ----------
    sector :
        One of the keys in IDX_SECTORS (e.g. ``"finance_banking"``,
        ``"mining_coal"``, ``"property"``, etc.).

    Returns
    -------
    list[str]
        Stock tickers in that sector, or empty list if unknown sector.

    Example
    -------
    >>> get_idx_stocks_by_sector("consumer_food")
    ["ADES", "AISA", "ALTO", ...]
    """
    return list(IDX_SECTORS.get(sector, []))


def get_sector_names() -> list[str]:
    """Return all available sector names."""
    return sorted(IDX_SECTORS.keys())


def get_sectors() -> dict[str, list[str]]:
    """Return the complete sector dictionary."""
    return {k: list(v) for k, v in IDX_SECTORS.items()}
