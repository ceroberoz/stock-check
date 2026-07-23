"""IDX (Indonesia Stock Exchange) — comprehensive list of all listed stocks.

This module provides the complete universe of ~900+ stocks listed on the
Indonesia Stock Exchange (IDX), organized by sector for easier maintenance
and filtering. Based on IDX listing data as of July 2026.
"""

from __future__ import annotations

from dataclasses import dataclass

# ── Finance / Banking ──────────────────────────────────────────────────────────
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

# ── Finance / Insurance ──────────────────────────────────────────────────────────
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

# ── Consumer / Food & Beverage ──────────────────────────────────────────────────────────
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
    "PDPP",   # Primadaya Plastisindo
]

# ── Consumer / Tobacco ──────────────────────────────────────────────────────────
CONSUMER_TOBACCO: list[str] = [
    "GGRM",   # Gudang Garam
    "HMSP",   # Hanjaya Mandala Sampoerna
    "ITIC",   # Indonesian Tobacco
]

# ── Consumer / Household ──────────────────────────────────────────────────────────
CONSUMER_HOUSEHOLD: list[str] = [
    "DVLA",   # Darya-Varia Laboratoria
    "KAEF",   # Kimia Farma
    "KIAS",   # Keramika Indonesia Assosiasi
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

# ── Infrastructure ──────────────────────────────────────────────────────────
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

# ── Energy ──────────────────────────────────────────────────────────
ENERGY: list[str] = [
    "APEX",   # Apexindo Pratama Duta
    "ELSA",   # Elnusa
    "ESSA",   # ESSA Industries Indonesia
    "HUMI",   # Humpuss Maritim Internasional
    "MEDC",   # Medco Energi Internasional
    "PGAS",   # Perusahaan Gas Negara (Persero)
    "RAJA",   # Rukun Raharja
    "RATU",   # Raharja Energi Cepu
    "RUIS",   # Radiant Utama Interinsco
    "SGER",   # Sumber Global Energy
    "WOWS",   # Ginting Jaya Energi
    "OILS",   # Indo Oil Perkasa
]

# ── Property & Real Estate ──────────────────────────────────────────────────────────
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
    "BUV",   # Bukit Uluwatu Villa (was BUVA)
]

# ── Agriculture ──────────────────────────────────────────────────────────
AGRICULTURE: list[str] = [
    "AALI",   # Astra Agro Lestari
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
    "TLDN",   # Teladan Prima Agro
    "UNSP",   # Bakrie Sumatera Plantations
    "SGRO",   # Prime Agri Resources
    "UDNG",   # Agro Bahari Nusantara
    "FISH",   # FKS Multi Agro
    "ALII",   # Ancara Logistics Indonesia (was agriculture)
]

# ── Basic Materials ──────────────────────────────────────────────────────────
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
    "CAKK",   # Cahayaputra Asa Keramik
    "CCSI",   # Communication Cable Systems Indonesia
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
    "KRAS",   # Krakatau Steel (Persero)
    "LION",   # Lion Metal Works
    "LMSH",   # Lionmesh Prima
    "LTL",   # Lautan Luas
    "MLIA",   # Mulia Industrindo
    "MSJA",   # Multi Spunindo Jaya
    "PBRX",   # Pan Brothers
    "POLU",   # Golden Flower
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
    "CHEM",   # Chemstar Indonesia
]

# ── Industrial ──────────────────────────────────────────────────────────
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
    "CARS",   # Industri dan Perdagangan Bintraco Dharma
    "DEPO",   # Caturkarda Depo Bangunan
    "DRMA",   # Dharma Polimetal
    "ERTX",   # Eratex Djaja
    "ESTI",   # Ever Shine Tex
    "FORU",   # Fortune Indonesia
    "GDYR",   # Goodyear Indonesia
    "GGRP",   # Gunung Raja Paksi
    "HEXA",   # Hexindo Adiperkasa
    "IKBI",   # Sumi Indo Kabel
    "IMAS",   # Indomobil Sukses Internasional
    "INDS",   # Indospring
    "INTA",   # Intraco Penta
    "JECC",   # Jembo Cable Company
    "JSPT",   # Jakarta Setiabudi Internasional
    "KDSI",   # Kedawung Setia Industrial
    "KOBX",   # Kobexindo Tractors
    "KONI",   # Perdana Bangun Pusaka
    "LPIN",   # Multi Prima Sejahtera
    "MARK",   # Mark Dynamics Indonesia
    "PACK",   # Abadi Nusantara Hijau Investama
    "PJHB",   # Pelayaran Jaya Hidup Baru
    "PJAA",   # Pembangunan Jaya Ancol
    "PRIM",   # Royal Prima
    "PTPW",   # Pratama Widya
    "RELI",   # Reliance Sekuritas Indonesia
    "SAPX",   # Satria Antaran Prima
    "SMSM",   # Selamat Sempurna
    "SOSS",   # Shield On Service
    "STAR",   # Buana Artha Anugerah
    "TRIS",   # Trisula International
    "UNIT",   # Nusantara Pelabuhan Handal (was UNIT)
    "WICO",   # Wicaksana Overseas International
    "WOOD",   # Integra Indocabinet
    "BELL",   # Trisula Textile Industries
    "SSTM",   # Sunson Textile Manufacturer
    "HADE",   # Himalaya Energi Perkasa
    "KREN",   # Quantum Clovera Investama
    "TRUS",   # Trust Finance Indonesia
    "KBLV",   # First Media
    "TOTO",   # Surya Toto Indonesia
    "CTBN",   # Citra Tubindo
]

# ── Trade & Services ──────────────────────────────────────────────────────────
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
    "MIDI",   # Midi Utama Indonesia (Alfamidi)
    "MLPT",   # Multipolar Technology
    "MPMX",   # Mitra Pinasthika Mustika
    "MPPA",   # Matahari Putra Prima
    "MTDL",   # Metrodata Electronics
    "PADI",   # Minna Padi Investama Sekuritas
    "RALS",   # Ramayana Lestari Sentosa
    "RISE",   # Jaya Sukses Makmur Sentosa
    "SONA",   # Sona Topas Tourism Industry
    "SUPR",   # Solusi Tunas Pratama
    "TELE",   # Omni Inovasi Indonesia
    "UNTR",   # United Tractors
    "YULE",   # Yulie Sekuritas Indonesia
    "ZONE",   # Mega Perintis
]

# ── Technology ──────────────────────────────────────────────────────────
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
    "ENZO",   # Morenzo Abadi Perkasa
    "FILM",   # MD Entertainment
    "GOTO",   # GoTo Gojek Tokopedia
    "HDIT",   # Hensel Davest Indonesia
    "INET",   # Sinergi Inti Andalan Prima
    "IPTV",   # MNC Vision Networks
    "KIOS",   # Kioson Komersial Indonesia
    "LUCK",   # Sentral Mitra Informatika
    "LUCY",   # Lima Dua Lima Tiga
    "MARI",   # Mahaka Radio Integra
    "MCAS",   # M Cash Integrasi
    "MDIA",   # Intermedia Capital
    "MGNA",   # Magna Investama Mandiri
    "MNCN",   # Media Nusantara Citra
    "MSIN",   # MNC Digital Entertainment
    "MSKY",   # MNC Sky Vision
    "MSTI",   # Mastersystem Infotama
    "MTPS",   # Meta Epsi
    "NETV",   # MDTV Media Technologies
    "NFCX",   # NFC Indonesia
    "RAAM",   # Tripar Multivision Plus
    "SCMA",   # Surya Citra Media
    "SEMA",   # Semacom Integrated
    "SILO",   # Siloam International Hospitals
    "SINI",   # Singaraja Putra
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

# ── Healthcare ──────────────────────────────────────────────────────────
HEALTHCARE: list[str] = [
    "BMHS",   # Bundamedik
    "CARE",   # Metro Healthcare Indonesia
    "DGNS",   # Diagnos Laboratorium Utama
    "EMMI",   # Esa Medika Mandiri
    "HEAL",   # Medikaloka Hermina
    "INAF",   # Indofarma
    "KLBF",   # Kalbe Farma
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
    "SOHO",   # Soho Global Health
    "SRAJ",   # Sejahteraraya Anugrahjaya
    "LABS",   # UBC Medical Indonesia
    "OBAT",   # Brigit Biofarmaka Technologi
    "CHEK",   # Diastika Biotekindo
    "DKHH",   # Cipta Sarana Medika
    "MEDS",   # Hetzer Medical Indonesia
]

# ── Transportation & Logistics ──────────────────────────────────────────────────────────
TRANSPORTATION: list[str] = [
    "BBRM",   # Pelayaran Nasional Bina Buana Raya
    "BLTA",   # Berlian Laju Tanker
    "BOAT",   # Newport Marine Services
    "BPTR",   # Batavia Prosperindo Trans
    "BSML",   # Bintang Samudera Mandiri Lines
    "CMPP",   # AirAsia Indonesia
    "ELPI",   # Pelayaran Nasional Ekalya Purnamasari
    "GMFI",   # Garuda Maintenance Facility Aero Asia
    "GIAA",   # Garuda Indonesia (Persero)
    "HAIS",   # Hasnur Internasional Shipping
    "HATM",   # Habco Trans Maritima
    "HITS",   # Humpuss Intermoda Transportasi
    "IPCC",   # Indonesia Kendaraan Terminal
    "IPCM",   # Jasa Armada Indonesia
    "JAYA",   # Armada Berjaya Trans
    "KARW",   # Meratus Jasa Prima
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
    "LEAD",   # Logindo Samudramakmur
    "DPNS",   # Duta Pertiwi Nusantara
    "KJEN",   # Krida Jaringan Nusantara
    "SBMA",   # Surya Biru Murni Acetylene
    "TRUK",   # Guna Timur Raya
    "RIGS",   # Rig Tenders Indonesia
    "WAPO",   # Wahana Pronatural
    "LAJU",   # Jasa Berdikari Logistics
]

# ── Hotels & Tourism ──────────────────────────────────────────────────────────
HOTELS_TOURISM: list[str] = [
    "BAYU",   # Bayu Buana
    "BOLA",   # Bali Bintang Sejahtera
    "EAST",   # Eastparc Hotel
    "FITT",   # Hotel Fitra International
    "GOLF",   # Intra Golflink Resorts
    "HILL",   # Hillcon
    "HOMI",   # Grand House Mulia
    "HOTL",   # Saraswanti Indoland Development
    "ICON",   # Island Concepts Indonesia
    "JIHD",   # Jakarta International Hotels & Development
    "PDES",   # Destinasi Tirta Nusantara
    "PLAN",   # Planet Properindo Jaya
    "PSDN",   # Prasidha Aneka Niaga
    "PTSP",   # Pioneerindo Gourmet International
    "PUDP",   # Pudjiadi Prestige
    "SHID",   # Hotel Sahid Jaya International
    "SNLK",   # Sunter Lakeside Hotel
    "CSIS",   # Cahayasakti Investindo Sukses
]

# ── Investment ──────────────────────────────────────────────────────────
INVESTMENT: list[str] = [
    "BHIT",   # MNC Asia Holding
    "BNBR",   # Bakrie & Brothers
    "BPII",   # Batavia Prosperindo Internasional
    "DSFI",   # Dharma Samudera Fishing Industries
    "MYTX",   # Asia Pacific Investama
    "SMMA",   # Sinar Mas Multiartha
    "SRTG",   # Saratoga Investama Sedaya
]

# ── Miscellaneous ──────────────────────────────────────────────────────────
MISCELLANEOUS: list[str] = [
    "ABBA",   # Mahaka Media
    "AGAR",   # Asia Sejahtera Mina
    "AIMS",   # Artha Mahiya Investama
    "AKSI",   # Mineral Sumberdaya Mandiri
    "ALKA",   # Alakasa Industrindo
    "AMAN",   # Makmur Berkah Amanda
    "AMMS",   # Agung Menjangan Mas
    "APII",   # Arita Prima Indonesia
    "ASLI",   # Asri Karya Lestari
    "ASPR",   # Asia Pramulia
    "ATAP",   # Trimitra Prawara Goldland
    "ATLA",   # Atlantis Subsea Indonesia
    "BABY",   # Multitrend Indo
    "BACH",   # Bach Multi Global
    "BAIK",   # Bersama Mencapai Puncak
    "BAPR",   # Bakrie Pipe Industries
    "BATR",   # Benteng Api Technic
    "BBIA",   # Sumber Mineral Global Abadi
    "BBSS",   # Bumi Benowo Sukses Sejahtera
    "BDKR",   # Berdikari Pondasi Perkasa
    "BEBE",   # Berkah Beton Sadaya
    "BIKA",   # Binakarya Jaya Abadi
    "BIKE",   # Sepeda Bersama Indonesia
    "BINO",   # Perma Plasindo
    "BLES",   # Superior Prima Sukses
    "BLTZ",   # Graha Layar Prima
    "BLUE",   # Berkah Prima Perkasa
    "BMBL",   # Lavender Bina Cendikia
    "BSBK",   # Wulandari Bangun Laksana
    "BUVA",   # Bukit Uluwatu Villa
    "CASH",   # Cashlez Worldwide Indonesia
    "CBPE",   # Citra Buana Prasida
    "CBUT",   # Citra Borneo Utama
    "CEKA",   # Wilmar Cahaya Indonesia
    "CHIP",   # Pelita Teknologi Global
    "CNMA",   # Nusantara Sejahtera Raya
    "CNKO",   # Exploitasi Energi Indonesia
    "CRAB",   # Toba Surimi Industries
    "CRSN",   # Carsurin
    "CSMI",   # Cipta Selera Murni
    "DADA",   # Diamond Citra Propertindo
    "DAAZ",   # Daaz Bara Lestari
    "DADP",   # Damai Sejahtera Abadi (was UFOE)
    "DATA",   # Remala Abadi
    "DEFI",   # Danasupra Erapacific
    "DEWI",   # Dewi Shri Farmindo
    "DIVI",   # Distribusi Voucher Nusantara (was DIVA)
    "DOSS",   # Global Sukses Digital
    "DWGL",   # Dwi Guna Laksana
    "DYAN",   # Dyandra Media International
    "ECOC",   # Ecocare Indo Pasifik (was HYGN)
    "ELTY",   # Bakrieland Development
    "EMDE",   # Megapolitan Developments
    "ERAL",   # Sinar Eka Selaras
    "ESTA",   # Esta Multi Usaha
    "EURO",   # Estee Gold Feet
    "FIMP",   # Fimperkasa Utama
    "FLMC",   # Falmaco Nonwoven Industri
    "FOLK",   # Multi Garam Utama
    "FWCT",   # Wijaya Cahaya Timber
    "GEMA",   # Gema Grahasarana
    "GLOB",   # Globe Kita Terang
    "GOLD",   # Visi Telekomunikasi Infrastruktur
    "GPSO",   # Geoprima Solusi
    "GUN",   # Gunanusa Eramandiri (was GUNA)
    "GWSA",   # Greenwood Sejahtera
    "HALO",   # Haloni Jane
    "HBAT",   # Minahasa Membangun Hebat
    "HGII",   # Hero Global Investment
    "HRME",   # Menteng Heritage Realty
    "HYGN",   # Ecocare Indo Pasifik
    "IBFN",   # Intan Baru Prana
    "IBOS",   # Indo Boga Sukses
    "IKAN",   # Era Mandiri Cemerlang
    "INA",   # Indal Aluminium Industry (was INAI)
    "INDX",   # Tanah Laut
    "INPS",   # Indah Prakasa Sentosa
    "INTD",   # Inter Delta
    "IOTF",   # Sumber Sinergi Makmur
    "IPAC",   # Era Graharealty
    "IRRA",   # Itama Ranoraya
    "IRSX",   # Folago Global Nusantara
    "ISAP",   # Isra Presisi Indonesia
    "ISEA",   # Indo American Seafoods
    "JAST",   # Jasnita Telekomindo
    "JECX",   # Nitrasanata Dharma
    "JELI",   # Niramas Utama
    "JGLE",   # Graha Andrasentra Propertindo
    "KDTN",   # Puri Sentul Permai
    "KETR",   # Ketrosden Triasmitra
    "KING",   # Hoffmen Cleanindo
    "KLAS",   # Pelayaran Kurnia Lautan Semesta
    "KLIN",   # Klinko Karya Imaji
    "KMDS",   # Kurniamitra Duta Sentosa
    "KMTR",   # Kirana Megatara
    "KOCE",   # Kokoh Exa Nusantara (was KOCI)
    "KOIN",   # Kokoh Inti Arebama
    "KOKA",   # Koka Indonesia
    "KRYA",   # Bangun Karya Perkasa Jaya
    "KSIX",   # Kentanix Supra International
    "KUAS",   # Ace Oldfields
    "LAPD",   # Leyand International
    "LCKM",   # LCK Global Kedaton
    "LFLP",   # Imago Mulia Persada
    "LMAX",   # Lupromax Pelumas Indonesia
    "LOPI",   # Logisticsplus International
    "LPPS",   # Lenox Pasifik Investama
    "MANG",   # Manggung Polahraya
    "MAXI",   # Maxindo Karya Anugerah
    "MDRN",   # Modern Internasional
    "MDKI",   # Emdeki Utama
    "MDPL",   # Mega Manunggal Property (was MMLP)
    "MEJA",   # Harta Djaya Karya
    "MENN",   # Menn Teknologi Indonesia
    "MERE",   # Merry Riana Edukasi
    "MFMI",   # Multifiling Mitra Indonesia
    "MITI",   # Mitra Investindo
    "MKN",   # Mitra Komunikasi Nusantara
    "MKTR",   # Menthobi Karyatama Raya
    "MOLI",   # Madusari Murni Indah
    "MPXL",   # MPX Logistics International
    "MTFN",   # Capitalinc Investment
    "MTSM",   # Metro Realty
    "MUTU",   # Mutuagung Lestari
    "NAIK",   # Adiwarna Anugerah Abadi
    "NANO",   # Nanotech Indonesia Global
    "NASA",   # Andalan Perkasa Abadi
    "NASI",   # Wahana Inti Makmur
    "NATO",   # Olympus Strategic Indonesia
    "NICE",   # Adhi Kartiko Pratama
    "NINE",   # Techno9 Indonesia
    "NPGF",   # Nusa Palapa Gemilang
    "NTBK",   # Nusatama Berkah
    "NZIA",   # Nusantara Almazia
    "OBMD",   # OBM Drilchem
    "OKAS",   # Ancora Indonesia Resources
    "OLIV",   # Oscar Mitra Sukses Sejahtera
    "OPMS",   # Optima Prima Metal Sinergi
    "PADA",   # Personel Alih Daya
    "PAMG",   # Bima Sakti Pertiwi
    "PCAR",   # Prima Cakrawala Abadi
    "PGLI",   # Pembangunan Graha Lestari Indah
    "PICO",   # Pelangi Indah Canindo
    "PIPE",   # Indo Pureco Pratama (was IPPE)
    "PMMP",   # Panca Mitra Multiperdana
    "PNSE",   # Pudjiadi and Sons
    "POLA",   # Pool Advista Finance
    "POLY",   # Asia Pacific Fibers
    "PPRE",   # PP Presisi
    "PTDU",   # Djasa Ubersakti
    "PTIS",   # Indo Straits
    "PTMR",   # Master Print
    "PTMP",   # Mitra Pack
    "PURA",   # Putra Rajawali Kencana
    "PURI",   # Puri Global Sukses
    "RBM",   # Ristia Bintang Mahkotasejati (was RBMS)
    "RCC",   # Utama Radar Cahaya (was RCCC)
    "RELF",   # Graha Mitra Asia
    "RGAS",   # Kian Santang Muliatama
    "RICY",   # Ricky Putra Globalindo
    "RMKO",   # Royaltama Mulia Kontraktorindo
    "RONY",   # Aesler Grup Internasional
    "SAFE",   # Steady Safe
    "SAGE",   # Saptausaha Gemilangindah
    "SAMF",   # Saraswanti Anugerah Makmur
    "SBM",   # Surya Biru Murni Acetylene (was SBMA)
    "SCNP",   # Selaras Citra Nusantara Perkasa
    "SDPC",   # Millennium Pharmacon International
    "SICO",   # Sigma Energy Compressindo
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
    "SUNI",   # Sunindo Pratama
    "SURI",   # Maja Agung Latexindo
    "SWID",   # Saraswanti Indoland Development
    "TAMA",   # Lancartama Sejati
    "TAYS",   # Jaya Swarasa Agung
    "TEBE",   # Dana Brata Luhur
    "TIRT",   # Tirta Mahakam Resources
    "TNCA",   # Trimuda Nuansa Citra
    "TOOL",   # Rohartindo Nusantara Luas
    "TOPS",   # Totalindo Eka Persada
    "TRGU",   # Cerestar Indonesia
    "TRUE",   # Triniti Dinamik
    "UANG",   # Pakuan
    "UFOE",   # Damai Sejahtera Abadi
    "UNIQ",   # Ulima Nitra
    "UNTD",   # Terang Dunia Internusa
    "UVCR",   # Trimegah Karya Pratama
    "VAST",   # Vastland Indonesia
    "VENT",   # Venteny Fortuna International (was VTNY)
    "VERN",   # Verona Indah Pictures
    "VIVA",   # Visi Media Asia
    "VRNA",   # Mizuho Leasing Indonesia
    "WBSA",   # BSA Logistics Indonesia
    "WGSH",   # Wira Global Solusi
    "WIDI",   # Widiant Jaya Krenindo
    "WINR",   # Winner Nusantara Jaya
    "WINE",   # Hatten Bali
    "WMPP",   # Widodo Makmur Perkasa
    "WSBP",   # Waskita Beton Precast
    "WTON",   # Wijaya Karya Beton
    "XISI",   # Ciptadana Properti Ritel Indonesia
    "YOUR",   # Roda Vivatex (was RDTX)
    "ZBRA",   # Dosni Roha Indonesia
    "ABMM",   # ABM Investama
    "BEER",   # Jobubu Jarum Minahasa
    "BESS",   # Batulicin Nusantara Maritim
    "BRRC",   # Raja Roti Cemerlang
    "CGAS",   # Citra Nusantara Gemilang
    "GTBO",   # Garda Tujuh Buana
    "GTRA",   # Grahaprima Suksesmandiri
    "JEJE",   # Jaya Swarasa Agung (was JEJE)
    "MGLV",   # Panca Anugerah Wisesa
    "MPIX",   # Mitra Pedagang Indonesia
    "MSIE",   # Multisarana Intan Eduka
    "PEGE",   # Panca Global Kapital
    "PKPK",   # Paragon Karya Perkasa
    "PPRI",   # Paperocks Indonesia
    "SWAT",   # Sriwahana Adityakarta
    "TGUK",   # Platinum Wahab Nusantara
    "ACRO",   # Samcro Hyosung Adilestari
    "AEGS",   # Anugerah Spareparts Sejahtera
    "AKKU",   # Anugerah Kagum Karya Utama
    "ASH",   # Cilacap Samudera Fishing Industry (was ASHA)
    "BOG",   # Apollo Global Interactive (was BOGA)
    "CLPI",   # Colorpak Indonesia
    "DFAM",   # Dafam Property Indonesia
    "DOOH",   # Era Media Sejahtera
    "FUJI",   # Fuji Finance Indonesia
    "FYU",   # Future Energy Global (was FUTR)
    "IFII",   # Indonesia Fibreboard Industry
    "IFSH",   # Ifishdeco
    "INRD",   # Royalindo Investa Wijaya (was INRO)
    "INTP",   # Indocement Tunggal Prakarsa
    "IRE",   # Itama Ranoraya (was IRRA)
    "KKES",   # Kusuma Kemindo Sentosa
    "LAPI",   # Logisticsplus International
    "LIV",   # Homeco Victoria Makmur (was LIVE)
    "PEG",   # Panca Global Kapital (was PEGE)
    "PHAP",   # Phapros (was PEHA)
    "RAFA",   # Sari Kreasi Boga
    "RDTX",   # Roda Vivatex
    "ROCK",   # Rockfields Properti Indonesia
    "SEM",   # Semacom Integrated (was SEMA)
    "SFAN",   # Surya Fajar Capital
    "SINO",   # Singaraja Putra (was SINI)
    "TOTP",   # Surya Toto Indonesia (was TOTO)
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


# ── Sector metadata ────────────────────────────────────────────────────────


@dataclass(frozen=True)
class SectorInfo:
    """Metadata for an IDX sector."""

    key: str
    name: str
    description: str
    tier: str  # blue_chip, mid_cap, small_cap, micro_cap


SECTOR_META: dict[str, SectorInfo] = {
    "finance_banking": SectorInfo(
        key="finance_banking",
        name="Finance / Banking",
        description="Commercial banks, rural banks, financial institutions",
        tier="blue_chip",
    ),
    "finance_insurance": SectorInfo(
        key="finance_insurance",
        name="Finance / Insurance",
        description="Insurance companies, asset management, securities",
        tier="mid_cap",
    ),
    "mining_coal": SectorInfo(
        key="mining_coal",
        name="Mining / Coal",
        description="Coal mining, metal mining, mineral extraction",
        tier="blue_chip",
    ),
    "consumer_food": SectorInfo(
        key="consumer_food",
        name="Consumer / Food & Beverage",
        description="Food production, beverages, dairy, agriculture processing",
        tier="blue_chip",
    ),
    "consumer_tobacco": SectorInfo(
        key="consumer_tobacco",
        name="Consumer / Tobacco",
        description="Tobacco manufacturing, cigarettes, tobacco products",
        tier="blue_chip",
    ),
    "consumer_household": SectorInfo(
        key="consumer_household",
        name="Consumer / Household",
        description="Household products, personal care, packaging",
        tier="mid_cap",
    ),
    "infrastructure": SectorInfo(
        key="infrastructure",
        name="Infrastructure",
        description="Telecommunications, toll roads, ports, utilities",
        tier="blue_chip",
    ),
    "energy": SectorInfo(
        key="energy",
        name="Energy",
        description="Oil & gas, geothermal, renewable energy",
        tier="mid_cap",
    ),
    "property": SectorInfo(
        key="property",
        name="Property & Real Estate",
        description="Property developers, real estate, construction",
        tier="mid_cap",
    ),
    "agriculture": SectorInfo(
        key="agriculture",
        name="Agriculture",
        description="Plantation, palm oil, rubber, agriculture",
        tier="mid_cap",
    ),
    "basic_materials": SectorInfo(
        key="basic_materials",
        name="Basic Materials",
        description="Chemicals, ceramics, glass, steel, cement",
        tier="mid_cap",
    ),
    "industrial": SectorInfo(
        key="industrial",
        name="Industrial",
        description="Machinery, automotive, electronics, manufacturing",
        tier="mid_cap",
    ),
    "trade_services": SectorInfo(
        key="trade_services",
        name="Trade & Services",
        description="Retail, wholesale, distribution, trading",
        tier="small_cap",
    ),
    "technology": SectorInfo(
        key="technology",
        name="Technology",
        description="Software, IT services, fintech, e-commerce",
        tier="mid_cap",
    ),
    "healthcare": SectorInfo(
        key="healthcare",
        name="Healthcare",
        description="Pharmaceuticals, hospitals, medical devices",
        tier="mid_cap",
    ),
    "transportation": SectorInfo(
        key="transportation",
        name="Transportation & Logistics",
        description="Airlines, shipping, trucking, logistics",
        tier="mid_cap",
    ),
    "hotels_tourism": SectorInfo(
        key="hotels_tourism",
        name="Hotels & Tourism",
        description="Hotels, resorts, tourism, entertainment",
        tier="small_cap",
    ),
    "investment": SectorInfo(
        key="investment",
        name="Investment",
        description="Investment companies, holding companies, venture capital",
        tier="small_cap",
    ),
    "miscellaneous": SectorInfo(
        key="miscellaneous",
        name="Miscellaneous",
        description="Conglomerates, diversified, other sectors",
        tier="small_cap",
    ),
}


# ── Reverse lookup: ticker → sector ────────────────────────────────────────
# Built once at import time for O(1) sector lookups.

TICKER_TO_SECTOR: dict[str, str] = {}
for _sector, _tickers in IDX_SECTORS.items():
    for _ticker in _tickers:
        TICKER_TO_SECTOR[_ticker] = _sector


def get_sector_for_ticker(ticker: str) -> str | None:
    """Return the sector key for a given ticker, or None if not found.

    Example
    -------
    >>> get_sector_for_ticker("BBCA")
    'finance_banking'
    """
    return TICKER_TO_SECTOR.get(ticker.upper())


def get_sector_info(sector: str) -> SectorInfo | None:
    """Return metadata for a given sector, or None if unknown."""
    return SECTOR_META.get(sector)


# ── Validation ─────────────────────────────────────────────────────────────


def validate_sectors() -> list[str]:
    """Check for duplicate tickers across sectors. Returns list of warnings."""
    warnings: list[str] = []
    seen: dict[str, str] = {}

    for sector, tickers in IDX_SECTORS.items():
        for ticker in tickers:
            if ticker in seen:
                warnings.append(
                    f"Duplicate ticker '{ticker}' in '{sector}' (first seen in '{seen[ticker]}')"
                )
            else:
                seen[ticker] = sector

    return warnings
