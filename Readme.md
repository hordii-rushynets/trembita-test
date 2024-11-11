# Trembita Setup

## Getting Started

### Step 1: Clone the Repository

Clone this repository to your local machine: 

```bash
git clone https://github.com/yourusername/yourrepository.git
cd trembita-test
```

### Step 2: Start project

```bash
docker-compose build
docker-compose up
```

### Step 3: Check time of executon.

1. Open trembita.log file.
2. Find in file: Task started at/Task ended at/Total execution time

### Step 4: Read Data from Database

1. Connect to db.
```bash
docker-compose exec db bash -c "psql -h localhost -Utrembita"
```

2. Copy content from create_view.sql file.
3. Paste the contents into the db terminal.
4. Read data from the field of view.
```bash
SELECT * FROM tsnap_full_view;
SELECT * FROM tsnap_full_view WHERE asc_org_idf = 'SN12000007';
```