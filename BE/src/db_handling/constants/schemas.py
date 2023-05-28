PATIENT_SCHEMA = '''
id INTEGER PRIMARY KEY,
forename TEXT NOT NULL,
lastname TEXT NOT NULL,
gender TEXT,
original_id TEXT UNIQUE
'''
JOURNAL_ENTRY_SCHEMA = '''
id INTEGER PRIMARY KEY,
text_entry TEXT,
date_written DATETIME,
consultation_id TEXT,
original_entry_id TEXT UNIQUE,
patient_id INTEGER,
FOREIGN KEY (patient_id) REFERENCES patients(id)
'''
SUMMARY_SCHEMA = '''
id INTEGER PRIMARY KEY,
text_entry TEXT,
timestamp_written DATETIME,
patient_id INTEGER,
FOREIGN KEY (patient_id) REFERENCES patients(id)
'''
MOTIVATION_SCORES_SCHEMA = '''
id INTEGER PRIMARY KEY,
date_noted DATETIME,
patient_id INTEGER,
overall_motivation INTEGER,
perceived_importance INTEGER,
chance_of_succ INTEGER,
perceived_control INTEGER,
meaningfulness INTEGER,
journal_entry_id INTEGER,
FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id),
FOREIGN KEY (patient_id) REFERENCES patients(id)
'''
VALENCE_SCHEMA = '''
id INTEGER PRIMARY KEY,
patient_id INTEGER,
topic TEXT,
sentiment REAL,
date_noted DATETIME,
journal_entry_id INTEGER,
FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id),
FOREIGN KEY (patient_id) REFERENCES patients(id)
'''