## Run the UI preview

```bash
pip install -r requirements.txt
flask --app app run --debug
```

Sign in at `/login` using the demo account dropdown (session preview only).

## Read queries

| Function | Route | Template variables |
|----------|-------|-------------------|
| `search_auctions(q)` | `/`, `/search` | `auctions`, `query` (search only) |
| `get_auction_with_item(id)` | `/auction/<id>` | `auction` (with nested `item`) |
| `get_bids_for_auction(id)` | `/auction/<id>` | `bids` |
| `get_user(login)` | `/account` | `user` |
| `get_user_bids(login)` | `/bids` | `bids` (each with nested `auction`) |
| `get_user_wins(login)` | `/wins` | `wins` (with `payment`, `shipment`) |
| `get_payment_for_auction(id)` | `/payment/<id>` | `payment` |
| `get_shipment_for_auction(id)` | `/orders/<id>` | `shipment` |
| `get_seller_hub_stats(login)` | `/sell` | `active_listings`, `total_bids`, `listings` |
| `get_seller_listings(login)` | `/sell/listings` | `listings` |
| `get_item(id)` | `/sell/edit/<id>` | `item` |
| `get_admin_stats()` | `/admin` | `stats` |
| `get_all_users()` | `/admin/users` | `users` |
| `get_all_auctions_enriched()` | `/admin/auctions` | `auctions` |
| `get_all_items()` | `/admin/items` | `items` |
| `get_payments(status)` | `/admin/payments` | `payments` |
| `get_shipments()` | `/admin/shipments` | `shipments` |

## Write operations

| Route | Form fields | SQL function |
|-------|-------------|--------------|
| `POST /login` | login, password | `authenticate_user` |
| `POST /register` | phone_num, login, password, address, favorite_category | `register_user` |
| `POST /account` | phone_num, address, favorite_category | `update_user_profile` |
| `POST /auction/<id>` (bid form) | bid_amount | `place_bid` |
| `POST /sell/create` | item_name, category, starting_price, item_condition, image_url, description | `create_listing` |
| `POST /sell/edit/<id>` | same as create | `update_listing` |
| `POST /sell/auction/<id>/manage` | action=end_auction | `end_auction` |
| `POST /payment/<id>` | — | `process_payment` |
| `POST /admin/users` | role_<login> per row | `update_user_role` |
| `POST /admin/items` | edit_item / remove_item | `update_listing` / `remove_item` |
| `POST /admin/shipments` | status_<id>, tracking_<id> | `update_shipment` |
