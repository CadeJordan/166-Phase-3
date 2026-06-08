# CS166 Phase 3

## How to Run

**Terminal 1** — SSH tunnel (keep open):

```bash
ssh -L 5432:localhost:25967 cjord019@cs166.cs.ucr.edu
```

**Terminal 2** — on the server, start Postgres if needed:

```bash
cs166_db_start
```

Then set up the database (run once, in order). The schema creates the tables,
`index.sql` adds the performance indexes, and `testData.sql` loads sample rows:

```bash
cs166_psql cjord019_phase3_DB < cs166_phase2_schema.sql
cs166_psql cjord019_phase3_DB < index.sql
cs166_psql cjord019_phase3_DB < testData.sql
```

> Running `index.sql` is required — the app's queries rely on these indexes for
> performance. The `CREATE INDEX IF NOT EXISTS` statements are safe to re-run.

**Terminal 3** — Flask on your laptop (project root):

```bash
pip install flask psycopg2-binary
flask --app routes.app run --debug
```

Open http://127.0.0.1:5000

Database settings are in `config.py` (defaults: `cjord019_phase3_DB`, port `5432` through the tunnel). Override with env vars if needed:

```powershell
$env:DB_NAME="cjord019_phase3_DB"
$env:DB_PORT="5432"
$env:DB_USER="cjord019"
```

On startup you should see `Connecting to database... Done` from `EmbeddedSQL` (uses psycopg2).
## Demo logins

Go to `/login` and pick one of these from the dropdown:
Password is not verified.

## Pages

**Public**
- `/` - list of auctions
- `/search` - search by item name
- `/auction/<id>` - auction details + place bid form
- `/login`, `/register`

**Buyer**
- `/bids` - bids you placed
- `/wins` - auctions you won
- `/account` - edit profile
- `/payment/<id>` - payment page
- `/orders/<id>` - shipment info

**Seller**
- `/sell` - seller hub
- `/sell/listings` - your items
- `/sell/create` - list a new item
- `/sell/edit/<item_id>` - edit listing
- `/sell/auction/<id>/manage` - end auction, see bids

**Admin**
- `/admin` - dashboard
- `/admin/users` - change user roles
- `/admin/auctions` - view all auctions
- `/admin/items` - manage items
- `/admin/payments` - view payments
- `/admin/shipments` - update shipment status

## Important notes

- Flask connects to PostgreSQL on startup via `data/queries.py` → `EmbeddedSQL` (psycopg2).
- Keep the SSH tunnel open while the app is running.
- Make sure `index.sql` has been run on the server (see Terminal 2 setup above).
- Reload sample data on the server if tables are empty: `cs166_psql cjord019_phase3_DB < testData.sql`
