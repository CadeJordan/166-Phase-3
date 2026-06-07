# CS166 Phase 3

## How to Run

From the project root (this folder):

```bash
pip install flask
flask --app routes.app run --debug
```

Then open http://127.0.0.1:5000 in your browser.

If `pip` doesn't work, try `python -m pip install flask` instead.

## Demo logins

Go to `/login` and pick one of these from the dropdown:

| Username | Role |
|----------|------|
| buyer1 | Buyer |
| buyer2 | Buyer |
| seller1 | Seller |
| seller2 | Seller |
| admin1 | Admin |

Password is not verified.

## Pages

**Public**
- `/` - list of auctions
- `/search` - search by item name
- `/auction/<id>` - auction details + place bid form (doesn't work yet)
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

- **Forms don't save anything.** If you submit a bid or register an account you'll get a message saying the backend isn't connected. That's expected.
- **All database queries should go in `data/queries.py`.** The route files just call functions from there and pass data to templates. See `INTEGRATION.md` for which function connects to which page.
